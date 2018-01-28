from src.grapple import Drag
from .entity import entities_with
from .violence import Transmitter, Vulnerable, Team
from .physics import Movement
from .hardware import Controller
from .friction import Friction
from .logic import Timer


class EndGameplayOnDeath:
    pass


def end_gameplay(entities):
    for entity in entities:
        entity.remove_type(Transmitter)
        entity.remove_type(Vulnerable)
        entity.remove_type(Movement)
        entity.remove_type(Drag)
        controller = entity.get(Controller)
        if controller:
            controller.menu = True
        entity.remove_type(Friction)
        entity.remove_type(Timer)


def update_end_gameplay(entities):
    for entity in entities:
        if not entity.get(EndGameplayOnDeath):
            continue
        team = entity.expect(Team)
        vulnerable = entity.get(Vulnerable)
        if vulnerable and vulnerable.dead:
            end_gameplay(entities)
            return team.team
