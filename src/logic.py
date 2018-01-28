class Timer:
    def __init__(self, interval, playtime, tasks=None):
        self.interval = interval
        self.timestamp = playtime
        if tasks is None:
            tasks = []
        self.tasks = tasks

    def tick(self, playtime, entities):
        if self.timestamp is None:
            self.timestamp = playtime
            return
        if (playtime - self.timestamp) >= self.interval:
            for task in self.tasks:
                task(entities)
            self.timestamp = playtime


class Trigger:
    def __init__(self, tasks=None):
        """
        :param tasks: List of (condition, action) value pairs. Both take the entities list as an argument.
        """
        if tasks is None:
            tasks = []
        self.tasks = tasks

    def pull(self, entities):
        for condition, task in self.tasks:
            if condition(entities):
                task(entities)


class Restart:
    """Flag for restarting the game.
    """
    pass


class Quit:
    """Flag for quitting the game
    """


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
