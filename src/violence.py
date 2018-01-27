from src.entity import Entity
from src.friction import Friction
from src.logic import Trigger
from src.physics import Position, Movement, Collision, entity_overlap


class Murders:
    """Removes anything that's vulnerable from the entities list. See the Vulnerable class.
    """
    def __init__(self, entity):
        self.entity = entity
        self.hit_list = []

    def grope(self, entities):
        self.hit_list = [
            entity for entity in entities if
            (entity_overlap(self.entity, entity) > 0 and entity.get(Vulnerable))
            and not entity == self.entity
        ]
        return self.hit_list

    def kill(self, entities):
        for entity in self.hit_list:
            entities.remove(entity)


class Transmitter:
    def __init__(self, position, radius=10, velocity=(4, 0), projectile_name='Death Wave'):
        self.position = position
        self.radius = radius
        self.projectile_name = projectile_name
        self.velocity_vector = velocity

    def create_projectile(self, entities):
        entity = Entity(name=self.projectile_name)
        entity.add(Position(self.position.x, self.position.y, self.radius))
        movement = Movement()
        movement.vx = self.velocity_vector[0]
        movement.vy = self.velocity_vector[1]
        entity.add(movement)
        entity.add(Collision(10))
        entity.add(Friction(.999))
        clear = ClearsOnStop(entity, cutoff=2)
        murder = Murders(entity)
        entity.add(Trigger([(clear.check, clear.clear), (murder.grope, murder.kill)]))
        entity.add(Vulnerable())
        entities.append(entity)


class ClearsOnStop:
    def __init__(self, entity, cutoff=.1):
        self.entity = entity
        self.cutoff = cutoff

    def check(self, _):
        movement = self.entity.get(Movement)
        if abs(movement.vx) <= self.cutoff and abs(movement.vy <= self.cutoff):
            return True

    def clear(self, entities):
        entities.remove(self.entity)


class Vulnerable:
    """Used as a flag to declare whether something should be destroyed
    if touched by a destructive item.
    """
    pass
