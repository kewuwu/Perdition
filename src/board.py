


class Board:

    def __init__(self) -> None:
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

    def _reset(self):
        pass