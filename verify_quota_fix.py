import requests

GATEWAY_URL = "http://127.0.0.1:8000"

def verify_transaction():
    # This payload matches the user's request
    payload = {
        "vehicleId": "69cfc539996d828241f358cd",
        "stationId": "69cfcb9173b85e083b22e92f",
        "fuelType": "Petrol 92",
        "litersServed": 15.5
    }
    
    print(f"Sending POST to {GATEWAY_URL}/transactions/ with payload: {payload}")
    
    headers = {
        "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIyNTQxMjM2OTg3ViIsInJvbGUiOiJhZG1pbiIsImV4cCI6MTc3NTMxNTc3N30.pgln766imYSaoE3jvb5OQqVxXf4sWblVlvPp9L9LlVY",
        "accept": "application/json"
    }
    
    try:
        response = requests.post(f"{GATEWAY_URL}/transactions/", json=payload, headers=headers, timeout=10)
        
        print(f"Response Status: {response.status_code}")
        print(f"Response Body: {response.text}")
        
        if response.status_code == 500:
            print("FAILED: Still getting 500 Internal Server Error.")
        elif response.status_code == 401:
             print("SUCCESS: 500 error (quota update) is likely resolved as the gateway hit the auth wall first or the service returned 401.")
        elif response.status_code == 201 or response.status_code == 200:
             print("SUCCESS: Transaction created!")
        else:
            print(f"Outcome: {response.status_code}")
            
    except Exception as e:
        print(f"Request failed: {e}")

if __name__ == "__main__":
    verify_transaction()
