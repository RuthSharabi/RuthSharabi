import requests

def send_to_react(direction, status):
    url = "http://localhost:3000/update-map"  # כתובת השרת שלך

    data = {
        "direction": direction,
        "detections": status
    }

    try:
        response = requests.post(url, json=data)
        response.raise_for_status()
        print(f"✅ Data sent to map: {data}")
    except requests.exceptions.RequestException as e:
        print(f"❌ Failed to send data to map: {e}")
