from game_events import Observer


REDEEMED = 'redeemed'
CORRUPTED = 'corrupted'

class Card:
    def __init__(self, card_type, card_id, name, front_png, back_png):
        self.card_id = card_id
        self.card_type = card_type
        self.name = name
        self.front_png = front_png
        self.back_png = back_png

        self.is_active = False
        self.event_observers = []


class SoulCard(Card):
    def __init__(
        self,
        card_id=None,
        name=None,
        rarity=None,
        sin=None,
        ceffect=None,
        reffect=None,
        vp=None,
        front_png=None,
        back_png=None,
    ):
        super().__init__("soul", card_id, name, front_png, back_png)
        self.rarity = rarity
        self.sin = sin
        self.ceffect = ceffect
        self.reffect = reffect
        self.vp = vp
        self.tapped = False
        self.converted_to = None

    def __str__(self) -> str:
        return f"{self.name} - {self.rarity.capitalize()} {self.sin.capitalize()} {self.card_type.capitalize()}"


class PlayerCard(Card):
    def __init__(self, card_id, name, front_png, back_png):
        super().__init__("player", card_id, name, front_png, back_png)
    
    def __str__(self) -> str:
        return f"{self.name} - Player"


class DaemonCard(Card):
    def __init__(
        self, card_id, sin=None, layer_card=None, name=None, front_png=None, back_png=None
    ):
        super().__init__("daemon", card_id, name, front_png, back_png)
        self.sin = sin
        self.layer_card = layer_card

    def __str__(self) -> str:
        return f"{self.name} - {self.card_type.capitalize()} of {self.sin}"


class DivineRevelationCard(Card):
    def __init__(
        self, card_id, effect=None, vp=None, name=None, front_png=None, back_png=None
    ):
        super().__init__("divine_revelation", card_id, name, front_png, back_png)
        self.effect = effect
        self.vp = vp

    def __str__(self) -> str:
        return f"{self.name} - {self.card_type.replace('_', ' ').capitalize()}"


class LayerCard(Card):
    def __init__(
        self, card_id, name=None, sin=None, effect=None, front_png=None, back_png=None
    ):
        super().__init__("layer_event", card_id, name, front_png, back_png)
        self.sin = sin
        self.effect = effect

    def __str__(self) -> str:
        return f"{self.name} - {self.sin.capitalize()} {self.card_type.replace('_', ' ').capitalize()}"
