# Green Skills AI - Project Summary

## 🎯 Project Overview
A machine learning-powered application to predict oxygen levels and optimal crowd capacity in tourist locations based on environmental conditions.

## ✅ Completed Phases

### Phase 1: Data Preparation ✓
- **Datasets**: 12 location datasets collected and organized
- **Locations**: Ooty, Manali, Shimla, Munnar, Kodaikanal, Gulmarg, Nainital, Mussoorie, Chikmagalur, Ponmudi, Valparai, Wagamon
- **Data Structure**: ~1000 rows per location with 10+ features
- **Features**: Altitude, Pressure, Temperature, Humidity, WindSpeed, CO2, PM2.5, NDVI, PopulationDensity

### Phase 2: Model Development ✓
- **Algorithm**: RandomForestRegressor
- **Models Trained**: 
  - Oxygen Level Prediction Model
  - Number of People Prediction Model
- **Performance**:
  - Oxygen Model R² Score: **0.9304** (Excellent)
  - People Model R² Score: -0.0560 (Needs improvement)
- **Feature Importance**: WindSpeed (51.7%), PM2.5 (35.6%) for oxygen prediction

### Phase 3: Backend Logic ✓
- **Framework**: FastAPI REST API
- **Endpoints**:
  - `GET /` - API information
  - `GET /health` - Health check
  - `GET /locations` - List all locations
  - `GET /locations/{name}` - Location details
  - `POST /predict` - Make predictions
- **Features**:
  - Dynamic location loading
  - Parameter override capability
  - Health status determination
  - CORS enabled for mobile integration
  - Auto API documentation at `/docs`

### Phase 4: User Interface ✓
- **Framework**: Streamlit
- **Features**:
  - Beautiful, modern UI with custom CSS
  - Location selector dropdown
  - Parameter adjustment inputs
  - Real-time prediction display
  - Health status with color coding
  - Environmental overview metrics
  - API connection status check
- **User Experience**:
  - Sidebar for inputs
  - Large, readable prediction boxes
  - Expandable sections for details
  - Responsive design

## 📊 Technical Stack
- **Backend**: Python, FastAPI, Uvicorn
- **Frontend**: Streamlit
- **ML**: scikit-learn, RandomForest
- **Data**: pandas, numpy
- **API**: RESTful architecture
- **Deployment**: Local (Ready for cloud deployment)

## 📁 Project Structure
```
Edunet_Ai_green_skills/
├── Datasets/                # 12 location CSV files
│   ├── ooty_dataset_updated.csv (with oxygen data)
│   └── [11 other locations]
├── models/                  # Trained ML models
│   ├── oxygen_model.pkl
│   ├── people_model.pkl
│   └── model_info.json
├── api.py                   # FastAPI backend
├── app.py                   # Streamlit UI
├── start_server.py          # API server launcher
├── train_models.py          # Model training script
├── test_api.py              # API testing script
├── main.py                  # Project status
├── requirements.txt         # Python dependencies
├── USAGE.md                 # Usage guide
├── PROJECT_SUMMARY.md       # This file
└── readme.md                # Original project plan
```

## 🚀 How to Run

### Step 1: Start API Server
```bash
python start_server.py
```
- Server starts on: `http://localhost:8000`
- API docs: `http://localhost:8000/docs`

### Step 2: Start UI
```bash
streamlit run app.py
```
- UI opens at: `http://localhost:8501`

### Step 3: Use the Application
1. Select a location from sidebar
2. Adjust parameters (optional)
3. Click "Predict"
4. View results with health status

## 🔍 Key Features

### 1. Environmental Monitoring
- Real-time oxygen level prediction
- Based on multiple environmental factors
- Health status classification

### 2. Capacity Planning
- Optimal number of people calculation
- Prevents overcrowding
- Air quality optimization

### 3. User-Friendly Interface
- Simple dropdown selection
- Adjustable parameters
- Clear visual feedback
- Color-coded health status

### 4. API-First Design
- RESTful API for mobile integration
- Easy to extend
- Well-documented endpoints
- CORS enabled

## 📈 Model Insights

### Oxygen Level Predictions
- **Top Features**: WindSpeed (51.7%), PM2.5 (35.6%)
- **Accuracy**: 93% R² score
- **Health Thresholds**:
  - Excellent: ≥21%
  - Good: 20-21%
  - Fair: 19-20%
  - Poor: 18-19%
  - Critical: <18%

### People Capacity Predictions
- **Status**: Needs improvement (negative R²)
- **Recommendation**: More training data needed
- **Current**: Provides baseline estimates

## ⚠️ Known Limitations
1. Only Ooty dataset has complete oxygen level data
2. People prediction model needs more data
3. Currently runs locally (Phase 5 for deployment)
4. Single location has full training data

## 🔄 Future Enhancements (Phase 5)
- [ ] Mobile app (Flutter/React Native)
- [ ] Cloud deployment (AWS/Render/Railway)
- [ ] Real-time sensor data integration
- [ ] Historical data visualization
- [ ] Alerts and notifications
- [ ] Multiple model comparison
- [ ] Advanced feature engineering

## 📝 Notes
- Models trained on 1000 rows (Ooty only for oxygen)
- API handles missing oxygen data gracefully
- UI provides default values for all locations
- System designed for easy extension

## 🎓 Learning Outcomes
- End-to-end ML project implementation
- API development with FastAPI
- UI development with Streamlit
- Data preprocessing and model training
- RESTful API design
- Full-stack ML application

---

**Status**: Phases 1-4 Completed ✓
**Next**: Phase 5 - Deployment**
**Date**: Current implementation

