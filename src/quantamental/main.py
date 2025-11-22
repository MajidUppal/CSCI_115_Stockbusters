"""
Main Pipeline Script
Orchestrates the complete Quantamental Model workflow:
1. Data Collection
2. Data Processing
3. Model Training (with W&B)
4. Prediction
5. Backtest & Upload to GCS
"""

import asyncio
import argparse
import logging
from pathlib import Path
import pandas as pd 

from utils import load_config
from data_collect import FMPDataCollector
from data_process import DataProcessor
from model_train import QuantamentalTrainer
from model_predict import QuantamentalPredictor
from backtest import QuantamentalBacktester

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def run_data_collection(config: dict, force_refresh: bool = False):
    """Step 1: Collect data from FMP API"""
    logger.info("="*60)
    logger.info("STEP 1: DATA COLLECTION")
    logger.info("="*60)
    
    if force_refresh:
        import os
        data_dir = config['data']['data_dir']
        cache_files = [
            f"{data_dir}/ohlcv_raw.parquet",
            f"{data_dir}/fundamentals_combined.parquet",
            f"{data_dir}/sp500_index.parquet"
        ]
        for f in cache_files:
            if os.path.exists(f):
                os.remove(f)
                logger.info(f"Removed cache: {f}")
    
    collector = FMPDataCollector(config)
    data = asyncio.run(collector.collect_all())
    
    return data


def run_data_processing(config: dict, data: dict = None):
    """Step 2: Process data and engineer features"""
    logger.info("="*60)
    logger.info("STEP 2: DATA PROCESSING")
    logger.info("="*60)
    
    processor = DataProcessor(config)
    
    if data is None:
        # Load from cache
        import pandas as pd
        data_dir = config['data']['data_dir']
        data = {
            'ohlcv': pd.read_parquet(f"{data_dir}/ohlcv_raw.parquet"),
            'fundamentals': pd.read_parquet(f"{data_dir}/fundamentals_combined.parquet"),
            'sp500_index': pd.read_parquet(f"{data_dir}/sp500_index.parquet")
        }
    
    df_processed = processor.process_all(
        data['ohlcv'],
        data['fundamentals'],
        data['sp500_index']
    )
    
    return df_processed


def run_model_training(config: dict, df: pd.DataFrame = None):
    """Step 3: Train model with W&B logging"""
    logger.info("="*60)
    logger.info("STEP 3: MODEL TRAINING")
    logger.info("="*60)
    
    trainer = QuantamentalTrainer(config)
    
    if df is None:
        # Load from cache
        import pandas as pd
        df = pd.read_parquet(f"{config['data']['data_dir']}/quantamental_monthly.parquet")
    
    model, scaler, metrics = trainer.train_with_wandb(df)
    
    return model, scaler, metrics


def run_prediction(config: dict, df: pd.DataFrame = None):
    """Step 4: Generate predictions"""
    logger.info("="*60)
    logger.info("STEP 4: PREDICTION")
    logger.info("="*60)
    
    predictor = QuantamentalPredictor(config)
    
    if df is None:
        # Load from cache
        import pandas as pd
        df = pd.read_parquet(f"{config['data']['data_dir']}/quantamental_monthly.parquet")
    
    df_predict, top_stocks = predictor.predict_next_month(df)
    
    return df_predict, top_stocks


def run_backtest(config: dict, df: pd.DataFrame = None):
    """Step 5: Backtest and upload to GCS"""
    logger.info("="*60)
    logger.info("STEP 5: BACKTEST & GCS UPLOAD")
    logger.info("="*60)
    
    backtester = QuantamentalBacktester(config)
    
    if df is None:
        # Load from cache
        import pandas as pd
        df = pd.read_parquet(f"{config['data']['data_dir']}/quantamental_monthly.parquet")
    
    results = backtester.run_backtest(df, use_wandb_logging=True)
    
    return results


def run_full_pipeline(force_refresh: bool = False, skip_training: bool = False):
    """Run complete end-to-end pipeline"""
    logger.info("🚀 STARTING FULL QUANTAMENTAL PIPELINE")
    logger.info("="*60)
    
    # Load config
    config = load_config()
    
    # Step 1: Data Collection
    data = run_data_collection(config, force_refresh=force_refresh)
    
    # Step 2: Data Processing
    df_processed = run_data_processing(config, data)
    
    # Step 3: Model Training (optional - skip if model already trained)
    if not skip_training:
        model, scaler, metrics = run_model_training(config, df_processed)
    else:
        logger.info("⏭️  Skipping model training (using existing model from W&B)")
    
    # Step 4: Prediction
    df_predict, top_stocks = run_prediction(config, df_processed)
    
    # Step 5: Backtest & Upload
    results = run_backtest(config, df_processed)
    
    logger.info("="*60)
    logger.info("✅ FULL PIPELINE COMPLETE!")
    logger.info("="*60)
    
    return results


def main():
    parser = argparse.ArgumentParser(description='Quantamental Model Pipeline')
    parser.add_argument(
        '--step',
        choices=['all', 'collect', 'process', 'train', 'predict', 'backtest'],
        default='all',
        help='Which pipeline step to run (default: all)'
    )
    parser.add_argument(
        '--force-refresh',
        action='store_true',
        help='Force refresh data from API (ignore cache)'
    )
    parser.add_argument(
        '--skip-training',
        action='store_true',
        help='Skip model training (use existing model from W&B)'
    )
    
    args = parser.parse_args()
    
    config = load_config()
    
    try:
        if args.step == 'all':
            results = run_full_pipeline(
                force_refresh=args.force_refresh,
                skip_training=args.skip_training
            )
            
        elif args.step == 'collect':
            run_data_collection(config, force_refresh=args.force_refresh)
            
        elif args.step == 'process':
            run_data_processing(config)
            
        elif args.step == 'train':
            run_model_training(config)
            
        elif args.step == 'predict':
            run_prediction(config)
            
        elif args.step == 'backtest':
            run_backtest(config)
        
        logger.info("\n✅ Pipeline execution successful!")
        
    except Exception as e:
        logger.error(f"\n❌ Pipeline failed: {e}", exc_info=True)
        raise


if __name__ == "__main__":
    main()
