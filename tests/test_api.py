import requests
import json

BASE_URL = "http://localhost:8000"

def test_api():
    print("🧪 Testing User Behavior Analysis API")
    print("=" * 50)
    
    print("\n1. Testing root endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/")
        if response.status_code == 200:
            print("✅ Root endpoint works")
            print(f"   Response: {response.json()['message']}")
        else:
            print(f"❌ Error: {response.status_code}")
    except Exception as e:
        print(f"❌ Connection error: {e}")
        return
    
    print("\n2. Testing health check...")
    try:
        response = requests.get(f"{BASE_URL}/health")
        if response.status_code == 200:
            print("✅ Health check passed")
        else:
            print(f"❌ Error: {response.status_code}")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    print("\n3. Testing users list...")
    try:
        response = requests.get(f"{BASE_URL}/users")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Found {data['total_users']} users")
            if data['users']:
                first_user = data['users'][0]
                print(f"   First user: {first_user['name']} ({first_user['email']})")
        else:
            print(f"❌ Error: {response.status_code}")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    print("\n4. Testing user interests...")
    try:
        test_user_id = "e15b0045-0001-4555-af6a-78a5530feca4"
        response = requests.get(f"{BASE_URL}/interests/{test_user_id}")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ User interests for {test_user_id} received")
            print(f"   Total interactions: {data['total_interactions']}")
            print(f"   Top tags: {len(data['top_tags'])}")
            print(f"   Top tools: {len(data['top_tools'])}")
            
            if data['top_tags']:
                print(f"   Most popular tag: {list(data['top_tags'][0].keys())[0]}")
            if data['top_tools']:
                print(f"   Most popular tool: {list(data['top_tools'][0].keys())[0]}")
        else:
            print(f"❌ Error: {response.status_code}")
            print(f"   Details: {response.text}")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    print("\n5. Testing detailed information...")
    try:
        test_user_id = "e15b0045-0001-4555-af6a-78a5530feca4"
        response = requests.get(f"{BASE_URL}/interests/{test_user_id}/detailed")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Detailed information received")
            print(f"   User: {data['name']} ({data['email']})")
            print(f"   Total interests: {len(data['all_interests'])}")
        else:
            print(f"❌ Error: {response.status_code}")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    print("\n6. Testing analytics...")
    try:
        response = requests.get(f"{BASE_URL}/analytics/summary")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Analytics received")
            print(f"   Total users: {data['total_users']}")
            print(f"   Total events: {data['total_events']}")
            print(f"   Average events per user: {data['average_events_per_user']}")
        else:
            print(f"❌ Error: {response.status_code}")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    print("\n" + "=" * 50)
    print("🎉 Testing completed!")

if __name__ == "__main__":
    test_api()
