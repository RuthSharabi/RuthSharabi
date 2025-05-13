import numpy as np

THRESHOLD = 1000  # סף מרחק שמעליו נחשב פנוי

def generate_lidar_data():
    distances = np.random.randint(500, 2000, 360)
    return distances

def process_lidar_data(distances):
    left_data = distances[:90]
    right_data = distances[90:180]
    front_data = distances[180:270]
    back_data = distances[270:360]

    avg_left = np.mean(left_data)
    avg_right = np.mean(right_data)
    avg_front = np.mean(front_data)
    avg_back = np.mean(back_data)

    return avg_left, avg_right, avg_front, avg_back

# מחזירה זיהוי בצורת מילון עבור הקוד הראשי
def detect_obstacle():
    lidar_data = generate_lidar_data()
    avg_left, avg_right, avg_front, _ = process_lidar_data(lidar_data)

    return {
        "front": avg_front < THRESHOLD,
        "left": avg_left < THRESHOLD,
        "right": avg_right < THRESHOLD
    }

