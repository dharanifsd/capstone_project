"""
Phase 3: Backend Logic - FastAPI Backend
REST API for predicting Oxygen Level and Number of People
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List
import pandas as pd
import joblib
import os
from glob import glob

# Initialize FastAPI app
app = FastAPI(
    title="Green Skills AI - Location Safety Predictor API",
    description="API for predicting oxygen levels and optimal people count in tourist locations",
    version="1.0.0"
)

# Enable CORS for frontend/mobile integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Constants
DATASETS_DIR = "Datasets"
MODELS_DIR = "models"

# Feature columns (must match training)
FEATURE_COLS = [
    'Altitude', 'Pressure', 'Temperature', 'Humidity', 'WindSpeed',
    'CO2', 'PM2.5', 'NDVI', 'PopulationDensity'
]

# Load models at startup
print("Loading models...")
try:
    oxygen_model = joblib.load(os.path.join(MODELS_DIR, "oxygen_model.pkl"))
    people_model = joblib.load(os.path.join(MODELS_DIR, "people_model.pkl"))
    print("✓ Models loaded successfully")
except Exception as e:
    print(f"✗ Error loading models: {e}")
    oxygen_model = None
    people_model = None

# Pydantic models for request/response
class PredictionInput(BaseModel):
    """Input model for predictions"""
    location: str
    altitude: Optional[float] = None
    pressure: Optional[float] = None
    temperature: Optional[float] = None
    humidity: Optional[float] = None
    wind_speed: Optional[float] = None
    co2: Optional[float] = None
    pm25: Optional[float] = None
    ndvi: Optional[float] = None
    population_density: Optional[float] = None

class PredictionOutput(BaseModel):
    """Output model for predictions"""
    location: str
    predicted_oxygen_level: float
    predicted_number_of_people: int
    input_features: dict
    health_status: str

class LocationInfo(BaseModel):
    """Location information"""
    name: str
    available: bool
    default_oxygen: Optional[float] = None
    default_features: Optional[dict] = None

def get_available_locations():
    """Get list of available locations from datasets"""
    csv_files = glob(os.path.join(DATASETS_DIR, "*.csv"))
    locations = []
    for file in csv_files:
        name = os.path.basename(file).replace("_dataset.csv", "").replace("_dataset_updated.csv", "")
        locations.append(name)
    return sorted(locations)

def get_location_data(location_name: str):
    """
    Get dataset for a specific location
    Returns mean values for all features
    """
    # Find the matching file
    csv_files = glob(os.path.join(DATASETS_DIR, "*.csv"))
    location_file = None
    
    for file in csv_files:
        name = os.path.basename(file).replace("_dataset.csv", "").replace("_dataset_updated.csv", "")
        if name.lower() == location_name.lower():
            location_file = file
            break
    
    if location_file is None:
        raise ValueError(f"Location '{location_name}' not found")
    
    # Load and return mean values
    df = pd.read_csv(location_file)
    
    # Get mean values for features
    location_features = {}
    for col in FEATURE_COLS:
        if col in df.columns:
            location_features[col] = float(df[col].mean())
        else:
            location_features[col] = None
    
    # Get default oxygen if available
    default_oxygen = None
    if 'Oxygen Level' in df.columns:
        default_oxygen = float(df['Oxygen Level'].mean())
    
    return location_features, default_oxygen

def get_health_status(oxygen_level: float) -> str:
    """Determine health status based on oxygen level"""
    if oxygen_level >= 21.0:
        return "Excellent - Optimal air quality"
    elif oxygen_level >= 20.0:
        return "Good - Normal air quality"
    elif oxygen_level >= 19.0:
        return "Fair - Slightly low oxygen, moderate activity recommended"
    elif oxygen_level >= 18.0:
        return "Poor - Low oxygen, avoid strenuous activity"
    else:
        return "Critical - Very low oxygen, seek medical attention"

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Green Skills AI - Location Safety Predictor API",
        "version": "1.0.0",
        "endpoints": {
            "locations": "/locations",
            "location_info": "/locations/{location_name}",
            "predict": "/predict"
        }
    }

@app.get("/locations")
async def get_locations():
    """Get list of all available locations"""
    locations = get_available_locations()
    return {
        "total_locations": len(locations),
        "locations": locations
    }

@app.get("/locations/{location_name}")
async def get_location_details(location_name: str):
    """Get default parameters for a specific location"""
    try:
        features, default_oxygen = get_location_data(location_name)
        return {
            "location": location_name,
            "default_oxygen": default_oxygen,
            "default_features": features,
            "available": True
        }
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@app.post("/predict", response_model=PredictionOutput)
async def predict(input_data: PredictionInput):
    """
    Make predictions for oxygen level and number of people
    
    You can either:
    1. Just provide location (uses default parameters)
    2. Provide location + custom parameters (overrides defaults)
    """
    if oxygen_model is None or people_model is None:
        raise HTTPException(
            status_code=500, 
            detail="Models not loaded. Please run train_models.py first."
        )
    
    try:
        # Get location defaults
        location_features, _ = get_location_data(input_data.location)
        
        # Prepare feature values (use custom if provided, otherwise use defaults)
        feature_values = {}
        feature_mapping = {
            'altitude': 'Altitude',
            'pressure': 'Pressure',
            'temperature': 'Temperature',
            'humidity': 'Humidity',
            'wind_speed': 'WindSpeed',
            'co2': 'CO2',
            'pm25': 'PM2.5',
            'ndvi': 'NDVI',
            'population_density': 'PopulationDensity'
        }
        
        for param, col in feature_mapping.items():
            value = getattr(input_data, param)
            if value is not None:
                feature_values[col] = value
            elif location_features.get(col) is not None:
                feature_values[col] = location_features[col]
            else:
                raise HTTPException(
                    status_code=400,
                    detail=f"Missing required parameter: {col}. Please provide default values."
                )
        
        # Convert to feature array in correct order
        X = [[feature_values[col] for col in FEATURE_COLS]]
        
        # Make predictions
        predicted_oxygen = float(oxygen_model.predict(X)[0])
        predicted_people = int(people_model.predict(X)[0])
        
        # Ensure people count is positive
        predicted_people = max(1, predicted_people)
        
        # Get health status
        health_status = get_health_status(predicted_oxygen)
        
        return PredictionOutput(
            location=input_data.location,
            predicted_oxygen_level=round(predicted_oxygen, 4),
            predicted_number_of_people=predicted_people,
            input_features=feature_values,
            health_status=health_status
        )
        
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction error: {str(e)}")

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "models_loaded": oxygen_model is not None and people_model is not None
    }

if __name__ == "__main__":
    import uvicorn
    print("\n" + "="*60)
    print("Starting Green Skills AI API Server...")
    print("="*60)
    print("API Documentation: http://localhost:8000/docs")
    print("API Endpoints: http://localhost:8000")
    print("="*60 + "\n")
    
    uvicorn.run(app, host="0.0.0.0", port=8000)

