import json

from card import Card
from observer import Observer, Subject
from player import HumanPlayer, AIPlayer, Player
from board import Board
import card_parser 

class Game:
    def __init__(self) -> None:
        self.players = [HumanPlayer(1), AIPlayer(2)]
        self.active_player = 1

        self.board = Board()

        self.start_of_turn_passive_subject = Subject()
        self.end_of_turn_passive_subject = Subject()

        self.deck = self._load_cards()

        self.players[0].hand.append(self.deck[-1])

    def _load_cards(self) -> list:
        c = Card("Broker of Diminishing Returns", "Greed", "Soul", "Common", None, {}, {})
        # with open("./cards.json", 'r') as fp:
        #     card_json = json.load(fp)
        # card_parser.exec_from_dict(card_json)
        return [c]

    def start(self):
        while True:
            self.do_round()

    def do_round(self):
        for p in self.players:
            self.active_player = p
            self.do_turn(p)

    def do_turn(self, player: Player):
        # return cards from punish/confess
        self.return_from_punishment_and_confession()
        # start of turn passives
        self._check_passives("start")
        # (player turn) purchase cards, tap cards, send cards to punish/confess
        player.take_turn()
        # end of turn passives
        self._check_passives("end")
        pass

    def _check_passives(self, condition: str):
        if condition == 'start':
            self.start_of_turn_passive_subject.notify()
        elif condition == 'end':
            self.end_of_turn_passive_subject.notify()

    def return_from_punishment_and_confession(self):
        for zone in [self.board.confession_zone, self.board.punishment_zone]:
            for card in filter(lambda c: c['player'] == self.active_player, zone):
                if card['rounds'] >= 2:
                    self.active_player.hand.append(zone.pop(zone.index(card)))


    def corrupt_or_redeem_soul(self, c_or_r, soul_card: Card, player: Player):
        if c_or_r == 'corrupt':
            zone = self.board.punishment_zone
        elif c_or_r == 'redeem':
            zone = self.board.confession_zone
        zone.append({"card": soul_card, "player": player, "rounds": 0})

if __name__ == "__main__":
    g = Game()
    g.start()