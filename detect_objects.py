
from IdentifyingObstacles import detect_obstacles
from recogmizePeople import detect_enemies
from cargoIdentification import detect_explosives

def detect_all(frame):
    return {
        "obstacles": detect_obstacles(),
        "enemies": detect_enemies(),
        "explosives": detect_explosives()
    }
