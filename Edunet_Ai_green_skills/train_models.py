"""
Phase 2: Model Development
Train ML models to predict Oxygen Level and Number of People
"""

import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score, mean_absolute_error, mean_squared_error
import joblib
import os
from glob import glob

# Configuration
DATASETS_DIR = "Datasets"
MODELS_DIR = "models"

# Feature columns
FEATURE_COLS = [
    'Altitude', 'Pressure', 'Temperature', 'Humidity', 'WindSpeed',
    'CO2', 'PM2.5', 'NDVI', 'PopulationDensity'
]

# Target columns
TARGET_OXYGEN = 'Oxygen Level'
TARGET_PEOPLE = 'Number of People'

def load_all_datasets(datasets_dir):
    """
    Load all CSV files from the datasets directory
    """
    print("Loading all datasets...")
    all_data = []
    
    # Get all CSV files
    csv_files = glob(os.path.join(datasets_dir, "*.csv"))
    
    for file in csv_files:
        location_name = os.path.basename(file).replace("_dataset.csv", "").replace("_dataset_updated.csv", "")
        df = pd.read_csv(file)
        df['Location'] = location_name
        all_data.append(df)
        print(f"  ✓ Loaded {location_name}: {len(df)} rows")
    
    # Combine all datasets
    combined_data = pd.concat(all_data, ignore_index=True)
    print(f"\nTotal rows: {len(combined_data)}")
    print(f"Total locations: {len(csv_files)}")
    
    return combined_data

def prepare_data(df):
    """
    Prepare features and targets from the dataframe
    """
    # Check for missing values in features and targets
    print("\nChecking for missing values...")
    
    # Check features
    feature_missing = df[FEATURE_COLS].isnull().sum()
    if feature_missing.sum() > 0:
        print(f"Missing values in features: \n{feature_missing[feature_missing > 0]}")
    
    # Check targets
    target_missing = df[[TARGET_OXYGEN, TARGET_PEOPLE]].isnull().sum()
    if target_missing.sum() > 0:
        print(f"Missing values in targets: \n{target_missing[target_missing > 0]}")
    
    # Drop rows with any missing values (in features or targets)
    initial_rows = len(df)
    df = df.dropna(subset=FEATURE_COLS + [TARGET_OXYGEN, TARGET_PEOPLE])
    final_rows = len(df)
    
    if initial_rows != final_rows:
        print(f"Dropped {initial_rows - final_rows} rows with missing values")
    
    # Prepare features and targets
    X = df[FEATURE_COLS].values
    y_oxygen = df[TARGET_OXYGEN].values
    y_people = df[TARGET_PEOPLE].values
    
    print(f"\nFeatures shape: {X.shape}")
    print(f"Oxygen target shape: {y_oxygen.shape}")
    print(f"People target shape: {y_people.shape}")
    
    return X, y_oxygen, y_people

def train_and_evaluate_model(X, y, model_name, test_size=0.2, random_state=42):
    """
    Train a RandomForest model and evaluate it
    """
    print(f"\n{'='*60}")
    print(f"Training {model_name}")
    print(f"{'='*60}")
    
    # Split the data
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, random_state=random_state
    )
    
    print(f"Training set size: {len(X_train)}")
    print(f"Test set size: {len(X_test)}")
    
    # Initialize and train the model
    model = RandomForestRegressor(
        n_estimators=100,
        max_depth=15,
        min_samples_split=5,
        min_samples_leaf=2,
        random_state=random_state,
        n_jobs=-1
    )
    
    print("\nTraining model...")
    model.fit(X_train, y_train)
    
    # Make predictions
    y_train_pred = model.predict(X_train)
    y_test_pred = model.predict(X_test)
    
    # Calculate metrics
    train_r2 = r2_score(y_train, y_train_pred)
    test_r2 = r2_score(y_test, y_test_pred)
    train_mae = mean_absolute_error(y_train, y_train_pred)
    test_mae = mean_absolute_error(y_test, y_test_pred)
    train_rmse = np.sqrt(mean_squared_error(y_train, y_train_pred))
    test_rmse = np.sqrt(mean_squared_error(y_test, y_test_pred))
    
    # Display results
    print(f"\n{'='*60}")
    print(f"MODEL EVALUATION RESULTS")
    print(f"{'='*60}")
    print(f"{'Metric':<20} {'Training':<20} {'Testing':<20}")
    print(f"{'-'*60}")
    print(f"{'R² Score':<20} {train_r2:<20.4f} {test_r2:<20.4f}")
    print(f"{'MAE':<20} {train_mae:<20.4f} {test_mae:<20.4f}")
    print(f"{'RMSE':<20} {train_rmse:<20.4f} {test_rmse:<20.4f}")
    print(f"{'='*60}\n")
    
    # Feature importance
    feature_importance = pd.DataFrame({
        'Feature': FEATURE_COLS,
        'Importance': model.feature_importances_
    }).sort_values('Importance', ascending=False)
    
    print("Top 5 Important Features:")
    for i, (idx, row) in enumerate(feature_importance.head().iterrows(), 1):
        print(f"  {i}. {row['Feature']:<20} {row['Importance']:.4f}")
    
    return model, {
        'train_r2': train_r2,
        'test_r2': test_r2,
        'train_mae': train_mae,
        'test_mae': test_mae,
        'train_rmse': train_rmse,
        'test_rmse': test_rmse
    }

def save_model(model, filename):
    """
    Save the trained model using joblib
    """
    os.makedirs(MODELS_DIR, exist_ok=True)
    filepath = os.path.join(MODELS_DIR, filename)
    joblib.dump(model, filepath)
    print(f"✓ Model saved to: {filepath}")

def main():
    """
    Main execution function
    """
    print("="*60)
    print("PHASE 2: MODEL DEVELOPMENT")
    print("="*60)
    
    # Load all datasets
    df = load_all_datasets(DATASETS_DIR)
    
    # Prepare data
    X, y_oxygen, y_people = prepare_data(df)
    
    # Train Oxygen Level model
    model_oxygen, metrics_oxygen = train_and_evaluate_model(
        X, y_oxygen, "Oxygen Level Prediction Model"
    )
    save_model(model_oxygen, "oxygen_model.pkl")
    
    # Train Number of People model
    model_people, metrics_people = train_and_evaluate_model(
        X, y_people, "Number of People Prediction Model"
    )
    save_model(model_people, "people_model.pkl")
    
    # Save feature information
    feature_info = {
        'feature_columns': FEATURE_COLS,
        'target_oxygen': TARGET_OXYGEN,
        'target_people': TARGET_PEOPLE,
        'metrics_oxygen': metrics_oxygen,
        'metrics_people': metrics_people
    }
    
    import json
    with open(os.path.join(MODELS_DIR, 'model_info.json'), 'w') as f:
        json.dump(feature_info, f, indent=2)
    
    print("\n" + "="*60)
    print("PHASE 2 COMPLETED SUCCESSFULLY!")
    print("="*60)
    print("\nSummary:")
    print(f"  • Trained 2 models (Oxygen Level & Number of People)")
    print(f"  • Models saved in '{MODELS_DIR}' directory")
    print(f"  • Oxygen Model R² Score: {metrics_oxygen['test_r2']:.4f}")
    print(f"  • People Model R² Score: {metrics_people['test_r2']:.4f}")

if __name__ == "__main__":
    main()

