class Card:
    def __init__(self, card_type, name, front_png, back_png):
        self.card_type = card_type
        self.name = name
        self.front_png = front_png
        self.back_png = back_png

        self.in_play = False


class Soul(Card):
    def __init__(
        self,
        id,
        name=None,
        rarity=None,
        sin=None,
        ceffect=None,
        reffect=None,
        vp=None,
        front_png=None,
        back_png=None,
    ):
        super().__init__("soul", name, front_png, back_png)
        self.id = id
        self.rarity = rarity
        self.sin = sin
        self.ceffect = ceffect
        self.reffect = reffect
        self.vp = vp

    def __str__(self) -> str:
        return f"{self.name} - {self.rarity} {self.sin} {self.card_type}"


class Player(Card):
    def __init__(self, id, name=None, guilt=None, front_png=None, back_png=None):
        super().__init__("player", name, front_png, back_png)
        self.id = id
        self.guilt = guilt


class DaemonCard(Card):
    def __init__(
        self, id, sin=None, layer_card=None, name=None, front_png=None, back_png=None
    ):
        super().__init__("daemon", name, front_png, back_png)
        self.id = id
        self.sin = sin
        self.layer_card = layer_card


class DivineRevelationCard(Card):
    def __init__(
        self, id, effect=None, vp=None, name=None, front_png=None, back_png=None
    ):
        super().__init__("divine_revelation", name, front_png, back_png)
        self.id = id
        self.effect = effect
        self.vp = vp


class LayerCard(Card):
    def __init__(
        self, id, name=None, sin=None, effect=None, front_png=None, back_png=None
    ):
        super().__init__("layer_event", name, front_png, back_png)
        self.id = id
        self.sin = sin
        self.effect = effect
