import json
import os
import random

from game_utils import get_input
import card
from observer import Observer, Subject
from player import HumanPlayer, AIPlayer, Player
from board import Board
import card_parser 

CURRENT_DIR = os.path.dirname(__file__)
CWD = os.getcwd()

STARTING_CARD_COUNT_PER_PLAYER = 7

ROUNDS_PER_LAYER = 3
LAYERS_PER_GAME = [
    'Greed'
]

class Game:
    def __init__(self) -> None:
        self.players = [HumanPlayer(1), AIPlayer(2)]
        self.active_player: Player = self.players[0]

        self.board = Board()

        self.start_of_turn_passive_subject = Subject()
        self.end_of_turn_passive_subject = Subject()

    def _load_cards(self) -> list:
        with open(os.path.join(CWD, "data", "card_data.json"), 'r') as fp:
            card_data = json.load(fp)

        deck = []
        for i, cd in enumerate(card_data):
            name = " ".join([k.capitalize() if k.lower() != 'of' else k for k in cd['name'].split()])
            card_type = cd['type']
            parsed_card = card_parser.parse_card_definition(cd)
            if parsed_card:
                deck.append(parsed_card)
        return deck

    def start(self):
        self.restart_game()
        for layer in LAYERS_PER_GAME:
            for i in range(ROUNDS_PER_LAYER):
                self.do_round(layer, i)

    def restart_game(self, starting_player: Player=None):
        """
        Reset to new game-ready state. Reset board, reset deck and shuffle, reset all players.
        Draw cards for players, assign initial currencies, choose starting player
        """
        self.board._reset()
        self.deck = self._load_cards()
        random.shuffle(self.deck)
        for player in self.players:
            player._reset()
        
        for _ in range(STARTING_CARD_COUNT_PER_PLAYER):
            for player in self.players:
                player.hand.append(self.deck.pop())

        self.active_player = starting_player or random.choice(self.players)

    def do_round(self, layer, round_num):
        print(f"Layer {layer} ({LAYERS_PER_GAME.index(layer) + 1}/{len(LAYERS_PER_GAME)})")
        print(f"Round {round_num + 1}/{ROUNDS_PER_LAYER})")
        for p in self.players:
            self.active_player = p
            self.do_turn(p)

    def do_turn(self, player: Player):
        # return cards from punish/confess
        self.return_from_punishment_and_confession()
        # start of turn passives
        self._check_passives("start")
        # (player turn) purchase cards, tap cards, send cards to punish/confess
        player.take_turn(self.purchase_soul, self.corrupt_or_redeem_soul)
        # end of turn passives
        self._check_passives("end")
        pass

    def _check_passives(self, condition: str):
        """
        Called at both the start and end of each round.
        Notify all subscribing cards that start/end has been triggered
        to check if criteria for effects are met
        """
        if condition == 'start':
            self.start_of_turn_passive_subject.notify()
        elif condition == 'end':
            self.end_of_turn_passive_subject.notify()

    def return_from_punishment_and_confession(self):
        """
        Called at the top of each player's round. Return cards that were put into
        confession and punishment 2 turns ago to players hand
        """
        for zone in [self.board.confession_zone, self.board.punishment_zone]:
            for card in filter(lambda c: c['player'] == self.active_player, zone):
                if card['rounds'] >= 2:
                    self.active_player.hand.append(zone.pop(zone.index(card)))

    def corrupt_or_redeem_soul(self, c_or_r, soul_card: card.Card, player: Player):
        """
        Add the soul_card to the respective corrupt or redeem board zone for the player
        """
        if c_or_r == 'corrupt':
            zone = self.board.punishment_zone
        elif c_or_r == 'redeem':
            zone = self.board.confession_zone
        zone.append({"card": soul_card, "player": player, "rounds": 0})

    def purchase_soul(self, player: Player):
        pass

if __name__ == "__main__":
    g = Game()
    g.start()