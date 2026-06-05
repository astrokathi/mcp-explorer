import os
import requests
from dotenv import load_dotenv

load_dotenv()
pk = os.getenv("LANGFUSE_PUBLIC_KEY")
sk = os.getenv("LANGFUSE_SECRET_KEY")

r = requests.get("http://localhost:3000/api/public/traces", auth=(pk, sk))
data = r.json()
if "data" in data and len(data["data"]) > 0:
    print("✅ SUCCESS! Traces found via API:")
    for trace in data["data"][:5]:
        print(f"Trace ID: {trace.get('id')}, Name: {trace.get('name')}, Timestamp: {trace.get('timestamp')}")
else:
    print("❌ No traces found!")
    print(data)
