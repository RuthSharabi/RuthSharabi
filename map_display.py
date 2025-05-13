class MapDisplay:
    def __init__(self):
        self.events = []

    def mark_event(self, location, event_type):
        print(f"⛳ {event_type} ב־{location}")
        self.events.append((location, event_type))

    def update(self, location, direction):
        print(f"רובוט נע ל-{location} בכיוון {direction}")
