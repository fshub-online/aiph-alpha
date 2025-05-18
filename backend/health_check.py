import sys
import urllib.request
import json

try:
    with urllib.request.urlopen('http://localhost:8001/health', timeout=3) as response:
        if response.status == 200:
            data = json.load(response)
            if data.get("status") == "healthy" and data.get("database") == "healthy":
                print("Health check passed")
                sys.exit(0) # Healthy
except Exception:
    pass # Fall through to exit with 1
print("Health check failed")
sys.exit(1) # Unhealthy