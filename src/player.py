from card import SoulCard
from game_utils import get_input

class Player:
    def __init__(self, player_number: int) -> None:
        self.player_number = player_number

        self._reset()

    def take_turn(self):
        raise NotImplementedError()
    
    def _reset(self):
        # currencies
        self.victory_points: int = 0
        self.guilt: int = 0
        self.layer_currency: int = 0
        self.souls: list = []

        self.hand = []

        self.turn_actions = {
            "purchased_souls_this_turn": []
        }

class HumanPlayer(Player):
    def __init__(self, player_number: int) -> None:
        super().__init__(player_number)

    def take_turn(self, purchase_func, corrupt_or_redeem_func):
        print("Your turn")
        print("Hand:")
        for c in self.hand:
            print("\t" + str(c))
        print("What would you like to do?")
        
        options = [
            {
                "display_text": "Purchase", 
                "func": purchase_func, 
                "args": self._get_purchase_args
            },
            {
                "display_text": "Punish or Redeem soul", 
                "func": corrupt_or_redeem_func, 
                "args": self._get_corrupt_or_redeem_args
            }
        ]

        for i, o in enumerate(options):
            print(f"{i+1} - {o['display_text']}")
        uin = get_input(int, lambda x: x > 0 and x <= len(options))
        options[uin-1]['func'](*options[uin-1]['args']())

    def _get_purchase_args(self):
        return (self,)

    def _get_corrupt_or_redeem_args(self):
        def get_selected_cr_action():
            print("1 - Corrupt")
            print("2 - Redeem")
            uin = get_input(int, lambda x: x == 1 or x == 2)
            return 'corrupt' if uin == 1 else 'redeem'

        def get_selected_soul_card():
            soul_cards = list(filter(lambda c: isinstance(c, SoulCard), self.hand))
            for i, c in enumerate(soul_cards):
                print(f"{i+1} - {c}")
            uin = get_input(int, lambda x: x > 0 and x <= len(soul_cards)) - 1
            return soul_cards[uin]
        c_or_r = get_selected_cr_action()
        soul_card = get_selected_soul_card()
        return c_or_r, soul_card, self


class AIPlayer(Player):
    def __init__(self, player_number: int) -> None:
        super().__init__(player_number)

    def take_turn(self):
        print(f"Player {self.player_number}'s turn")
        