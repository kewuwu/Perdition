
class Player:
    def __init__(self, player_number: int) -> None:
        self.player_number = player_number

        # currencies
        self.victory_points: int = 0
        self.guilt: int = 0
        self.layer_currency: int = 0
        self.souls: list = []

        self.hand = []

    def take_turn(self):
        raise NotImplementedError()

class HumanPlayer(Player):
    def __init__(self, player_number: int) -> None:
        super().__init__(player_number)

    def take_turn(self):
        print("Your turn")
        print("Hand:")
        for c in self.hand:
            print(c)
        uin = input("> ")
        if uin.lower() in ['q', 'quit', 'exit']:
            exit()

class AIPlayer(Player):
    def __init__(self, player_number: int) -> None:
        super().__init__(player_number)

    def take_turn(self):
        print(f"Player {self.player_number}'s turn")
        