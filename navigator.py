class Navigator:
    def get_next_move(self, frame, location):
        # כלל ימינה תמיד, אלא אם מכשול
        return 'E'  # כיוון סימולציה

    def avoid_obstacle(self, location):
        return 'N'

    def avoid_explosive(self, location):
        return 'S'

    def is_entry_point(self, location):
        return location == (0, 0)
