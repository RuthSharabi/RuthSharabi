import cv2
from ultralytics import YOLO
import face_recognition
import os
import winsound
import dlib

predictor_path = "D:/RShProject/codes/shape_predictor_68_face_landmarks.dat"
# face_predictor = dlib.shape_predictor(predictor_path)

wanted_faces = []
wanted_names = []

wanted_folder = r"D:/RShProject/codes/images/wanted_people"
for filename in os.listdir(wanted_folder):
    if filename.endswith((".jpg", ".png", ".jpeg")):
        path = os.path.join(wanted_folder, filename)
        image = face_recognition.load_image_file(path)
        encodings = face_recognition.face_encodings(image)
        if encodings:
            wanted_faces.append(encodings[0])
            wanted_names.append(os.path.splitext(filename)[0])

# טען את מודל YOLO פעם אחת
yolo_model = YOLO('yolov8n.pt')

def detect_human(frame):
    """
    מחזירה רשימה של שמות האנשים שזוהו בתמונה, מתוך המאגר של המבוקשים.
    """
    results = yolo_model(frame)
    yolo_faces = []

    for result in results[0].boxes:
        cls = int(result.cls[0])
        if cls == 0:  # cls == 0 מייצג "אדם" ב־YOLO
            x1, y1, x2, y2 = map(int, result.xyxy[0])
            yolo_faces.append((y1, x2, y2, x1))  # הסדר ש־face_recognition צריך

    detected_names = []

    if yolo_faces:
        face_encodings = face_recognition.face_encodings(frame, yolo_faces)
        for (top, right, bottom, left), face_encoding in zip(yolo_faces, face_encodings):
            matches = face_recognition.compare_faces(wanted_faces, face_encoding, tolerance=0.5)
            if True in matches:
                matched_index = matches.index(True)
                wanted_name = wanted_names[matched_index]
                detected_names.append(wanted_name)
                # ניתן גם להשמיע צליל כאן אם רוצים
                winsound.Beep(1000, 200)

    return detected_names  # רשימה של שמות (או ריקה אם לא זוהה כלום)
