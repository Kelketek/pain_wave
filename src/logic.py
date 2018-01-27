from src.entity import Entity
from src.friction import Friction
from src.physics import Position, Movement, Collision


class Timer:
    def __init__(self, interval, playtime, tasks=None):
        self.interval = interval
        self.timestamp = playtime
        if tasks is None:
            tasks = []
        self.tasks = tasks

    def tick(self, playtime, entities):
        if (playtime - self.timestamp) >= self.interval:
            for task in self.tasks:
                task(entities)
            self.timestamp = playtime


class Trigger:
    def __init__(self, condition, task):
        self.condition = condition
        self.task = task

    def pull(self, entities):
        if self.condition():
            self.task(entities)


class ClearsOnStop:
    def __init__(self, entity, cutoff=.1):
        self.entity = entity
        self.cutoff = cutoff

    def check(self):
        movement = self.entity.get(Movement)
        if abs(movement.vx) <= self.cutoff and abs(movement.vy <= self.cutoff):
            return True

    def clear(self, entities):
        entities.remove(self.entity)


class Transmitter:
    def __init__(self, position, radius=10, velocity=(4, 0), projectile_name='Death Wave'):
        self.position = position
        self.radius = radius
        self.projectile_name = projectile_name
        self.velocity_vector = velocity

    def create_projectile(self, entities):
        entity = Entity(name=self.projectile_name)
        entity.add(Position(self.position.x, self.position.y, self.radius))
        entity.add(Movement(self.velocity_vector[0], self.velocity_vector[1]))
        entity.add(Collision(10))
        entity.add(Friction(.999))
        clear = ClearsOnStop(entity, cutoff=2)
        entity.add(Trigger(clear.check, clear.clear))
        entities.append(entity)


def update_triggers(entities):
    for entity in entities[:]:
        trigger = entity.get(Trigger)
        if trigger:
            trigger.pull(entities)


def update_timers(entities, playtime):
    for entity in entities[:]:
        timer = entity.get(Timer)
        if timer:
            timer.tick(playtime=playtime, entities=entities)
