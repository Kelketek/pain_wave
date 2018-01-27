
from .entity import entities_with, components_typed
from .physics import Movement

def update_friction(entities):
    for movement in components_typed(entities, Movement):
        movement.vx *= .95
        movement.vy *= .95
