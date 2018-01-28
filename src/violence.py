import pygame

from .hardware import Controller
from .entity import Entity
from .friction import Friction
from .logic import Trigger, Timer
from .physics import Position, Movement, Collision, entity_overlap, distance
from .router import Routable
from .facing import Facing
from .face_toward_movement import FaceTowardMovement
from .video import Image
from .boundary import DieOnReflect


# shoot_sound = pygame.mixer.Sound('assets/shoot.ogg')
kill_sound = pygame.mixer.Sound('assets/Collision Opt 2.wav')

ASPLODE_TIME = .2


class Murders:
    """Removes anything that's vulnerable from the entities list. See the Vulnerable class.
    """
    def __init__(self, entity):
        self.entity = entity
        self.hit_list = []

    def grope(self, entities):
        self.hit_list = [
            entity for entity in entities if
            (entity_overlap(self.entity, entity) > 0
            and entity.get(Vulnerable))
            and not entity == self.entity
            and not entity.get(Vulnerable).dead
        ]
        return self.hit_list

    def kill(self, entities):
        if self.hit_list:
            kill_sound.play()
        for entity in self.hit_list:
            controller = entity.get(Controller)
            if controller:
                controller.disabled = True
                entity.add(Timer(ASPLODE_TIME, None, tasks=[
                    lambda entities: entity.replace(Image('assets/character_dead_2.png', entity, fixed_rotation=True))
                ]))
            entity.remove_type(Collision)
            vulnerable = entity.get(Vulnerable)
            vulnerable.dead = True
            if vulnerable.next_image:
                entity.replace(vulnerable.next_image)
            if not vulnerable.tombstone:
                try:
                    entities.remove(entity)
                except ValueError:
                    # Already removed by some other condition.
                    pass


class Transmitter:
    def __init__(self, position, velocity, projectile_name='Pain Wave', offset=(0, 0), radius=10):
        self.position = position
        self.radius = radius
        self.projectile_name = projectile_name
        self.velocity_vector = velocity
        self.offset = offset

    def create_projectile(self, entities):
        # shoot_sound.play()
        entity = Entity(name=self.projectile_name)
        entity.add(Position(self.position.x + self.offset[0], self.position.y + self.offset[1],
                            self.radius))
        movement = Movement(self.velocity_vector[0], self.velocity_vector[1])
        entity.add(movement)
        entity.add(Collision(1))
        entity.add(Friction(.999))
        clear = ClearsOnStop(entity, cutoff=2)
        murder = Murders(entity)
        entity.add(Trigger([(clear.check, clear.clear), (murder.grope, murder.kill)]))
        entity.add(Vulnerable())
        entity.add(Routable())
        entity.add(Facing(0, entity))
        entity.add(FaceTowardMovement())
        entity.add(Image('assets/pain_wave.png', entity))
        entity.add(DieOnReflect())
        entities.append(entity)


class ClearsOnStop:
    def __init__(self, entity, cutoff=.1):
        self.entity = entity
        self.cutoff = cutoff

    def check(self, _):
        movement = self.entity.get(Movement)
        if movement:
            magnitude = distance(0, 0, movement.vx, movement.vy)
            if magnitude <= self.cutoff:
                return True

    def clear(self, entities):
        try:
            entities.remove(self.entity)
        except ValueError:
            # Already removed by some other condition.
            pass


class Team:
    def __init__(self, team):
        self.team = team


class Vulnerable:
    """Declares whether something should be destroyed
    if touched by a destructive item. If 'tombstone' is set, keeps in the entity list,
    but removes ability to affect other entities.
    """
    def __init__(self, tombstone=False, next_image=None):
        self.tombstone = tombstone
        self.dead = False
        self.next_image = next_image
