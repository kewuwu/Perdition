class Cards:
    def __init__(self, type):
        self.type = type


class Souls(Cards):
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
        super().__init__("soul")
        self.id = id
        self.name = name
        self.rarity = rarity
        self.sin = sin
        self.ceffect = ceffect
        self.reffect = reffect
        self.vp = vp
        self.front_png = front_png
        self.back_png = back_png


class Players(Cards):
    def __init__(self, id, name=None, guilt=None, front_png=None, back_png=None):
        super().__init__("player")
        self.id = id
        self.name = name
        self.guilt = guilt
        self.front_png = front_png
        self.back_png = back_png


class Daemon(Cards):
    def __init__(
        self, id, sin=None, layerCards=None, name=None, front_png=None, back_png=None
    ):
        super().__init__("daemon")
        self.id = id
        self.sin = sin
        self.layerCards = layer_cards
        self.name = name
        self.front_png = front_png
        self.back_png = back_png


class DivineRevelation(Cards):
    def __init__(
        self, id, effect=None, vp=None, name=None, front_png=None, back_png=None
    ):
        super().__init__("divine_revelation")
        self.id = id
        self.effect = effect
        self.vp = vp
        self.name = name
        self.font_png = front_png
        self.back_png = back_png


class layer_cards(Cards):
    def __init__(
        self, id, name=None, sin=None, effect=None, front_png=None, back_png=None
    ):
        super().__init__("layer_event")
        self.id = id
        self.name = name
        self.front_png = front_png
        self.back_png = back_png
        self.sin = sin
        self.effect = effect
