"""
ML Pipeline Master Script

Phase 5: Complete ML Pipeline Runner

This script runs the entire ML pipeline in sequence:
  1. EDA - Exploratory Data Analysis
  2. Preprocessing - Data cleaning and preparation
  3. Feature Engineering - Feature selection and creation
  4. Model Training - Train and evaluate models

Usage:
    python run_pipeline.py                  # Run all steps
    python run_pipeline.py --step eda       # Run only EDA
    python run_pipeline.py --step training  # Run only training

"""

import sys
import argparse
import logging
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from ml.utils import setup_logging
from ml.notebooks import eda_analysis, preprocessing, feature_engineering, model_training

logger = setup_logging()

# =====================================================
# PIPELINE RUNNER
# =====================================================

def run_all_steps():
    """Run entire ML pipeline."""
    
    logger.info("\n" + "="*70)
    logger.info("PHASE 5: COMPLETE ML PIPELINE")
    logger.info("="*70 + "\n")
    
    try:
        # Step 1: EDA
        logger.info("\n" + ">"*70)
        logger.info("STEP 1: EXPLORATORY DATA ANALYSIS")
        logger.info(">"*70 + "\n")
        df_eda = eda_analysis.main()
        
        # Step 2: Preprocessing
        logger.info("\n" + ">"*70)
        logger.info("STEP 2: DATA PREPROCESSING")
        logger.info(">"*70 + "\n")
        X_processed, y = preprocessing.main()
        
        # Step 3: Feature Engineering
        logger.info("\n" + ">"*70)
        logger.info("STEP 3: FEATURE ENGINEERING & SELECTION")
        logger.info(">"*70 + "\n")
        feature_engineering.main()
        
        # Step 4: Model Training
        logger.info("\n" + ">"*70)
        logger.info("STEP 4: MODEL TRAINING & EVALUATION")
        logger.info(">"*70 + "\n")
        best_model, results = model_training.main()
        
        # =====================================================
        # FINAL SUMMARY
        # =====================================================
        
        logger.info("\n" + "="*70)
        logger.info("PIPELINE COMPLETE!")
        logger.info("="*70 + "\n")
        
        logger.info("""
        ✓ All 4 notebooks executed successfully
        ✓ Trained model saved and ready for use
        ✓ Model artifacts:
           - ml/models/best_model.pkl
           - ml/models/scaler.pkl
           - ml/models/encoder.pkl
           - ml/models/feature_names.pkl
           - ml/data/model_metadata.json
        
        ✓ Next: Integrate with services/prediction_service.py
        ✓ Then: Test API endpoint /api/predict
        ✓ Finally: Deploy to production
        """)
        
        return True
        
    except Exception as e:
        logger.error(f"\n✗ Pipeline failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def run_step(step):
    """Run specific pipeline step."""
    
    steps = {
        'eda': ('EDA', eda_analysis.main),
        'preprocessing': ('Preprocessing', preprocessing.main),
        'features': ('Feature Engineering', feature_engineering.main),
        'training': ('Model Training', model_training.main),
    }
    
    if step not in steps:
        logger.error(f"Unknown step: {step}")
        logger.info(f"Available steps: {', '.join(steps.keys())}")
        return False
    
    step_name, step_func = steps[step]
    
    logger.info("\n" + "="*70)
    logger.info(f"RUNNING: {step_name}")
    logger.info("="*70 + "\n")
    
    try:
        step_func()
        logger.info(f"\n✓ {step_name} completed successfully")
        return True
    except Exception as e:
        logger.error(f"\n✗ {step_name} failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

# =====================================================
# CLI INTERFACE
# =====================================================

def main():
    """Main entry point."""
    
    parser = argparse.ArgumentParser(
        description='ML Pipeline Runner for Land Acquisition Prediction',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python run_pipeline.py              # Run all 4 steps
  python run_pipeline.py --step eda   # Run only EDA
  python run_pipeline.py --step training  # Run only model training
        """
    )
    
    parser.add_argument(
        '--step',
        choices=['eda', 'preprocessing', 'features', 'training'],
        help='Run specific pipeline step (default: run all)'
    )
    
    args = parser.parse_args()
    
    if args.step:
        success = run_step(args.step)
    else:
        success = run_all_steps()
    
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
