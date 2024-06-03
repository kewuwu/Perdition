import json
import os
import random
import yaml
import math
import card
from game_events import GameEvent, GameEvents, Observer
from player import HumanPlayer, AIPlayer, Player
from board import Board
import card_parser 
from configLoader import Config
from functools import partial

CURRENT_DIR = os.path.dirname(__file__)
CWD = os.getcwd()
CONFIG_FILE_PATH = os.path.join(CWD, "src", "game_settings.yaml")


class Game:
    def __init__(self, configs: Config) -> None:
        self.configs = configs
        self.game_events = GameEvents()

        self.players: list[Player] = [HumanPlayer(1)]
        for i in range(self.configs.max_players - 1):
            self.players.append(AIPlayer(i+2))
        self.active_player: Player = self.players[0]
        self.current_layer = None

        self.start_of_turn_passive_game_event = GameEvent()
        self.end_of_turn_passive_game_event = GameEvent()

        self.cards = self._load_cards()
        self.board = Board(configs, self.cards)

    def _load_cards(self) -> list:
        with open(os.path.join(CWD, "data", "card_data.json"), 'r') as fp:
            card_data = json.load(fp)

        deck = []
        for i, cd in enumerate(card_data):
            name = " ".join([k.capitalize() if k.lower() != 'of' else k for k in cd['name'].split()])
            card_type = cd['type']
            parsed_card = card_parser.parse_card_definition(cd, self)
            if parsed_card:
                deck.append(parsed_card)
        return deck

    def start(self):
        self.restart_game(self.players[0])
        for layer in self.configs.game_layers:
            self.do_layer(layer)
            for round_num in range(self.configs.rounds_per_layer):
                self.do_round(layer, round_num)

    def do_layer(self, layer):
        layer_num = self.configs.game_layers.index(layer) + 1
        print(f"{layer['name']} Layer ({layer_num}/{len(self.configs.game_layers)})")
        # TODO: load layer event card & archdaemon
        self.current_layer = layer
        if layer_num > 1:
            for player in self.players:
                player.layer_currency = math.floor(player.layer_currency * self.configs.layer_currency_retention_on_layer_transition)

    def restart_game(self, starting_player: Player=None):
        """
        Reset to new game-ready state. Reset board, reset deck and shuffle, reset all players.
        Draw cards for players, assign initial currencies, choose starting player
        """
        self.board._reset()
        
        self.discard = []
        # FIXME: shuffle these
        # random.shuffle(self.board.soul_deck)
        # random.shuffle(self.board.archdaemon_deck)
        # random.shuffle(self.board.divine_revelation_deck)
        # random.shuffle(self.board.layer_event_deck)

        for player in self.players:
            player._reset(
                guilt=self.configs.game_layers[0]['max-guilt'], 
                layer_currency=self.configs.starting_layer_currency_per_player
            )

        self.players[0].soul_hand.append(self.board.soul_deck.pop(2))
        self.players[0].soul_hand[0].is_active = True
        self.players[0].soul_hand[0].converted_to = card.REDEEMED
        
        for _ in range(self.configs.starting_card_count_per_player):
            for player in self.players:
                player.soul_hand.append(self.board.soul_deck.pop())
        # FIXME:
        

        self.active_player = starting_player or random.choice(self.players)

    def do_round(self, layer, round_num):
        print(f"Round ({round_num + 1}/{self.configs.rounds_per_layer})")
        for p in self.players:
            self.active_player = p
            self.do_turn(p)

    def do_turn(self, player: Player):
        self.board.populate_pit_of_annihilation()
        # return cards from punish/confess
        self.return_from_punishment_and_confession()
        # start of turn passives
        self._check_passives("start")
        # (player turn) purchase cards, tap cards, send cards to punish/confess
        player.take_turn(
            self.purchase_soul, 
            self.corrupt_or_redeem_soul, 
            self.purchase_divine_revelation,
            self.tap_card,
            self.recharge_tapped_card,
            self
        )
        # end of turn passives
        self._check_passives("end")

        for card in filter(lambda c: c['player'] == self.active_player, self.board.confession_zone + self.board.punishment_zone):
            card['rounds'] += 1
        player.end_turn()
        pass

    def _check_passives(self, condition: str):
        """
        Called at both the start and end of each round.
        Notify all subscribing cards that start/end has been triggered
        to check if criteria for effects are met
        """
        if condition == 'start':
            self.start_of_turn_passive_game_event.notify()
        elif condition == 'end':
            self.end_of_turn_passive_game_event.notify()

    def return_from_punishment_and_confession(self):
        """
        Called at the top of each player's round. Return cards that were put into
        confession and punishment 2 turns ago to players hand
        """
        for zone in [self.board.confession_zone, self.board.punishment_zone]:
            for c in filter(lambda c: c['player'] == self.active_player, zone):
                if c['rounds'] >= 2:
                    c = zone.pop(zone.index(c))['card']
                    if zone == self.board.confession_zone:
                        c.converted_to = card.REDEEMED
                    else:
                        c.converted_to = card.CORRUPTED
                    self.active_player.soul_hand.append(c)

    # card observer callback
    def do_card_effect(self, obj, c, effect_type, *args, **kwargs):
        if c.is_active and (
            (effect_type == 'reffect' and c.converted_to == card.REDEEMED) or 
            (effect_type == 'ceffect' and c.converted_to == card.CORRUPTED)
        ):
            print(f"Effect from Player {kwargs.get('player').player_number}'s -- {c} -- triggered!")
            card_parser.exec_from_dict(obj, self, **kwargs)

    ## PLAYER TURN FUNCTIONS
    def tap_card(self, card):
        pass

    def recharge_tapped_card(self, card):
        pass

    def purchase_soul(self, player: Player, card_to_purchase: card.SoulCard, card_type_purchased: str):
        if player.layer_currency < self.configs.card_costs[card_type_purchased]:
            print(f"Not enough money! {player.layer_currency}/{self.configs.card_costs[card_type_purchased]}")
        player.layer_currency -= self.configs.card_costs[card_type_purchased]
        player.soul_hand.append(card_to_purchase)
        self.game_events.soul_card_purchased.notify(item=card_to_purchase, player=player)
        if card_to_purchase in self.board.pit_of_annihilation_zone:
            self.board.pit_of_annihilation_zone.pop(self.board.pit_of_annihilation_zone.index(card_to_purchase))
        else:
            self.board.soul_deck.pop(self.board.soul_deck.index(card_to_purchase))

        self.board.populate_pit_of_annihilation()

    def purchase_divine_revelation(self, player: Player, selected_cards: list[card.SoulCard]):
        for card in selected_cards:
            card.is_active = False
            self.board.discard_deck.append(card)
        player.divine_revelation_hand.append(self.board.divine_revelation_deck.pop())
    
    def corrupt_or_redeem_soul(self, c_or_r, soul_card: card.Card, player: Player):
        """
        Add the soul_card to the respective corrupt or redeem board zone for the player
        """
        if player.guilt <= 0:
            print("Not enough guilt to convert soul")
            return
        player.guilt -= 1
        if c_or_r == 'corrupt':
            zone = self.board.punishment_zone
        elif c_or_r == 'redeem':
            zone = self.board.confession_zone
        zone.append({"card": soul_card, "player": player, "rounds": 0})
        player.soul_hand.pop(player.soul_hand.index(soul_card))


if __name__ == "__main__":
    with open(CONFIG_FILE_PATH, 'r') as fp:
        conf = Config(yaml.safe_load(fp))
    g = Game(conf)
    g.start()