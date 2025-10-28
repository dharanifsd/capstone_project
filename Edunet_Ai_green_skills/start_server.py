"""
Start the FastAPI server
"""
import uvicorn

if __name__ == "__main__":
    print("\n" + "="*60)
    print("Starting Green Skills AI API Server...")
    print("="*60)
    print("API Documentation: http://localhost:8000/docs")
    print("API Endpoints: http://localhost:8000")
    print("Press CTRL+C to stop the server")
    print("="*60 + "\n")
    
    uvicorn.run("api:app", host="0.0.0.0", port=8000, reload=False)

