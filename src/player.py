from card import SoulCard, DivineRevelationCard
import card
from game_utils import get_input
from functools import partial
from time import sleep

class Player:
    def __init__(self, player_number: int) -> None:
        self.player_number = player_number
        self._reset()

    def take_turn(self):
        raise NotImplementedError()
    
    @property
    def player_article_text(self):
        return "You" if self.player_number == 0 else ("Player " + str(self.player_number))
    
    def _reset(
            self, 
            victory_points: int = 0, 
            guilt: int = 0, 
            layer_currency: int = 0, 
            soul_hand: list[SoulCard] = None,
            divine_revelation_hand: list[DivineRevelationCard] = None,
            field: list[SoulCard] = None
        ):
        # currencies
        self.victory_points = victory_points
        self.guilt = guilt
        self.layer_currency = layer_currency

        # unplayed souls
        self.soul_hand = soul_hand if soul_hand is not None else []
        self.divine_revelation_hand = divine_revelation_hand if divine_revelation_hand is not None else []
        # active souls
        self.field = field if field is not None else []
        # actions that the player performed this turn (used for determining some card effects)
        self.turn_actions = {
            "purchased_souls_this_turn": []
        }

    def end_turn(self):
        self.turn_actions = {
            "purchased_souls_this_turn": []
        }

class HumanPlayer(Player):
    def __init__(self, player_number: int) -> None:
        super().__init__(player_number)

    def take_turn(
            self, 
            purchase_func, 
            corrupt_or_redeem_func, 
            purchase_divine_revelation_card_func, 
            tap_card_func,
            recharge_tapped_card_func,
            game
    ):
        print("Your turn")
        print("Hand:")
        for c in self.soul_hand:
            print("\t" + str(c))
        print("What would you like to do?")
        
        # TODO: remove this and replace with Game.player_options passed into function
        options = [
            {
                "display_text": "Purchase", 
                "func": purchase_func, 
                "args": partial(self._get_purchase_args, game)
            },
            {
                "display_text": "Punish or Redeem soul (1 Guilt)", 
                "func": corrupt_or_redeem_func, 
                "args": self._get_corrupt_or_redeem_args
            },
            {
                "display_text": "Purchase Divine Intervention card",
                "func": purchase_divine_revelation_card_func,
                "args": partial(self._destroy_cards, 2, list(filter(lambda c: c.converted_to == card.REDEEMED, self.soul_hand)))
            },
            {
                "display_text": "Tap Soul Card",
                "func": tap_card_func,
                "args": self._get_tapped_card_args
            },
            {
                "display_text": "Rechard Tapped Card (2 Guilt)",
                "func": recharge_tapped_card_func,
                "args": self._get_card_to_recharge_args
            },
            {
                "display_text": "End turn (end turn)"
            }
        ]

        CHEATS = ['givemegold']

        while True:
            print(f"Guilt: {self.guilt}")
            print(f"Currency: {self.layer_currency}")
            for i, o in enumerate(options):
                print(f"{i+1} - {o['display_text']}")
            uin = get_input(
                str, 
                lambda x: x in ['end turn']+CHEATS or (int(x) > 0 and int(x) <= len(options))
            )
            if uin == 'end turn':
                break
            elif uin == 'givemegold':
                self.layer_currency += 100
                continue
            uin = int(uin)
            args = options[uin-1]['args']()
            if not args:
                continue
            options[uin-1]['func'](*args)

    @staticmethod
    def _destroy_cards(num_cards, cards_to_choose_from: list[SoulCard]) -> tuple:
        selected_cards = []
        if not cards_to_choose_from:
            print("No cards to destroy")
            return

        while len(selected_cards) < num_cards:
            if selected_cards:
                print("Cards selected:")
                print([str(c) for c in selected_cards])
            print("Choose a card to destroy")
            for i, card in enumerate(cards_to_choose_from):
                print(f"{i+1} - {card}")
            uin = get_input(int, lambda x: x > 0 and x <= len(cards_to_choose_from))
            selected_cards.append(cards_to_choose_from.pop(uin-1))
        return selected_cards

    def _get_purchase_args(self, game):
        print("Which card do you wish to purchase?")
        purchasable_cards = game.board.pit_of_annihilation_zone
        for i, c in enumerate(purchasable_cards):
            print(f"{i+1} - {c} ({game.configs.card_costs[c.rarity]})")
        print(f"{i+2} - Purchase from top of deck ({game.configs.card_costs['unknown']})")
        uin = get_input(int, lambda x: x > 0 and x <= len(purchasable_cards) + 1)
        if uin > len(purchasable_cards):
            selected_card = game.board.soul_deck[-1]
            card_type_purchased = 'unknown'
        else:
            selected_card = purchasable_cards[uin-1]
            card_type_purchased = selected_card.rarity
        return self, selected_card, card_type_purchased

    def _get_corrupt_or_redeem_args(self):
        def get_selected_cr_action():
            print("1 - Corrupt")
            print("2 - Redeem")
            uin = get_input(int, lambda x: x == 1 or x == 2)
            return 'corrupt' if uin == 1 else 'redeem'

        def get_selected_soul_card():
            soul_cards = list(filter(lambda c: isinstance(c, SoulCard), self.soul_hand))
            for i, c in enumerate(soul_cards):
                print(f"{i+1} - {c}")
            uin = get_input(int, lambda x: x > 0 and x <= len(soul_cards)) - 1
            return soul_cards[uin]
        c_or_r = get_selected_cr_action()
        soul_card = get_selected_soul_card()
        return c_or_r, soul_card, self

    def _get_tapped_card_args(self):
        def is_tappable(c):
            if c.is_active and c.converted_to == card.REDEEMED and 'tap' in c.reffect:
                return True
            if c.is_active and c.converted_to == card.CORRUPTED and 'tap' in c.ceffect:
                return True
            return False
        tappable_cards = list(filter(lambda c: is_tappable(c), self.field))
        if not tappable_cards:
            print("No tappable cards")
            return None
        print("Which card would you like to tap?")
        for i, c in enumerate(tappable_cards):
            print(f"{i+1} - {c}")
        uin = get_input(int, lambda x: x > 0 and x <= len(tappable_cards)) 
        return self, tappable_cards[uin-1]       

    def _get_card_to_recharge_args(self):
        return None

class AIPlayer(Player):
    def __init__(self, player_number: int) -> None:
        super().__init__(player_number)

    def take_turn(self, purchase_soul_func, corrupt_or_redeem_func, purchase_divine_revelation_card_func, game):
        print(f"Player {self.player_number}'s turn")
        sleep(2)
        