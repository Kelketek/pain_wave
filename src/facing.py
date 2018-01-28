
class Facing:
    """Determines which direction an object is facing.
    """
    def __init__(self, degrees, entity):
        self.degrees = degrees
        self.entity = entity
        self.surface = None
        self.last_degrees = None
