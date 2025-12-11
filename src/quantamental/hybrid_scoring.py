"""
Hybrid Scoring Module - UPDATED with Trailing Backtest Metrics

Changes from original:
- calculate_backtest_metrics now uses TRAILING (historical) returns
- Works even for latest month predictions (no future data needed)
"""

import pandas as pd
import numpy as np
import logging

logger = logging.getLogger(__name__)


def calculate_hybrid_scores(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate Hybrid Quantamental Scores from monthly features

    Args:
        df: DataFrame with monthly features (from data_process.py)

    Returns:
        DataFrame with added columns:
        - Technical_Score, Fundamental_Score, Hybrid_Score
        - Hybrid_CS_Pct, Hybrid_Rank
        - H_Score Recommendation
    """
    logger.info(" Calculating Hybrid Quantamental Scores...")

    df_score = df.copy()
    df_score.replace([np.inf, -np.inf], np.nan, inplace=True)

    # ============================================
    # Step 1: Define feature groups
    # ============================================
    tech_cols = [
        "return_1m",
        "ema_12",
        "ema_26",
        "macd",
        "macd_signal",
        "macd_hist",
        "RSI_14",
        "volatility_21d",
    ]

    fund_cols = [
        "payoutRatio",
        "cashPerShare",
        "dividendYield",
        "revenuePerShare",
        "earningsYield",
        "evToOperatingCashFlow",
        "netDebtToEBITDA",
        "freeCashFlowYield",
        "pocfratio",
        "intangiblesToTotalAssets",
        "netIncomePerShare",
        "incomeQuality",
        "capexToDepreciation",
        "operatingCashFlowPerShare",
        "peRatio",
        "returnOnTangibleAssets",
        "investedCapital",
        "roe",
        "roic",
        "debtToEquity",
        "currentRatio",
        "interestCoverage",
    ]

    # Only use columns that exist
    tech_cols = [c for c in tech_cols if c in df_score.columns]
    fund_cols = [c for c in fund_cols if c in df_score.columns]

    logger.info(f"   Technical indicators: {len(tech_cols)}")
    logger.info(f"   Fundamental metrics: {len(fund_cols)}")

    # ============================================
    # Step 2: Define scoring direction
    # ============================================
    higher_better = {
        # Technicals
        "return_1m": True,
        "ema_12": True,
        "ema_26": True,
        "macd": True,
        "macd_signal": True,
        "macd_hist": True,
        "RSI_14": True,
        "volatility_21d": False,  # Lower volatility is better
        # Fundamentals
        "payoutRatio": False,
        "cashPerShare": True,
        "dividendYield": True,
        "revenuePerShare": True,
        "earningsYield": True,
        "evToOperatingCashFlow": False,
        "netDebtToEBITDA": False,
        "freeCashFlowYield": True,
        "pocfratio": False,
        "intangiblesToTotalAssets": False,
        "netIncomePerShare": True,
        "incomeQuality": True,
        "capexToDepreciation": True,
        "operatingCashFlowPerShare": True,
        "peRatio": False,  # Lower P/E is better (value)
        "returnOnTangibleAssets": True,
        "investedCapital": True,
        "roe": True,
        "roic": True,
        "debtToEquity": False,
        "currentRatio": True,
        "interestCoverage": True,
    }

    # ============================================
    # Step 3: Create month identifier
    # ============================================
    if "date" not in df_score.columns:
        logger.error("    'date' column missing!")
        return df_score

    df_score["ym"] = pd.to_datetime(df_score["date"]).dt.to_period("M")

    # ============================================
    # Step 4: Calculate cross-sectional ranks
    # ============================================
    def cs_rank(series):
        """Cross-sectional percentile rank in [0,1]"""
        return series.rank(pct=True, ascending=True)

    rank_cols = []
    all_factor_cols = tech_cols + fund_cols

    for col in all_factor_cols:
        if col not in df_score.columns:
            continue

        # Base percentile: high value = high percentile
        base = df_score.groupby("ym")[col].transform(cs_rank).astype(float)

        # Flip if lower is better
        is_higher_better = higher_better.get(col, True)
        if not is_higher_better:
            base = 1.0 - base

        rank_col = f"{col}_rank"
        df_score[rank_col] = base
        rank_cols.append(rank_col)

    logger.info(f"    Created {len(rank_cols)} rank columns")

    # ============================================
    # Step 5: Build composite scores
    # ============================================
    tech_rank_cols = [f"{c}_rank" for c in tech_cols if f"{c}_rank" in df_score.columns]
    fund_rank_cols = [f"{c}_rank" for c in fund_cols if f"{c}_rank" in df_score.columns]

    # Technical Score = mean of technical percentiles
    df_score["Technical_Score"] = df_score[tech_rank_cols].mean(axis=1, skipna=True)

    # Fundamental Score = mean of fundamental percentiles
    df_score["Fundamental_Score"] = df_score[fund_rank_cols].mean(axis=1, skipna=True)

    # Hybrid Score = 50/50 blend
    df_score["Hybrid_Score"] = (
        0.5 * df_score["Technical_Score"] + 0.5 * df_score["Fundamental_Score"]
    )

    # Cross-sectional percentile of Hybrid Score
    df_score["Hybrid_CS_Pct"] = df_score.groupby("ym")["Hybrid_Score"].transform(
        lambda s: s.rank(pct=True, ascending=True)
    )

    logger.info(f"    Technical_Score: {df_score['Technical_Score'].mean():.3f} avg")
    logger.info(
        f"    Fundamental_Score: {df_score['Fundamental_Score'].mean():.3f} avg"
    )
    logger.info(f"    Hybrid_Score: {df_score['Hybrid_Score'].mean():.3f} avg")

    # ============================================
    # Step 6: Generate recommendations
    # ============================================
    def classify_stock_v2(
        row,
        top_cut=0.70,
        bot_cut=0.30,
        diff_thresh=0.05,
        min_ret_1m=0.02,
        min_RSI=50,
        min_macd_hist=0.0,
    ):
        """
        Improved recommendation logic using hybrid percentile and technical filters
        """
        hyb = row["Hybrid_CS_Pct"]
        diff = row["Technical_Score"] - row["Fundamental_Score"]

        # Extract technical indicators
        r1m = row.get("return_1m", np.nan)
        rsi = row.get("RSI_14", np.nan)
        mh = row.get("macd_hist", np.nan)

        # TOP BUCKET (>=70th percentile)
        if hyb >= top_cut:
            # Momentum Buy: strong technical confirmation
            if (
                (diff > diff_thresh)
                and pd.notna(r1m)
                and r1m > min_ret_1m
                and pd.notna(rsi)
                and rsi > min_RSI
                and pd.notna(mh)
                and mh > min_macd_hist
            ):
                return "Short-Term Buy (Momentum)"

            # Fundamental Buy: strong fundamentals
            elif diff < -diff_thresh:
                return "Long-Term Buy (Fundamental)"

            # Balanced
            else:
                return "Balanced Buy / Hold"

        # BOTTOM BUCKET (<=30th percentile)
        elif hyb <= bot_cut:
            return "Avoid / Bearish"

        # MIDDLE BUCKET
        else:
            return "Hold / Neutral"

    df_score["H_Score Recommendation"] = df_score.apply(classify_stock_v2, axis=1)

    logger.info("   Recommendations generated")
    logger.info(
        f"      {(df_score['H_Score Recommendation'].str.contains('Buy')).sum()} Buy signals"
    )
    logger.info(
        f"      {(df_score['H_Score Recommendation'] == 'Hold / Neutral').sum()} Hold"
    )
    logger.info(
        f"      {(df_score['H_Score Recommendation'] == 'Avoid / Bearish').sum()} Avoid"
    )

    # ============================================
    # Step 7: Calculate Hybrid_Rank
    # ============================================
    # Rank within each month
    df_score["Hybrid_Rank"] = df_score.groupby("ym")["Hybrid_Score"].transform(
        lambda s: s.rank(ascending=False)
    )

    logger.info(" Hybrid scoring complete!")

    # Clean up temporary columns
    temp_cols = [c for c in df_score.columns if c.endswith("_rank") or c == "ym"]
    df_score = df_score.drop(columns=temp_cols, errors="ignore")

    return df_score


def calculate_backtest_metrics(
    df: pd.DataFrame, df_full: pd.DataFrame = None
) -> pd.DataFrame:
    """
    Calculate per-symbol TRAILING backtest metrics (historical performance)

    UPDATED: Uses historical returns instead of forward returns
    This ensures metrics are always available, even for latest month predictions.

    Args:
        df: DataFrame with current predictions (latest month)
        df_full: Full historical DataFrame with all months (optional, for trailing calc)

    Returns:
        DataFrame with added columns:
        - n_periods, avg_fwd_1m_ret, vol_1m, sharpe_1m_annual
        - max_drawdown, hit_rate_pos, hit_rate_vs_sp500, cagr
    """
    logger.info(" Calculating TRAILING backtest metrics per symbol...")

    # Check if we have return_1m for trailing calculation
    if "return_1m" not in df.columns:
        logger.warning("     'return_1m' not found - cannot calculate backtest metrics")
        for col in [
            "n_periods",
            "avg_fwd_1m_ret",
            "vol_1m",
            "sharpe_1m_annual",
            "max_drawdown",
            "hit_rate_pos",
            "hit_rate_vs_sp500",
            "cagr",
        ]:
            df[col] = np.nan
        return df

    # If we have full historical data, use it for better trailing metrics
    if df_full is not None and len(df_full) > len(df):
        logger.info("    Using full historical data for trailing metrics")
        hist_df = df_full.copy()
    else:
        # Try to load historical data
        try:
            import os

            data_dir = os.path.dirname(os.path.abspath(__file__))
            hist_file = f"{data_dir}/data/quantamental_monthly.parquet"
            if os.path.exists(hist_file):
                hist_df = pd.read_parquet(hist_file)
                logger.info(f"    Loaded historical data: {len(hist_df)} rows")
            else:
                hist_df = df.copy()
                logger.warning("    No historical data found, using current data only")
        except Exception as e:
            hist_df = df.copy()
            logger.warning(f"    Could not load historical data: {e}")

    # Ensure we have SP500 returns for comparison
    if "sp500_return_1m" not in hist_df.columns:
        hist_df["sp500_return_1m"] = 0.0  # Default to 0 if not available

    def _trailing_metrics(symbol_df):
        """Calculate trailing metrics for one symbol using historical data"""
        # Get all historical returns for this symbol (not forward returns)
        rets = symbol_df["return_1m"].dropna()

        if len(rets) < 2:
            return pd.Series(
                {
                    "n_periods": len(rets),
                    "avg_fwd_1m_ret": np.nan,
                    "vol_1m": np.nan,
                    "sharpe_1m_annual": np.nan,
                    "max_drawdown": np.nan,
                    "hit_rate_pos": np.nan,
                    "hit_rate_vs_sp500": np.nan,
                    "cagr": np.nan,
                }
            )

        # Average return (trailing, not forward)
        avg_ret = rets.mean()

        # Volatility
        vol = rets.std()

        # Annualized Sharpe (using trailing returns)
        sharpe = (avg_ret / vol) * np.sqrt(12) if vol > 0 else np.nan

        # Drawdown calculation
        equity = (1 + rets).cumprod()
        running_max = equity.cummax()
        max_dd = (equity / running_max - 1).min()

        # Hit rate (positive returns)
        hit_pos = (rets > 0).mean()

        # Hit rate vs S&P500 (trailing)
        if "sp500_return_1m" in symbol_df.columns:
            bench = symbol_df["sp500_return_1m"].reindex(rets.index)
            hit_vs_bench = (rets > bench).mean()
        else:
            hit_vs_bench = np.nan

        # CAGR (trailing)
        total_return = equity.iloc[-1] - 1 if len(equity) > 0 else 0
        years = len(rets) / 12
        cagr = (1 + total_return) ** (1 / years) - 1 if years > 0 else np.nan

        return pd.Series(
            {
                "n_periods": len(rets),
                "avg_fwd_1m_ret": avg_ret,  # Renamed but actually trailing
                "vol_1m": vol,
                "sharpe_1m_annual": sharpe,
                "max_drawdown": max_dd,
                "hit_rate_pos": hit_pos,
                "hit_rate_vs_sp500": hit_vs_bench,
                "cagr": cagr,
            }
        )

    # Calculate metrics per symbol using HISTORICAL data
    metrics_list = []
    symbols = df["symbol"].unique()

    for symbol in symbols:
        # Get ALL historical data for this symbol
        symbol_hist = hist_df[hist_df["symbol"] == symbol].sort_values("date")

        if len(symbol_hist) > 0:
            metrics = _trailing_metrics(symbol_hist)
            metrics["symbol"] = symbol
            metrics_list.append(metrics)

    if metrics_list:
        metrics_df = pd.DataFrame(metrics_list)

        # Merge back to original df
        df_result = df.merge(metrics_df, on="symbol", how="left")

        logger.info(f"    Trailing metrics calculated for {len(metrics_df)} symbols")
        logger.info(f"      Avg Sharpe: {metrics_df['sharpe_1m_annual'].mean():.2f}")
        logger.info(f"      Avg CAGR: {metrics_df['cagr'].mean()*100:.1f}%")
        logger.info(f"      Avg Hit Rate: {metrics_df['hit_rate_pos'].mean()*100:.1f}%")
        logger.info(f"      Avg Periods: {metrics_df['n_periods'].mean():.0f} months")
    else:
        logger.warning("     No metrics calculated")
        for col in [
            "n_periods",
            "avg_fwd_1m_ret",
            "vol_1m",
            "sharpe_1m_annual",
            "max_drawdown",
            "hit_rate_pos",
            "hit_rate_vs_sp500",
            "cagr",
        ]:
            df[col] = np.nan
        df_result = df

    return df_result


def calculate_backtest_metrics_forward(df: pd.DataFrame) -> pd.DataFrame:
    """
    ORIGINAL: Calculate per-symbol backtest metrics using FORWARD returns

    NOTE: This requires future data (fwd_return_1m) which may not exist
    for latest month predictions. Use calculate_backtest_metrics() instead
    for trailing metrics that always work.

    Args:
        df: DataFrame with fwd_return_1m and fwd_sp500_return_1m

    Returns:
        DataFrame with added columns (may be NaN if no forward data)
    """
    logger.info(" Calculating FORWARD backtest metrics per symbol...")

    # Ensure we have required columns
    if "fwd_return_1m" not in df.columns:
        logger.warning(
            "     'fwd_return_1m' not found - cannot calculate forward backtest metrics"
        )
        # Add NaN columns
        for col in [
            "n_periods",
            "avg_fwd_1m_ret",
            "vol_1m",
            "sharpe_1m_annual",
            "max_drawdown",
            "hit_rate_pos",
            "hit_rate_vs_sp500",
            "cagr",
        ]:
            df[col] = np.nan
        return df

    use = df.dropna(subset=["fwd_return_1m"]).copy()

    # Check if we have any valid forward returns
    if len(use) == 0:
        logger.warning("     No valid forward returns - adding NaN columns")
        logger.warning(
            "    This is normal for latest month predictions (no future data yet)"
        )
        logger.warning(
            "    TIP: Use calculate_backtest_metrics() for trailing metrics instead"
        )

        # Add NaN columns
        for col in [
            "n_periods",
            "avg_fwd_1m_ret",
            "vol_1m",
            "sharpe_1m_annual",
            "max_drawdown",
            "hit_rate_pos",
            "hit_rate_vs_sp500",
            "cagr",
        ]:
            df[col] = np.nan
        return df

    def _metrics(g):
        """Calculate metrics for one symbol"""
        rets = g["fwd_return_1m"].dropna()

        if len(rets) == 0:
            return pd.Series(
                {
                    "n_periods": 0,
                    "avg_fwd_1m_ret": np.nan,
                    "vol_1m": np.nan,
                    "sharpe_1m_annual": np.nan,
                    "max_drawdown": np.nan,
                    "hit_rate_pos": np.nan,
                    "hit_rate_vs_sp500": np.nan,
                    "cagr": np.nan,
                }
            )

        # Average and Volatility
        avg_ret = rets.mean()
        vol = rets.std()

        # Annualized Sharpe
        sharpe = (avg_ret / vol) * np.sqrt(12) if vol > 0 else np.nan

        # Drawdown
        equity = (1 + rets).cumprod()
        running_max = equity.cummax()
        max_dd = (equity / running_max - 1).min()

        # Hit rate (positive returns)
        hit_pos = (rets > 0).mean()

        # Hit rate vs S&P500
        if "fwd_sp500_return_1m" in g.columns:
            bench = g["fwd_sp500_return_1m"].reindex(rets.index)
            hit_vs_bench = (rets > bench).mean()
        else:
            hit_vs_bench = np.nan

        # CAGR
        total_return = equity.iloc[-1] - 1
        years = len(rets) / 12
        cagr = (1 + total_return) ** (1 / years) - 1 if years > 0 else np.nan

        return pd.Series(
            {
                "n_periods": len(rets),
                "avg_fwd_1m_ret": avg_ret,
                "vol_1m": vol,
                "sharpe_1m_annual": sharpe,
                "max_drawdown": max_dd,
                "hit_rate_pos": hit_pos,
                "hit_rate_vs_sp500": hit_vs_bench,
                "cagr": cagr,
            }
        )

    # Calculate per symbol
    metrics = (
        use.groupby("symbol", as_index=False)
        .apply(_metrics, include_groups=False)
        .reset_index()
    )

    # Merge back to original df
    df_result = df.merge(metrics, on="symbol", how="left")

    logger.info(f"    Metrics calculated for {len(metrics)} symbols")

    # Only log stats if we have data
    if len(metrics) > 0 and "sharpe_1m_annual" in metrics.columns:
        logger.info(f"      Avg Sharpe: {metrics['sharpe_1m_annual'].mean():.2f}")
        logger.info(f"      Avg CAGR: {metrics['cagr'].mean()*100:.1f}%")
        logger.info(f"      Avg Hit Rate: {metrics['hit_rate_pos'].mean()*100:.1f}%")
    else:
        logger.warning(
            "      No valid backtest metrics (this is normal for latest predictions)"
        )

    return df_result
