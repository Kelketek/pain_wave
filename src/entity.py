
class Entity(object):
    def __init__(self, name=None):
        self.name = None
        self.components = []

    def get(self, kind):
        for comp in self.components:
            if type(comp) == kind:
                return comp
        return None

    def expect(self, kind):
        result = self.get(kind)
        if result is None:
            raise TypeError('Entity does not have component of type ' + str(kind))
        return result

    def add(self, comp):
        if self.get(type(comp)) is not None:
            raise TypeError('Entity already has component of that type')
        self.components.append(comp)

    def __repr__(self):
        return "<{name} with components {components}>".format(
            name=self.name or 'Unknown Entity', components=self.components
        )

    def __str__(self):
        return self.__repr__()


def components_typed(entities, kind):
    for entity in entities:
        comp = entity.get(kind)
        if comp is not None:
            yield comp


def entities_with(entities, kind):
    for entity in entities:
        if entity.get(kind) is not None:
            yield entity
