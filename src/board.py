

class Board:

    def __init__(self, configs, cards) -> None:
        self.all_cards = cards
        self.configs = configs
        self._reset()

    def populate_pit_of_annihilation(self):
        while len(self.pit_of_annihilation_zone) < self.configs.pit_of_annihilation_size:
            if self.soul_deck:
                self.pit_of_annihilation_zone.append(self.soul_deck.pop())

    def _reset_zones(self):
        # corrupts souls - grants 3 layer currency
        self.punishment_zone = []
        # redeems souls - returns 1 guilt
        self.confession_zone = []
        # sacrifice 2 redeeemed souls for 1 revelation card
        self.revelation_zone = []
        # purchase things
        self.pit_of_annihilation_zone = []
        # archdaemon and layer event
        self.throne_zone = []

    def _reset_decks(self):
        self.soul_deck = list(filter(lambda c: c.card_type == 'soul', self.all_cards))
        self.layer_event_deck = list(filter(lambda c: c.card_type == 'layer_event', self.all_cards))
        self.divine_revelation_deck = list(filter(lambda c: c.card_type == 'divine_revelation', self.all_cards))
        self.archdaemon_deck = list(filter(lambda c: c.card_type == 'archdaemon', self.all_cards))
        self.player_deck = list(filter(lambda c: c.card_type == 'player', self.all_cards))
        
        self.discard_deck = []
        # cards that players have set to be either corrupted or redeemed
        self.active_conversion_deck = []

    def _reset(self):
        self._reset_zones()
        self._reset_decks()
