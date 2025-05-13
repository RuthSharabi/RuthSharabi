class SLAM:
    def __init__(self):
        self.map = {}
        self.location = (0, 0)
        self.direction = 'E'

    def update_location(self, frame):
        # סימולציה של זיהוי תזוזה
        x, y = self.location
        if self.direction == 'E':
            x += 1
        elif self.direction == 'N':
            y += 1
        elif self.direction == 'W':
            x -= 1
        elif self.direction == 'S':
            y -= 1
        self.location = (x, y)
        return self.location

    def move(self, direction):
        self.direction = direction
