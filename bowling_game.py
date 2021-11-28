

class BowlingGame():
    def __init__(self, *args, **kwargs):
        self._shots = []

    def add_shot(self, shot: int) -> None:
        self._shots += [shot]

    @property
    def score(self):
        return sum(self._shots)
