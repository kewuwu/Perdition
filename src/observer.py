

class Observer:
    def __init__(self, on_update_func) -> None:
        self.on_update_func = on_update_func

    def update(self, subject, game, *args, **kwargs):
        self.on_update_func(subject, game, *args, **kwargs)


class Subject:
    def __init__(self) -> None:
        self._observers = []

    def notify(self, game, *args, **kwargs):
        for observer in self._observers:
            observer.update(self, game, *args, **kwargs)
        pass

    def subscribe(self, observer: Observer):
        self._observers.append(observer)

    def unsubscribe(self, observer: Observer):
        self._observers.remove(observer)