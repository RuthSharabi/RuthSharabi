import requests
import time

url = "http://localhost:5000/updateMap"

# מסלול לדוגמה שהרובוט עובר בו
robot_path = [
    {"x": 0, "y": 0},
    {"x": 1, "y": 0},
    {"x": 2, "y": 0},
    {"x": 2, "y": 1},
    {"x": 2, "y": 2}
]

# זיהויים לדוגמה
detections = [
    {"x": 2, "y": 0, "type": "obstacle", "label": "מכשול"},
    {"x": 2, "y": 1, "type": "explosive", "label": "מטען חבלה"},
    {"x": 2, "y": 2, "type": "person", "label": "חשוד"}
]

# שילוב ושליחה לשרת
full_data = robot_path + detections

response = requests.post(url, json=full_data)

if response.status_code == 200:
    print("✅ נשלח בהצלחה!")
else:
    print("❌ שגיאה:", response.text)
