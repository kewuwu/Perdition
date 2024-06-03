

class Observer:
    def __init__(self, on_update_func) -> None:
        self.on_update_func = on_update_func

    def update(self, game_event, *args, **kwargs):
        self.on_update_func(game_event, *args, **kwargs)


class GameEvent:
    def __init__(self) -> None:
        self._observers = []

    def notify(self, *args, **kwargs):
        for observer in self._observers:
            observer.update(self, *args, **kwargs)

    def subscribe(self, observer: Observer):
        self._observers.append(observer)

    def unsubscribe(self, observer: Observer):
        self._observers.remove(observer)

class GameEvents:
    def __init__(self) -> None:
        self.start_of_turn = GameEvent()
        self.end_of_turn = GameEvent()
        self.start_of_round = GameEvent()
        self.end_of_round = GameEvent()
        self.start_of_layer = GameEvent()
        self.end_of_layer = GameEvent()

        self.divine_revelation_purchased = GameEvent()
        self.loan_repayed = GameEvent()
        self.item_traded = GameEvent()

        self.soul_card_activated = GameEvent()
        self.soul_card_attached = GameEvent()
        self.soul_card_corrupted = GameEvent()
        self.soul_card_destroyed = GameEvent()
        self.soul_card_discarded = GameEvent()
        self.soul_card_effect_copied = GameEvent()
        self.soul_card_purchased = GameEvent()
        self.soul_card_redeemed = GameEvent()
        self.soul_card_tapped = GameEvent()
        self.soul_card_unused = GameEvent()
        self.soul_card_used = GameEvent()

        self.currency_received = GameEvent()