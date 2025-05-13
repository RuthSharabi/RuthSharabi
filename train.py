from ultralytics import YOLO
import cv2
# טוען את המודל YOLO שהוכן מראש
#model = YOLO("C:\explosives-detection-training-main\explosives-detection-training-main\wtrained_models\exp_yolo.pt")

model = YOLO("C:/explosives-detection-training-main/explosives-detection-training-main/YOLO/runs/detect/train12/weights/best.pt")

image_path = "D:\RShProject\codes\cargo\cargo1.jpg"
results = model(image_path)
cv2.imread(image_path)
# אימון המודל על התמונות
#model.train(data="dataset.yaml", epochs=5, imgsz=640)

# שמירת המודל המאומן
#model.export(format="onnx")