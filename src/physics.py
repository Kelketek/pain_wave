from math import sqrt
from entity import entities_with


class Position(object):
    def __init__(self, x, y, radius):
        self.x = x
        self.y = y
        self.radius = radius

class Movement(object):
    def __init__(self, radius, mass):
        self.vx = 0
        self.vy = 0

    # def __str__(self):
    #     return ('Entity[r=' + str(self.radius) + ' x=' + str(self.x) + ' y=' + str(self.y) +
    #         ' vx=' + str(self.vx) + ' vy=' + str(self.vy) + ']')
    #
    # def __repr__(self):
    #     return str(self)

class Collision(object):
    def __init__(self, mass):
        self.mass = mass

# def distance(x1, y1, x2, y2):
#     dx = x1 - x2
#     dy = y1 - y2
#     return sqrt(dx * dx + dy * dy)
#
# def entity_distance(a, b):
#     return distance(a.x, a.y, b.x, b.y)

# def update(entities):
#     for entity in components_typed(entities, Physics):
#         entity.x += entity.vx
#         entity.y += entity.vy
#
#         if entity.mass is None:
#             continue
#         for other in entities:
#             if other == entity or other.mass is None:
#                 continue
#             cdist = entity_distance(entity, other)
#             overlap = entity.radius + other.radius - cdist
#             if overlap > 0:
#                 entity.vx += abs(entity.x - other.x) / entity.mass / 10
#                 entity.vy += abs(entity.y - other.y) / entity.mass / 10

def random_entity():
    from random import random
    from entity import Entity
    # result = Entity(random() * 5 + 10, random() * 9 + 1)
    # result.x = random() * 10
    # result.y = random() * 10
    result = Entity()
    entity.add(Position(random() * 10, random() * 10))
    return result

### testing ###
if __name__ == '__main__':
    assert distance(0, 0, 0, 0) == 0
    assert distance(0, 0, 1, 0) == 1
    assert distance(-1, 0, 0, 0) == 1

    entities = []
    for _ in range(10):
        entities.append(random_entity())

    print(entities)
    for _ in range(3):
        update(entities)
        print(entities)
