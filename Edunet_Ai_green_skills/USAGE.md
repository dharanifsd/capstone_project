# Green Skills AI - Usage Guide

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- All dependencies installed (`pip install -r requirements.txt`)

### Running the Application

#### Step 1: Start the API Server
```bash
python start_server.py
```
The API will start on `http://localhost:8000`

#### Step 2: Start the Streamlit UI
```bash
streamlit run app.py
```
The UI will open automatically in your browser at `http://localhost:8501`

#### Step 3: Use the Application
1. Select a location from the sidebar
2. Adjust environmental parameters (or use defaults)
3. Click "Predict" to get results

## 📁 Project Structure

```
Edunet_Ai_green_skills/
├── Datasets/              # 12 location datasets
├── models/                # Trained ML models
│   ├── oxygen_model.pkl
│   ├── people_model.pkl
│   └── model_info.json
├── api.py                 # FastAPI backend
├── app.py                 # Streamlit UI
├── start_server.py        # API server launcher
├── train_models.py        # Model training script
├── main.py                # Project status
├── requirements.txt       # Dependencies
└── USAGE.md              # This file
```

## 🔧 Development Commands

### Training Models
```bash
python train_models.py
```

### Testing API
```bash
python test_api.py
```

### View Project Status
```bash
python main.py
```

## 📊 API Endpoints

- `GET /` - Root endpoint
- `GET /health` - Health check
- `GET /locations` - List all locations
- `GET /locations/{name}` - Get location details
- `POST /predict` - Make predictions

## 🌐 Access Points

- **Streamlit UI**: http://localhost:8501
- **API Server**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs

## 📝 Notes

- Only 'ooty_dataset_updated.csv' contains Oxygen Level data
- Other locations will use computed predictions
- API server must be running for the UI to work
- Models were trained with R² scores: Oxygen (0.93), People (-0.06)

## 🐛 Troubleshooting

### API not connecting
- Make sure `python start_server.py` is running
- Check that port 8000 is available

### No predictions showing
- Verify models are loaded in `/health` endpoint
- Check that datasets are in `Datasets/` folder

### Module not found errors
```bash
pip install -r requirements.txt
```

