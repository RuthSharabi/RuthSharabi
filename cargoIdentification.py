import cv2
import os
from ultralytics import YOLO

# נתיב למודל
model_path = "C:/explosives-detection-training-main/explosives-detection-training-main/YOLO/runs/detect/train12/weights/best.pt"

# טעינת המודל פעם אחת בלבד
if not os.path.isfile(model_path):
    raise FileNotFoundError("⚠️ קובץ המודל לא נמצא בנתיב שציינת!")

try:
    model = YOLO(model_path)
except Exception as e:
    raise RuntimeError(f"שגיאה בטעינת המודל: {e}")

# 🔍 הפונקציה שנקראת מהקוד הראשי
def detect_explosives(frame):
    """
    מזהה מטענים בתמונה (פריים) ומחזירה True אם זוהה לפחות אחד.
    אפשר גם להחזיר רשימת מיקומים או שמות אם נרצה פירוט.
    """
    results = model(frame)
    explosives_found = []

    for result in results:
        if not result.boxes:
            continue

        for box in result.boxes:
            cls = int(box.cls[0].item())
            label = model.names[cls]
            conf = box.conf[0].item()

            if label.lower() == "cargo" and conf > 0.3:
                explosives_found.append({
                    "label": label,
                    "confidence": conf
                })

    return explosives_found  # אפשר גם להחזיר True/False אם רוצים פשטות
