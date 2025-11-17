import requests
import time

print("Testing server connection...")
print("=" * 50)

try:
    response = requests.get('http://localhost:5001/health', timeout=5)
    print(f"Status Code: {response.status_code}")
    print(f"Response Text: {response.text}")
    print(f"Response Headers: {response.headers}")
    
    if response.status_code == 200:
        try:
            print(f"JSON Response: {response.json()}")
            print("\n✅ SUCCESS! Server is working correctly!")
        except Exception as e:
            print(f"\n❌ ERROR: Server responded but not with JSON")
            print(f"Error: {e}")
    else:
        print(f"\n❌ ERROR: Server returned status code {response.status_code}")
        
except requests.exceptions.ConnectionError:
    print("\n❌ ERROR: Cannot connect to server!")
    print("Make sure the server is running on port 5001")
    
except requests.exceptions.Timeout:
    print("\n❌ ERROR: Connection timed out!")
    print("Server is not responding")
    
except Exception as e:
    print(f"\n❌ ERROR: {type(e).__name__}: {e}")

print("=" * 50)
input("\nPress Enter to close...")
