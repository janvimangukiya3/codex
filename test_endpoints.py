"""
Quick test script to verify all API endpoints are working
"""
import requests
import json

BASE_URL = "http://127.0.0.1:5000"

print("=" * 60)
print("TESTING ALL API ENDPOINTS")
print("=" * 60)

# Test chart endpoints
chart_endpoints = [
    '/api/charts/delivery-time-distribution',
    '/api/charts/distance-vs-time',
    '/api/charts/rating-impact',
    '/api/charts/vehicle-comparison',
    '/api/charts/order-type-analysis',
    '/api/charts/age-performance'
]

print("\n1. Testing Chart Endpoints:")
for endpoint in chart_endpoints:
    try:
        response = requests.get(BASE_URL + endpoint, timeout=5)
        if response.status_code == 200:
            print(f"   ✓ {endpoint} - OK")
        else:
            print(f"   ✗ {endpoint} - Failed (Status: {response.status_code})")
    except Exception as e:
        print(f"   ✗ {endpoint} - Error: {str(e)}")

# Test prediction endpoint
print("\n2. Testing Prediction Endpoint:")
test_data = {
    "age": 30,
    "rating": 4.5,
    "distance": 10.5,
    "vehicle": 2,
    "order": 1
}

try:
    response = requests.post(
        BASE_URL + '/api/predict',
        json=test_data,
        headers={'Content-Type': 'application/json'},
        timeout=5
    )
    if response.status_code == 200:
        result = response.json()
        print(f"   ✓ Prediction API - OK")
        print(f"   Predicted Time: {result.get('prediction')} minutes")
    else:
        print(f"   ✗ Prediction API - Failed (Status: {response.status_code})")
except Exception as e:
    print(f"   ✗ Prediction API - Error: {str(e)}")

# Test page endpoints
print("\n3. Testing Page Endpoints:")
page_endpoints = ['/', '/predict-page', '/analytics', '/about']

for endpoint in page_endpoints:
    try:
        response = requests.get(BASE_URL + endpoint, timeout=5)
        if response.status_code == 200:
            print(f"   ✓ {endpoint} - OK")
        else:
            print(f"   ✗ {endpoint} - Failed (Status: {response.status_code})")
    except Exception as e:
        print(f"   ✗ {endpoint} - Error: {str(e)}")

print("\n" + "=" * 60)
print("TESTING COMPLETED")
print("=" * 60)
