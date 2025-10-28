"""
Test script for the FastAPI backend
"""
import requests
import json
import time

BASE_URL = "http://localhost:8000"

def test_endpoints():
    """Test all API endpoints"""
    print("="*60)
    print("TESTING FASTAPI BACKEND")
    print("="*60)
    
    # Wait for server to start
    print("\nWaiting for server to start...")
    time.sleep(3)
    
    # Test 1: Root endpoint
    print("\n1. Testing root endpoint...")
    try:
        response = requests.get(BASE_URL)
        print(f"   Status: {response.status_code}")
        print(f"   Response: {json.dumps(response.json(), indent=2)}")
    except Exception as e:
        print(f"   Error: {e}")
        return
    
    # Test 2: Health check
    print("\n2. Testing health check...")
    try:
        response = requests.get(f"{BASE_URL}/health")
        print(f"   Status: {response.status_code}")
        print(f"   Response: {json.dumps(response.json(), indent=2)}")
    except Exception as e:
        print(f"   Error: {e}")
    
    # Test 3: Get locations
    print("\n3. Testing get locations...")
    try:
        response = requests.get(f"{BASE_URL}/locations")
        print(f"   Status: {response.status_code}")
        data = response.json()
        print(f"   Total locations: {data['total_locations']}")
        print(f"   Locations: {', '.join(data['locations'][:5])}...")
    except Exception as e:
        print(f"   Error: {e}")
    
    # Test 4: Get location details
    print("\n4. Testing get location details (Ooty)...")
    try:
        response = requests.get(f"{BASE_URL}/locations/ooty")
        print(f"   Status: {response.status_code}")
        print(f"   Response: {json.dumps(response.json(), indent=2)}")
    except Exception as e:
        print(f"   Error: {e}")
    
    # Test 5: Make prediction (location only)
    print("\n5. Testing prediction (location only)...")
    try:
        payload = {"location": "ooty"}
        response = requests.post(f"{BASE_URL}/predict", json=payload)
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"   Location: {data['location']}")
            print(f"   Predicted Oxygen Level: {data['predicted_oxygen_level']}")
            print(f"   Predicted Number of People: {data['predicted_number_of_people']}")
            print(f"   Health Status: {data['health_status']}")
        else:
            print(f"   Error: {response.text}")
    except Exception as e:
        print(f"   Error: {e}")
    
    # Test 6: Make prediction (with custom parameters)
    print("\n6. Testing prediction (with custom parameters)...")
    try:
        payload = {
            "location": "ooty",
            "temperature": 18.0,
            "humidity": 60.0,
            "wind_speed": 10.0
        }
        response = requests.post(f"{BASE_URL}/predict", json=payload)
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"   Predicted Oxygen Level: {data['predicted_oxygen_level']}")
            print(f"   Predicted Number of People: {data['predicted_number_of_people']}")
        else:
            print(f"   Error: {response.text}")
    except Exception as e:
        print(f"   Error: {e}")
    
    print("\n" + "="*60)
    print("TESTING COMPLETE")
    print("="*60)

if __name__ == "__main__":
    test_endpoints()

