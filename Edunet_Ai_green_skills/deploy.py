"""
Deployment Helper Script
Guide users through deployment process
"""

import os
import sys

def print_header(text):
    print("\n" + "="*60)
    print(text)
    print("="*60)

def check_dependencies():
    """Check if required tools are installed"""
    print_header("🔍 Checking Dependencies")
    
    tools = {
        'docker': 'docker --version',
        'docker-compose': 'docker-compose --version',
        'git': 'git --version'
    }
    
    installed = []
    missing = []
    
    for tool, command in tools.items():
        try:
            import subprocess
            result = subprocess.run(command.split(), capture_output=True, timeout=5)
            if result.returncode == 0:
                installed.append(tool)
                print(f"✓ {tool} is installed")
            else:
                missing.append(tool)
                print(f"✗ {tool} is not installed")
        except:
            missing.append(tool)
            print(f"✗ {tool} is not installed")
    
    return installed, missing

def docker_deployment():
    """Guide through Docker deployment"""
    print_header("🐳 Docker Deployment")
    
    print("\nStep 1: Build and start containers")
    print("Command: docker-compose up -d")
    print("\nThis will:")
    print("  • Build API and UI containers")
    print("  • Start both services")
    print("  • Make them available at:")
    print("    - API: http://localhost:8000")
    print("    - UI: http://localhost:8501")
    
    response = input("\nProceed with Docker deployment? (y/n): ")
    if response.lower() == 'y':
        os.system('docker-compose up -d')
        print("\n✓ Deployment started!")
        print("\nTo view logs: docker-compose logs -f")
        print("To stop: docker-compose down")

def cloud_deployment():
    """Guide through cloud deployment"""
    print_header("☁️ Cloud Deployment Options")
    
    options = {
        '1': 'Render.com (Free tier available)',
        '2': 'Railway.app (Free tier available)',
        '3': 'Heroku',
        '4': 'Docker Hub → Deploy anywhere',
    }
    
    print("\nAvailable platforms:")
    for key, value in options.items():
        print(f"  {key}. {value}")
    
    choice = input("\nSelect deployment platform (1-4): ")
    
    if choice == '1':
        render_deployment()
    elif choice == '2':
        railway_deployment()
    elif choice == '3':
        heroku_deployment()
    elif choice == '4':
        dockerhub_deployment()
    else:
        print("Invalid choice")

def render_deployment():
    """Render.com deployment guide"""
    print_header("🚀 Render.com Deployment")
    
    print("\nSteps to deploy on Render:")
    print("\n1. Push code to GitHub")
    print("   git init")
    print("   git add .")
    print("   git commit -m 'Initial commit'")
    print("   git push origin main")
    
    print("\n2. Go to https://render.com")
    print("   • Sign up/Login with GitHub")
    print("   • Click 'New Web Service'")
    print("   • Connect your repository")
    
    print("\n3. For API Backend:")
    print("   • Build Command: pip install -r requirements.txt")
    print("   • Start Command: python start_server.py")
    print("   • Environment: Python 3")
    print("   • Health Path: /health")
    
    print("\n4. For UI (separate service):")
    print("   • Build Command: pip install -r requirements.txt")
    print("   • Start Command: streamlit run app.py --server.port=$PORT")
    print("   • Environment Variable: API_BASE_URL=<your-api-url>")
    
    print("\n✓ Render.yaml is already configured in your project!")

def railway_deployment():
    """Railway.app deployment guide"""
    print_header("🚂 Railway.app Deployment")
    
    print("\nSteps to deploy on Railway:")
    print("\n1. Push code to GitHub")
    print("   git init")
    print("   git add .")
    print("   git commit -m 'Initial commit'")
    print("   git push origin main")
    
    print("\n2. Go to https://railway.app")
    print("   • Sign up/Login with GitHub")
    print("   • Click 'New Project' → 'Deploy from GitHub repo'")
    print("   • Select your repository")
    
    print("\n3. Railway will auto-detect railway.json")
    print("   • Add environment variable:")
    print("     API_BASE_URL=<your-deployed-api-url>")
    
    print("\n4. Add another service for UI:")
    print("   • Add Streamlit service")
    print("   • Set command: streamlit run app.py")
    print("   • Set API_BASE_URL env var")
    
    print("\n✓ railway.json is already configured in your project!")

def heroku_deployment():
    """Heroku deployment guide"""
    print_header("🟣 Heroku Deployment")
    
    print("\nSteps to deploy on Heroku:")
    print("\n1. Install Heroku CLI: https://devcenter.heroku.com/articles/heroku-cli")
    
    print("\n2. Login and create app:")
    print("   heroku login")
    print("   heroku create green-skills-api")
    
    print("\n3. Deploy:")
    print("   git add .")
    print("   git commit -m 'Deploy to Heroku'")
    print("   git push heroku main")
    
    print("\n4. Check logs:")
    print("   heroku logs --tail")
    
    print("\n✓ Procfile and runtime.txt are already configured!")

def dockerhub_deployment():
    """Docker Hub deployment guide"""
    print_header("🐳 Docker Hub Deployment")
    
    print("\nSteps to deploy to Docker Hub:")
    print("\n1. Build images:")
    print("   docker build -t your-username/green-skills-api .")
    print("   docker build -f Dockerfile.ui -t your-username/green-skills-ui .")
    
    print("\n2. Push to Docker Hub:")
    print("   docker login")
    print("   docker push your-username/green-skills-api")
    print("   docker push your-username/green-skills-ui")
    
    print("\n3. Deploy anywhere:")
    print("   docker run -d -p 8000:8000 your-username/green-skills-api")
    print("   docker run -d -p 8501:8501 your-username/green-skills-ui")

def main():
    print_header("🌿 Green Skills AI - Deployment Helper")
    
    print("\nDeployment Options:")
    print("  1. Docker (Local/Server)")
    print("  2. Cloud Platform (Render/Railway/Heroku)")
    print("  3. View deployment documentation")
    print("  4. Exit")
    
    choice = input("\nSelect option (1-4): ")
    
    if choice == '1':
        installed, missing = check_dependencies()
        if 'docker' in missing:
            print("\n⚠️ Docker is required for this deployment.")
            print("Install from: https://www.docker.com/get-started")
        else:
            docker_deployment()
    
    elif choice == '2':
        cloud_deployment()
    
    elif choice == '3':
        print_header("📖 Documentation")
        print("\nAvailable guides:")
        print("  • DEPLOYMENT.md - Comprehensive deployment guide")
        print("  • USAGE.md - User guide")
        print("  • README.md - Project overview")
        print("\nOpening DEPLOYMENT.md...")
        os.system('cat DEPLOYMENT.md | more' if sys.platform != 'win32' else 'type DEPLOYMENT.md | more')
    
    elif choice == '4':
        print("\nGoodbye! 👋")
    
    else:
        print("\nInvalid choice")

if __name__ == "__main__":
    main()

