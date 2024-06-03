
class Config:
    def __init__(self, raw) -> None:
        # Game Settings
        self.pit_of_annihilation_size = raw['pit-of-annihilation-size']
        self.max_active_cards_per_layer: int = raw['max-active-cards-per-player']
        self.corruption_layer_currency_reward: int = raw['corruption-layer-currency-reward']
        self.redemption_layer_currency_reward: int = raw['redemption-layer-currency-reward']
        self.max_cards_converted_per_layer: int = raw['max-cards-converted-per-layer']
        self.starting_card_count_per_player: int = raw['starting-card-count-per-player']
        self.starting_layer_currency_per_player = raw['starting-layer-currency-per-player']
        self.conversion_guilt_cost: int = raw['conversion-guilt-cost']
        self.max_players: int = raw['max-players']
        self.min_players: int = raw['min-players']

        # Card Settings
        self.diving_revelation_soul_cost: int = raw['divine-revelation-soul-cost']
        self.card_costs: dict = raw['card-costs']

        # Layer Settings
        self.restock_cards_per_layer: int = raw['restock-cards-per-layer']
        self.layer_currency_retention_on_layer_transition: int = raw['layer-currency-retention-on-layer-transition']
        self.layer_events_per_layer: int = raw['layer-events-per-layer']
        self.game_layers: list = raw['game-layers']
        self.rounds_per_layer: int = raw['rounds-per-layer']