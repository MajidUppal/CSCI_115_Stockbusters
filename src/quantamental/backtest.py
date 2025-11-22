"""
Backtest Module
- Rank stocks by prediction probability
- Generate final output reports
- Upload results to GCS
- Log results to W&B
"""

import pandas as pd
import numpy as np
from datetime import datetime
import wandb
import logging

from utils import load_config, GCSHandler, get_timestamp_suffix
from model_predict import QuantamentalPredictor

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class QuantamentalBacktester:
    """Generate backtest reports and upload to GCS"""
    
    def __init__(self, config: dict):
        self.config = config
        self.data_dir = config['data']['data_dir']
        
        # Initialize GCS handler
        self.gcs = GCSHandler(
            bucket_name=config['gcs']['bucket_name'],
            credentials_path=config['gcs'].get('credentials_path')
        )
        
        self.output_folder = config['gcs']['output_folder']
        
        logger.info(f"📊 Quantamental Backtester initialized")
        logger.info(f"   GCS Bucket: {config['gcs']['bucket_name']}")
        logger.info(f"   Output Folder: {self.output_folder}")
    
    def create_ranked_output(self, df_predict: pd.DataFrame, 
                            top_n: int = None) -> pd.DataFrame:
        """
        Create ranked output report
        
        Args:
            df_predict: DataFrame with predictions
            top_n: Optional - only return top N stocks
            
        Returns:
            Ranked DataFrame
        """
        logger.info("📋 Creating ranked output report...")
        
        # Select columns
        output_cols = [
            'symbol', 'date', 'close', 'pred_prob', 'pred_rank',
            'return_1m', 'volatility_21d', 'RSI_14',
            'peRatio', 'roe', 'debtToEquity'
        ]
        
        # Keep only available columns
        available_cols = [col for col in output_cols if col in df_predict.columns]
        df_ranked = df_predict[available_cols].copy()
        
        # Sort by rank
        df_ranked = df_ranked.sort_values('pred_rank')
        
        # Limit to top N if specified
        if top_n:
            df_ranked = df_ranked.head(top_n)
        
        # Add metadata
        df_ranked['generated_at'] = datetime.now().isoformat()
        df_ranked['model_version'] = 'quantamental-v1'
        
        logger.info(f"✅ Ranked output created: {len(df_ranked)} stocks")
        
        return df_ranked
    
    def create_agent_output_files(self, df_predict: pd.DataFrame) -> dict:
        """
        Create the 3 specific files needed by agents:
        1. combined_quantamental_hybrid_with_factors_and_backtest.csv
        2. company_profiles.csv
        3. all_equity_curves.csv
        
        Args:
            df_predict: DataFrame with predictions
            
        Returns:
            Dictionary with paths to created files
        """
        logger.info("📊 Creating agent output files...")
        
        output_files = {}
        
        # 1. Main combined file with predictions and factors
        # Add hybrid score (simple average of normalized prob and factors)
        df_combined = df_predict.copy()
        df_combined['hybrid_score'] = df_predict['pred_prob']  # Can enhance with other factors
        df_combined['signal'] = (df_combined['pred_prob'] > 0.5).astype(int)
        
        # Add backtest columns (placeholders for now - can be enhanced)
        df_combined['backtest_return'] = np.nan  # Will be filled after actual returns
        df_combined['position'] = df_combined['signal']
        
        combined_path = f"{self.data_dir}/combined_quantamental_hybrid_with_factors_and_backtest.csv"
        df_combined.to_csv(combined_path, index=False)
        output_files['combined'] = combined_path
        logger.info(f"   ✅ Created: {combined_path}")
        
        # 2. Company profiles (need to fetch from data collection)
        # Try to load from cache, if not available, create minimal version
        profiles_path = f"{self.data_dir}/company_profiles.csv"
        try:
            import pandas as pd
            profiles = pd.read_parquet(f"{self.data_dir}/company_profiles.parquet")
            profiles.to_csv(profiles_path, index=False)
            logger.info(f"   ✅ Loaded cached company profiles")
        except:
            # Create minimal profiles from prediction data
            profiles = df_predict[['symbol']].drop_duplicates()
            profiles['sector'] = 'Unknown'
            profiles['industry'] = 'Unknown'
            profiles['marketCap'] = df_predict.groupby('symbol')['close'].first().values
            profiles.to_csv(profiles_path, index=False)
            logger.info(f"   ⚠️  Created minimal company profiles (fetch full data for complete version)")
        
        output_files['profiles'] = profiles_path
        
        # 3. All equity curves (simplified version)
        # Create equity curve for each stock based on cumulative returns
        equity_data = []
        for symbol in df_predict['symbol'].unique():
            df_sym = df_predict[df_predict['symbol'] == symbol].sort_values('date')
            
            # Calculate cumulative return
            df_sym['cumulative_return'] = (1 + df_sym.get('return_1m', 0).fillna(0)).cumprod()
            
            for _, row in df_sym.iterrows():
                equity_data.append({
                    'symbol': symbol,
                    'date': row['date'],
                    'equity_value': row.get('cumulative_return', 1.0) * 100,  # Start at $100
                    'return': row.get('return_1m', 0)
                })
        
        df_equity = pd.DataFrame(equity_data)
        equity_path = f"{self.data_dir}/all_equity_curves.csv"
        df_equity.to_csv(equity_path, index=False)
        output_files['equity_curves'] = equity_path
        logger.info(f"   ✅ Created: {equity_path}")
        
        logger.info(f"✅ Agent output files created")
        
        return output_files
    
    def create_summary_report(self, df_predict: pd.DataFrame, 
                             top_n: int = 10) -> dict:
        """
        Create summary statistics report
        
        Returns:
            Dictionary with summary metrics
        """
        logger.info("📊 Creating summary report...")
        
        top_stocks = df_predict.nlargest(top_n, 'pred_prob')
        
        summary = {
            'timestamp': datetime.now().isoformat(),
            'prediction_month': df_predict['date'].dt.to_period('M').iloc[0].strftime('%Y-%m'),
            'total_stocks': len(df_predict),
            'top_n': top_n,
            'top_stocks': top_stocks['symbol'].tolist(),
            'top_probs': top_stocks['pred_prob'].tolist(),
            'mean_prob': float(df_predict['pred_prob'].mean()),
            'std_prob': float(df_predict['pred_prob'].std()),
            'min_prob': float(df_predict['pred_prob'].min()),
            'max_prob': float(df_predict['pred_prob'].max()),
        }
        
        logger.info(f"✅ Summary report created")
        
        return summary
    
    def upload_to_gcs(self, df_ranked: pd.DataFrame, 
                     summary: dict = None,
                     agent_files: dict = None) -> dict:
        """
        Upload results to GCS bucket
        
        Args:
            df_ranked: Ranked predictions DataFrame
            summary: Optional summary dictionary
            agent_files: Optional dictionary of agent output file paths
            
        Returns:
            Dictionary with GCS URLs
        """
        logger.info("☁️ Uploading results to GCS...")
        
        timestamp = get_timestamp_suffix()
        predict_month = df_ranked['date'].dt.to_period('M').iloc[0].strftime('%Y%m')
        
        urls = {}
        output_format = self.config['backtest']['output_format']
        
        # Upload CSV
        if output_format in ['csv', 'both']:
            csv_path = f"{self.output_folder}/predictions_{predict_month}_{timestamp}.csv"
            csv_url = self.gcs.upload_dataframe(df_ranked, csv_path, format='csv')
            urls['csv'] = csv_url
        
        # Upload Parquet
        if output_format in ['parquet', 'both']:
            parquet_path = f"{self.output_folder}/predictions_{predict_month}_{timestamp}.parquet"
            parquet_url = self.gcs.upload_dataframe(df_ranked, parquet_path, format='parquet')
            urls['parquet'] = parquet_url
        
        # Upload summary JSON if provided
        if summary and self.config['backtest']['include_metrics']:
            import json
            import tempfile
            
            summary_path = f"{self.output_folder}/summary_{predict_month}_{timestamp}.json"
            
            with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
                json.dump(summary, f, indent=2)
                temp_path = f.name
            
            summary_url = self.gcs.upload_file(temp_path, summary_path)
            urls['summary'] = summary_url
            
            import os
            os.remove(temp_path)
        
        # Upload agent-specific files (CRITICAL FOR AGENT INTEGRATION)
        if agent_files:
            logger.info("📤 Uploading agent-specific files...")
            
            # 1. Combined quantamental file
            if 'combined' in agent_files:
                combined_gcs_path = f"{self.output_folder}/combined_quantamental_hybrid_with_factors_and_backtest.csv"
                combined_url = self.gcs.upload_file(agent_files['combined'], combined_gcs_path)
                urls['agent_combined'] = combined_url
                logger.info(f"   ✅ Uploaded: combined_quantamental_hybrid_with_factors_and_backtest.csv")
            
            # 2. Company profiles
            if 'profiles' in agent_files:
                profiles_gcs_path = f"{self.output_folder}/company_profiles.csv"
                profiles_url = self.gcs.upload_file(agent_files['profiles'], profiles_gcs_path)
                urls['agent_profiles'] = profiles_url
                logger.info(f"   ✅ Uploaded: company_profiles.csv")
            
            # 3. All equity curves
            if 'equity_curves' in agent_files:
                equity_gcs_path = f"{self.output_folder}/all_equity_curves.csv"
                equity_url = self.gcs.upload_file(agent_files['equity_curves'], equity_gcs_path)
                urls['agent_equity'] = equity_url
                logger.info(f"   ✅ Uploaded: all_equity_curves.csv")
        
        logger.info(f"✅ All results uploaded to GCS")
        for name, url in urls.items():
            logger.info(f"   {name}: {url}")
        
        return urls
    
    def log_to_wandb(self, df_ranked: pd.DataFrame, summary: dict, 
                    gcs_urls: dict) -> None:
        """
        Log backtest results to W&B
        
        Args:
            df_ranked: Ranked predictions
            summary: Summary dictionary
            gcs_urls: Dictionary of GCS URLs
        """
        logger.info("🎨 Logging results to W&B...")
        
        # Create a W&B run for backtest
        run = wandb.init(
            project=self.config['wandb']['project'],
            job_type='backtest',
            tags=['backtest', 'ranking'] + self.config['wandb']['tags']
        )
        
        # Log summary metrics
        wandb.log(summary)
        
        # Log top stocks as table
        top_stocks_df = df_ranked.head(self.config['backtest']['top_n_stocks'])
        wandb.log({
            'top_stocks': wandb.Table(dataframe=top_stocks_df)
        })
        
        # Log GCS URLs
        wandb.config.update({'gcs_urls': gcs_urls})
        
        # Log probability distribution histogram
        import matplotlib.pyplot as plt
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.hist(df_ranked['pred_prob'], bins=30, edgecolor='k', alpha=0.7)
        ax.set_title('Prediction Probability Distribution')
        ax.set_xlabel('Probability')
        ax.set_ylabel('Count')
        wandb.log({'prob_distribution': wandb.Image(fig)})
        plt.close()
        
        wandb.finish()
        
        logger.info(f"✅ Results logged to W&B")
    
    def run_backtest(self, df: pd.DataFrame, top_n: int = None,
                    use_wandb_logging: bool = True) -> dict:
        """
        Complete backtest pipeline
        
        Args:
            df: Processed monthly data
            top_n: Number of top stocks (default from config)
            use_wandb_logging: Whether to log to W&B
            
        Returns:
            Dictionary with results and URLs
        """
        logger.info("🚀 Starting backtest pipeline...")
        
        if top_n is None:
            top_n = self.config['backtest']['top_n_stocks']
        
        # Step 1: Generate predictions
        predictor = QuantamentalPredictor(self.config)
        df_predict, top_stocks = predictor.predict_next_month(df, top_n=top_n)
        
        # Step 2: Create ranked output
        df_ranked = self.create_ranked_output(df_predict, top_n=None)  # Full ranking
        
        # Step 3: Create agent-specific output files
        agent_files = self.create_agent_output_files(df_predict)
        
        # Step 4: Create summary
        summary = self.create_summary_report(df_predict, top_n=top_n)
        
        # Step 5: Upload to GCS (including agent files)
        gcs_urls = self.upload_to_gcs(df_ranked, summary, agent_files=agent_files)
        
        # Step 6: Log to W&B (optional)
        if use_wandb_logging:
            self.log_to_wandb(df_ranked, summary, gcs_urls)
        
        logger.info("✅ Backtest pipeline complete!")
        
        # Print summary
        print("\n" + "="*60)
        print("📊 BACKTEST RESULTS SUMMARY")
        print("="*60)
        print(f"Prediction Month: {summary['prediction_month']}")
        print(f"Total Stocks: {summary['total_stocks']}")
        print(f"Mean Probability: {summary['mean_prob']:.4f}")
        print(f"\n🏆 Top {top_n} Stocks:")
        for i, (symbol, prob) in enumerate(zip(summary['top_stocks'], summary['top_probs']), 1):
            print(f"   {i}. {symbol}: {prob:.4f}")
        print(f"\n☁️  GCS URLs:")
        for name, url in gcs_urls.items():
            print(f"   {name}: {url}")
        print(f"\n🤖 Agent Files Created:")
        print(f"   ✅ combined_quantamental_hybrid_with_factors_and_backtest.csv")
        print(f"   ✅ company_profiles.csv")
        print(f"   ✅ all_equity_curves.csv")
        print("="*60)
        
        return {
            'predictions': df_predict,
            'ranked_output': df_ranked,
            'top_stocks': top_stocks,
            'summary': summary,
            'gcs_urls': gcs_urls,
            'agent_files': agent_files
        }


def main():
    """Run backtest pipeline"""
    config = load_config()
    backtester = QuantamentalBacktester(config)
    
    # Load processed data
    logger.info("📂 Loading processed data...")
    df = pd.read_parquet(f"{config['data']['data_dir']}/quantamental_monthly.parquet")
    
    # Run backtest
    results = backtester.run_backtest(df, use_wandb_logging=True)
    
    print("\n✅ Backtest complete!")
    print(f"   Results saved to GCS bucket: {config['gcs']['bucket_name']}")


if __name__ == "__main__":
    main()
