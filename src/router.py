from .entity import entities_with
from .physics import entity_overlap, Movement


class Router:
    # def __init__(self):
    pass

class Routable:
    pass


# class RouterTrigger:
#     # def __init__(self):
#     #     self.entity = entity
#     #     self.hit_list = []
#
#     def check(self, entities):
#         # self.hit_list = [
#         #     entity for entity in entities if
#         #     (entity_overlap(self.entity, entity) > 0 and entity.get(Vulnerable))
#         #     and not entity == self.entity
#         # ]
#         # return self.hit_list
#
#     def action(self, entities):
#         # for entity in self.hit_list:
#         #     entities.remove(entity)
#


def update_routers(entities):
    for entity in entities_with(entities, Router):
        for other in entities_with(entities, Routable):
            if entity_overlap(entity, other) > 0:
                # TODO: Need facing module
                movement = other.get(Movement)
                movement.vx = 2
                movement.vy = 2



                # movement = entity.get(Movement)
                # mass = entity.get(Collision).mass
                # position_a = entity.get(Position)
                # position_b = other.get(Position)
                #
                # movement.vx += (position_a.x - position_b.x) / mass / 8.0
                # movement.vy += (position_a.y - position_b.y) / mass / 8.0

            # entity for entity in entities if
            # (entity_overlap(self.entity, entity) > 0 and entity.get(Vulnerable))
            # and not entity == self.entity
