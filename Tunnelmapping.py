import cv2
import json
import ctypes
import os
from IdentifyingObstacles import detect_obstacle
from recogmizePeople import detect_human
from cargoIdentification import detect_explosives
from voiceRecognition import detect_language
from react_interface import send_to_react

# נתיב הסרטון
video_path = "tunnel.mp4"

# --- טען את ספריית ה-DLL ---
try:
    dll_path = os.path.abspath("./decision_logic.dll")
    if not os.path.exists(dll_path):
        raise FileNotFoundError(f"❌ קובץ ה-DLL לא נמצא בנתיב: {dll_path}")
    c_lib = ctypes.CDLL(dll_path)  # נסה לטעון את ה-DLL
    c_lib.get_next_move.restype = ctypes.c_char_p
    c_lib.get_next_move.argtypes = [ctypes.c_char_p]
except FileNotFoundError as fnf_error:
    print(fnf_error)
    exit(1)
except OSError as os_error:
    print(f"❌ שגיאה בטעינת ה-DLL: {os_error}")
    exit(1)

# מצב הרובוט
position = [0, 0]  # X, Y
heading = "right"  # כיוון התקדמות נוכחי

# תרגום כיוון למרחק
direction_map = {
    "right": (1, 0),
    "left": (-1, 0),
    "forward": (0, 1),
    "back": (0, -1)
}


def frame_to_json(data_dict):
    """המר נתוני Python לפורמט JSON כדי לשלוח ל-DLL"""
    return json.dumps(data_dict).encode('utf-8')


def update_position(direction):
    """עדכן את מיקום הרובוט על סמך הכיוון"""
    global position, heading
    if direction in direction_map:
        dx, dy = direction_map[direction]
        position[0] += dx
        position[1] += dy
        heading = direction


def process_video(video_path):
    """פעולה לעיבוד הסרטון ולהפעלת האלגוריתם"""
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print("❌ לא ניתן לפתוח את הסרטון")
        return

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        try:
            # --- שלב 1: ניווט ראשוני על סמך מכשולים בלבד ---
            obstacle_data = detect_obstacle()  # {front, left, right}
            minimal_status = {
                "front": obstacle_data["front"],
                "left": obstacle_data["left"],
                "right": obstacle_data["right"]
            }
            direction = c_lib.get_next_move(frame_to_json(minimal_status)).decode('utf-8')
            update_position(direction)

            # --- שלב 2: ביצוע זיהויים נוספים ---
            enemies = detect_human(frame)
            explosives = detect_explosives(frame)
            language = detect_language()

            full_status = {
                **minimal_status,
                "enemy": enemies,
                "explosive": explosives,
                "language": language
            }

            # --- שלב 3: שליחה שנייה לקובץ C להחלטה עם מידע נוסף ---
            direction = c_lib.get_next_move(frame_to_json(full_status)).decode('utf-8')
            update_position(direction)

            # --- שלב 4: שליחה ל-React למיפוי ---
            send_to_react(
                direction,
                {
                    "position": {"x": position[0], "y": position[1]},
                    "detections": full_status,
                    "direction": direction
                }
            )

            # --- שלב תצוגה אופציונלי ---
            print(f"📍 מיקום: {position} | כיוון: {direction} | זיהויים: {full_status}")

        except Exception as e:
            print(f"❌ שגיאה במהלך עיבוד הפריים: {e}")
            break

    cap.release()
    cv2.destroyAllWindows()


# --- הרצת התוכנית ---
if __name__ == "__main__":
    if not os.path.exists(video_path):
        print(f"❌ קובץ הסרטון לא נמצא בנתיב: {video_path}")
    else:
        process_video(video_path)
