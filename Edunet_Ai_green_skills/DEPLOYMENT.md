# Deployment Guide - Green Skills AI

## 📋 Deployment Options

This project can be deployed using multiple platforms. Choose the one that best fits your needs.

---

## 🐳 Option 1: Docker Deployment (Recommended for Production)

### Prerequisites
- Docker installed
- Docker Compose installed

### Steps

#### 1. Build and Run with Docker Compose
```bash
# Build and start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

The application will be available at:
- **API**: http://localhost:8000
- **UI**: http://localhost:8501

#### 2. Docker Commands
```bash
# Build API image only
docker build -t green-skills-api .

# Run API container
docker run -d -p 8000:8000 green-skills-api

# Build UI image
docker build -f Dockerfile.ui -t green-skills-ui .

# Run UI container
docker run -d -p 8501:8501 green-skills-ui
```

---

## ☁️ Option 2: Cloud Deployment

### A. Render.com (Free Tier Available)

#### Deploy API
1. Go to [Render.com](https://render.com)
2. Create a new "Web Service"
3. Connect your GitHub repository
4. Use these settings:
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `python start_server.py`
   - **Environment**: Python 3
5. Render will auto-detect `render.yaml` configuration

#### Deploy Streamlit UI
1. Create a new "Web Service" for Streamlit
2. Use these settings:
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `streamlit run app.py --server.port=$PORT`
   - **Environment Variable**: `API_BASE_URL=<your-api-url>`

### B. Railway.app

1. Go to [Railway.app](https://railway.app)
2. Click "New Project" → "Deploy from GitHub repo"
3. Railway will auto-detect `railway.json`
4. Set environment variable:
   - `API_BASE_URL` = your deployed API URL

### C. Heroku

#### 1. Create Procfile
```bash
echo "web: python start_server.py" > Procfile
```

#### 2. Create runtime.txt
```bash
echo "python-3.11.0" > runtime.txt
```

#### 3. Deploy
```bash
heroku create green-skills-api
git push heroku main
```

### D. AWS EC2

#### 1. Launch EC2 Instance
```bash
# Connect to instance
ssh -i your-key.pem ubuntu@your-ec2-ip

# Install dependencies
sudo apt update
sudo apt install python3-pip -y

# Clone repository
git clone <your-repo-url>
cd Edunet_Ai_green_skills

# Install Python packages
pip3 install -r requirements.txt

# Run with screen or tmux
screen -S api
python3 start_server.py
# Press Ctrl+A then D to detach
```

#### 2. Use Nginx as Reverse Proxy
```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

### E. Streamlit Cloud

1. Push your code to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Sign in with GitHub
4. Select your repository
5. Set environment variables:
   - `API_BASE_URL`: Your deployed API URL
6. Deploy!

---

## 📱 Option 3: Mobile App Deployment

### Streamlit Mobile (Progressive Web App)

Your Streamlit app can work as a PWA:

1. Deploy to Streamlit Cloud
2. Add to home screen on mobile
3. Works offline with caching

### React Native / Flutter Integration

Use the API with mobile frameworks:

1. Deploy API to cloud (Render/Railway/AWS)
2. Create mobile app using:
   - React Native + Axios
   - Flutter + HTTP package
3. Call API endpoints:
   ```javascript
   // React Native example
   const response = await fetch('https://your-api-url/predict', {
     method: 'POST',
     headers: {'Content-Type': 'application/json'},
     body: JSON.stringify({location: 'ooty'})
   });
   const data = await response.json();
   ```

---

## 🌐 Option 4: Full Stack Deployment Architecture

### Recommended Setup

```
┌─────────────────┐
│  Cloudflare CDN │
│   (Frontend)    │
└────────┬────────┘
         │
┌────────▼────────┐
│  Streamlit UI   │
│  (Streamlit     │
│   Cloud / VPS)  │
└────────┬────────┘
         │
┌────────▼────────┐
│  FastAPI Backend│
│  (Render / AWS) │
└────────┬────────┘
         │
┌────────▼────────┐
│   ML Models     │
│  (S3 / Storage) │
└─────────────────┘
```

### Environment Variables
```bash
# API Server
API_BASE_URL=https://your-api.com
PORT=8000
PYTHON_ENV=production

# For Streamlit UI
API_BASE_URL=https://your-api.com

# Optional: Database
DATABASE_URL=postgresql://...
```

---

## 🔒 Security Considerations

### 1. HTTPS Setup
- Use Let's Encrypt for free SSL
- Configure domain with HTTPS

### 2. CORS Configuration
```python
# In api.py - already configured
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://yourdomain.com"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### 3. Rate Limiting
```bash
pip install slowapi
```

```python
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter

@app.post("/predict")
@limiter.limit("5/minute")
async def predict(...):
    ...
```

### 4. API Keys (Optional)
```python
API_KEY = os.getenv("API_KEY")

@app.post("/predict")
async def predict(request: Request, ...):
    if request.headers.get("X-API-Key") != API_KEY:
        raise HTTPException(401, "Invalid API Key")
    ...
```

---

## 📊 Monitoring & Logging

### Health Checks
```bash
# Check API health
curl http://your-api.com/health

# Expected response:
{"status": "healthy", "models_loaded": true}
```

### Logging
```python
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
```

### Metrics
- Use tools like Prometheus for monitoring
- Set up alerts for downtime

---

## 🚀 Quick Deployment Checklist

- [ ] Choose deployment platform
- [ ] Set up repository (GitHub/GitLab)
- [ ] Configure environment variables
- [ ] Deploy API backend
- [ ] Deploy Streamlit UI
- [ ] Test all endpoints
- [ ] Set up custom domain (optional)
- [ ] Configure SSL/HTTPS
- [ ] Set up monitoring
- [ ] Test mobile responsiveness
- [ ] Document API endpoints
- [ ] Create user guide

---

## 🆘 Troubleshooting

### API not connecting
- Check API server is running
- Verify CORS settings
- Check firewall/security groups
- Test with curl: `curl http://localhost:8000/health`

### Models not loading
- Verify model files exist in `models/` directory
- Check file permissions
- Verify paths are correct

### Streamlit not connecting to API
- Set correct `API_BASE_URL` environment variable
- Check network connectivity
- Verify API is publicly accessible

---

## 📞 Support

For issues during deployment:
1. Check logs: `docker-compose logs`
2. Verify environment variables
3. Test API endpoints manually
4. Review error messages in console

---

**Ready to deploy! 🚀**

Choose your platform and follow the instructions above.

