class Points:
    def __init__(self, user_id: str, points: int, last_updated: int):
        self.user_id = user_id
        self.points = points
        self.last_updated = last_updated

    def __repr__(self):
        return f"Points(user_id={self.user_id}, points={self.points}, last_updated={self.last_updated})"
