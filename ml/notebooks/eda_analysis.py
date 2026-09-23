"""
NOTEBOOK 1: Exploratory Data Analysis (EDA)

Phase 5 - Step 1: Analyze synthetic data distributions, correlations, and patterns.

Run this notebook first to understand the data before building models.

To run:
    cd backend && python -m ml.notebooks.eda_analysis
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sqlalchemy import create_engine
import logging

# Set up visualization style
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (12, 6)

from ml.config import DB_URL, TARGET, NUMERIC_FEATURES, CATEGORICAL_FEATURES
from ml.utils import setup_logging, load_projects_from_database, print_summary

logger = setup_logging()

# =====================================================
# LOAD DATA
# =====================================================

def main():
    """Run exploratory data analysis."""
    
    logger.info("\n" + "="*70)
    logger.info("PHASE 5 - NOTEBOOK 1: EXPLORATORY DATA ANALYSIS (EDA)")
    logger.info("="*70 + "\n")
    
    # Load projects from database
    df = load_projects_from_database()
    
    # Print summary
    print_summary(df, y=df[TARGET] if TARGET in df.columns else None)
    
    # =====================================================
    # BASIC STATISTICS
    # =====================================================
    
    logger.info("\n" + "="*70)
    logger.info("1. BASIC STATISTICS")
    logger.info("="*70 + "\n")
    
    logger.info("Target Variable (delay_probability):")
    if TARGET in df.columns:
        target = df[TARGET].dropna()
        logger.info(f"  Count:  {len(target)}")
        logger.info(f"  Mean:   {target.mean():.4f}")
        logger.info(f"  Median: {target.median():.4f}")
        logger.info(f"  Std:    {target.std():.4f}")
        logger.info(f"  Min:    {target.min():.4f}")
        logger.info(f"  Max:    {target.max():.4f}")
        logger.info(f"  Q1:     {target.quantile(0.25):.4f}")
        logger.info(f"  Q3:     {target.quantile(0.75):.4f}")
    
    # =====================================================
    # NUMERIC FEATURES
    # =====================================================
    
    logger.info("\n" + "="*70)
    logger.info("2. NUMERIC FEATURES DISTRIBUTION")
    logger.info("="*70 + "\n")
    
    numeric_cols = [col for col in NUMERIC_FEATURES if col in df.columns]
    
    for col in numeric_cols:
        data = df[col].dropna()
        if len(data) > 0:
            logger.info(f"\n{col}:")
            logger.info(f"  Count: {len(data)}")
            logger.info(f"  Mean:  {data.mean():.2f}")
            logger.info(f"  Std:   {data.std():.2f}")
            logger.info(f"  Min:   {data.min():.2f}")
            logger.info(f"  Max:   {data.max():.2f}")
            logger.info(f"  Null:  {df[col].isnull().sum()}")
    
    # =====================================================
    # CATEGORICAL FEATURES
    # =====================================================
    
    logger.info("\n" + "="*70)
    logger.info("3. CATEGORICAL FEATURES DISTRIBUTION")
    logger.info("="*70 + "\n")
    
    categorical_cols = [col for col in CATEGORICAL_FEATURES if col in df.columns]
    
    for col in categorical_cols:
        logger.info(f"\n{col}:")
        value_counts = df[col].value_counts()
        for val, count in value_counts.items():
            logger.info(f"  {val}: {count} ({count/len(df)*100:.1f}%)")
        logger.info(f"  Null: {df[col].isnull().sum()}")
    
    # =====================================================
    # CORRELATION ANALYSIS
    # =====================================================
    
    logger.info("\n" + "="*70)
    logger.info("4. CORRELATION WITH TARGET")
    logger.info("="*70 + "\n")
    
    if TARGET in df.columns:
        df_numeric = df[numeric_cols + [TARGET]].fillna(df.mean())
        correlations = df_numeric.corr()[TARGET].sort_values(ascending=False)
        
        logger.info("\nCorrelation with delay_probability:")
        for feature, corr in correlations.items():
            if feature != TARGET:
                logger.info(f"  {feature:40s}: {corr:7.4f}")
    
    # =====================================================
    # MISSING DATA
    # =====================================================
    
    logger.info("\n" + "="*70)
    logger.info("5. MISSING DATA ANALYSIS")
    logger.info("="*70 + "\n")
    
    missing = df.isnull().sum()
    missing_pct = (missing / len(df) * 100)
    
    missing_df = pd.DataFrame({
        'Missing_Count': missing,
        'Missing_Percentage': missing_pct
    }).sort_values('Missing_Count', ascending=False)
    
    logger.info("\n" + missing_df[missing_df['Missing_Count'] > 0].to_string())
    
    # =====================================================
    # OUTLIER DETECTION
    # =====================================================
    
    logger.info("\n" + "="*70)
    logger.info("6. OUTLIER DETECTION (IQR Method)")
    logger.info("="*70 + "\n")
    
    for col in numeric_cols:
        Q1 = df[col].quantile(0.25)
        Q3 = df[col].quantile(0.75)
        IQR = Q3 - Q1
        lower = Q1 - 1.5 * IQR
        upper = Q3 + 1.5 * IQR
        
        outliers = ((df[col] < lower) | (df[col] > upper)).sum()
        if outliers > 0:
            logger.info(f"\n{col}:")
            logger.info(f"  Outliers: {outliers}")
            logger.info(f"  Range: [{lower:.2f}, {upper:.2f}]")
    
    # =====================================================
    # CLASS DISTRIBUTION (Risk Levels)
    # =====================================================
    
    logger.info("\n" + "="*70)
    logger.info("7. RISK LEVEL DISTRIBUTION")
    logger.info("="*70 + "\n")
    
    if TARGET in df.columns:
        target = df[TARGET].dropna()
        
        risk_bins = [0, 0.15, 0.40, 0.70, 1.0]
        risk_labels = ['NO_RISK', 'LOW', 'MEDIUM', 'HIGH']
        risk_counts = pd.cut(target, bins=risk_bins, labels=risk_labels).value_counts()
        
        logger.info("\nRisk Level Distribution:")
        for risk_level, count in risk_counts.items():
            logger.info(f"  {risk_level}: {count} projects ({count/len(target)*100:.1f}%)")
    
    # =====================================================
    # DATA QUALITY INSIGHTS
    # =====================================================
    
    logger.info("\n" + "="*70)
    logger.info("8. DATA QUALITY INSIGHTS")
    logger.info("="*70 + "\n")
    
    logger.info(f"\nTotal Records: {len(df)}")
    logger.info(f"Total Features: {len(df.columns)}")
    logger.info(f"Duplicate Rows: {df.duplicated().sum()}")
    logger.info(f"Complete Cases: {df.dropna().shape[0]}")
    logger.info(f"Rows with Missing Data: {(df.isnull().sum(axis=1) > 0).sum()}")
    
    # =====================================================
    # KEY FINDINGS
    # =====================================================
    
    logger.info("\n" + "="*70)
    logger.info("9. KEY FINDINGS FOR MODEL BUILDING")
    logger.info("="*70 + "\n")
    
    logger.info("""
    ✓ Data loaded successfully from MySQL database
    ✓ {num_records} projects available for training
    ✓ Target variable: delay_probability (continuous, 0-1)
    ✓ Features include: project characteristics, stage info, disputes, grievances
    ✓ Will need to handle missing values (especially in predictions)
    ✓ Consider scaling/normalization for numeric features
    ✓ May need to encode categorical features (project_type, state, stage)
    
    Next Step: Proceed to Notebook 2 (Preprocessing)
    """.format(num_records=len(df)))
    
    logger.info("="*70)
    logger.info("EDA NOTEBOOK COMPLETE")
    logger.info("="*70 + "\n")
    
    return df

if __name__ == "__main__":
    df = main()
