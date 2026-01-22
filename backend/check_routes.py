import http.client
import json

# Connect to the server
conn = http.client.HTTPConnection('0.0.0.0', 8000)

# Test the root path
try:
    conn.request("GET", "/openapi.json")
    response = conn.getresponse()
    print(f"Status: {response.status}")
    data = response.read()
    print(f"Response: {data.decode('utf-8')[:500]}...")  # Print first 500 chars

    # Parse the response to see available paths
    try:
        openapi_data = json.loads(data.decode('utf-8'))
        print(f"\nAvailable paths:")
        for path in openapi_data.get('paths', {}):
            print(f"  {path}")
    except json.JSONDecodeError:
        print("Could not parse as JSON")

except Exception as e:
    print(f"Error: {e}")
finally:
    conn.close()