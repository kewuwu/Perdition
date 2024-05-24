

class Observer:
    def update(self, subject):
        pass


class Subject:
    def __init__(self) -> None:
        self._observers = []

    def notify(self):
        for observer in self._observers:
            observer.update(self)
        pass

    def subscribe(self, observer: Observer):
        self._observers.append(observer)

    def unsubscribe(self, observer: Observer):
        self._observers.remove(observer)