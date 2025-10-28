# Quick Deployment Guide

## 🚀 Fastest Way to Deploy

### Option 1: Docker (Recommended - 2 minutes)

```bash
# Build and start everything
docker-compose up -d

# Check status
docker-compose ps

# View logs
docker-compose logs -f

# Access the app
# API: http://localhost:8000
# UI: http://localhost:8501
```

### Option 2: Cloud Deployment (5 minutes)

#### For Render.com (Free Tier):

1. **Push to GitHub**:
```bash
git init
git add .
git commit -m "Deploy Green Skills AI"
git branch -M main
git remote add origin YOUR_GITHUB_REPO_URL
git push -u origin main
```

2. **Deploy on Render**:
   - Go to https://render.com
   - Sign up with GitHub
   - Click "New Web Service"
   - Connect your repo
   - Settings:
     - Build Command: `pip install -r requirements.txt`
     - Start Command: `python start_server.py`
     - Add Environment Variable:
       - Key: `PYTHON_VERSION`
       - Value: `3.11.0`

3. **Deploy UI** (separate service):
   - Create another Web Service
   - Same repo, different settings:
     - Start Command: `streamlit run app.py --server.port=$PORT --server.headless=true`
     - Environment Variable:
       - Key: `API_BASE_URL`
       - Value: `<your-api-url>`

#### For Railway.app (Free Tier):

1. **Same GitHub push as above**

2. **Deploy on Railway**:
   - Go to https://railway.app
   - Sign up with GitHub
   - Click "New Project" → "Deploy from GitHub repo"
   - Select your repo
   - Railway auto-detects railway.json ✓
   - Add Environment Variable: `API_BASE_URL=<your-api-url>`

## 🎯 Pre-Deployment Checklist

- [ ] All tests passing locally
- [ ] Models trained (run `python train_models.py`)
- [ ] Git repository initialized
- [ ] Code pushed to GitHub
- [ ] Environment variables documented
- [ ] API_BASE_URL configured for UI

## 🔍 Post-Deployment Verification

### Test API:
```bash
curl https://your-api-url/health
```

Expected response:
```json
{"status": "healthy", "models_loaded": true}
```

### Test Prediction:
```bash
curl -X POST https://your-api-url/predict \
  -H "Content-Type: application/json" \
  -d '{"location": "ooty"}'
```

## 🐛 Common Issues

### Issue: Models not loading
**Solution**: Ensure `models/` directory is included in deployment

### Issue: UI can't connect to API
**Solution**: Set `API_BASE_URL` environment variable correctly

### Issue: Port conflicts
**Solution**: Update ports in docker-compose.yml or platform settings

## 📞 Need Help?

- See [DEPLOYMENT.md](DEPLOYMENT.md) for detailed instructions
- Check API docs: https://your-api-url/docs
- View logs: Check platform logs or `docker-compose logs`

---

**Quick Deploy Command**:
```bash
python deploy.py
```

This helper script will guide you through the process!

