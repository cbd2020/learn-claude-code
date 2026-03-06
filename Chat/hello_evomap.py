import json
import uuid
import datetime
import urllib.request
import urllib.error
import os

CONFIG_FILE = "evomap_config.json"

def load_config():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r") as f:
            return json.load(f)
    return {}

def save_config(config):
    with open(CONFIG_FILE, "w") as f:
        json.dump(config, f, indent=2)

config = load_config()

# Use existing node_id or generate a new one
if "node_id" not in config:
    config["node_id"] = f"node_{uuid.uuid4().hex[:16]}"
    print(f"Generated new node_id: {config['node_id']}")
    save_config(config)

if "device_id" not in config:
    config["device_id"] = str(uuid.uuid4())
    save_config(config)

envelope = {
    "protocol": "gep-a2a",
    "protocol_version": "1.0.0",
    "message_type": "hello",
    "message_id": f"msg_{int(datetime.datetime.now(datetime.timezone.utc).timestamp())}_{uuid.uuid4().hex[:8]}",
    "sender_id": config["node_id"],
    "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat().replace("+00:00", "Z"),
    "payload": {
        "name": "My Agent",
        "capabilities": {
            "code_review": True,
            "debugging": True
        },
        "device_id": config["device_id"]
    }
}

try:
    print(f"Sending hello to EvoMap with node_id: {config['node_id']}")
    req = urllib.request.Request(
        "https://evomap.ai/a2a/hello",
        data=json.dumps(envelope).encode('utf-8'),
        headers={"Content-Type": "application/json"},
        method='POST'
    )
    with urllib.request.urlopen(req) as response:
        print(f"Response Status: {response.getcode()}")
        response_data = json.loads(response.read().decode('utf-8'))
        
        # Extract node_secret from response
        if "payload" in response_data and "node_secret" in response_data["payload"]:
            config["node_secret"] = response_data["payload"]["node_secret"]
            save_config(config)
            print(f"✅ Successfully registered! Saved 'node_id' and 'node_secret' to {CONFIG_FILE}")
        else:
            print("⚠️ Warning: response did not contain 'node_secret'.")
            
except urllib.error.HTTPError as e:
    print(f"\nHTTP Error {e.code}: {e.reason}")
    print(e.read().decode('utf-8'))
except Exception as e:
    print(f"Error: {e}")



\\https://evomap.ai/a2a/hello