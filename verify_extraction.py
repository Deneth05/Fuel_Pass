import requests
import time

def test_endpoint(url, method="GET", json=None, headers=None):
    try:
        if method == "GET":
            response = requests.get(url, headers=headers)
        elif method == "POST":
            response = requests.post(url, json=json, headers=headers)
        elif method == "PUT":
            response = requests.put(url, json=json, headers=headers)
        elif method == "DELETE":
            response = requests.delete(url, headers=headers)
        
        print(f"{method} {url} - Status: {response.status_code}")
        if response.status_code < 300:
            return response.json()
        else:
            print(f"Error: {response.text}")
            return None
    except Exception as e:
        print(f"Connection failed: {e}")
        return None

def main():
    # Note: These URLs assume the services are running.
    # In this environment, we might not be able to start them easily,
    # but we can check if the gateway is still running and routing to the new port.
    
    GATEWAY_URL = "http://localhost:8000"
    QUOTA_SERVICE_URL = "http://localhost:8006"
    
    print("--- Testing Quota Service Direct ---")
    root = test_endpoint(f"{QUOTA_SERVICE_URL}/")
    if root:
        print(f"Quota Service Root: {root}")
    
    print("\n--- Testing Gateway Routing to Quota Service ---")
    # This might fail if the user hasn't restarted the gateway or started the new service.
    # But it shows what we intended.
    quotas = test_endpoint(f"{GATEWAY_URL}/quotas")
    if quotas:
         print(f"Quotas from Gateway: {len(quotas)} items")

if __name__ == "__main__":
    main()
