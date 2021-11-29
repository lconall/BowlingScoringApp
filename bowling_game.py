

class BowlingGame():
    def __init__(self, *args, **kwargs):
        self._shots = []
        self._current_shot = 0

    def add_shot(self, shot: int) -> None:
        self._shots.append(shot)

    @property
    def score(self):
        score = 0
        frame_first_shot_index = 0
        for frame in range(0, 10):
            if self.is_strike(frame_first_shot_index):
                score += self.strike_frame_score(frame_first_shot_index)
                frame_first_shot_index += 1
            elif self.is_spare(frame_first_shot_index):
                score += self.spare_frame_score(frame_first_shot_index)
                frame_first_shot_index += 2
            else:
                score += self.open_frame_score(frame_first_shot_index)
                frame_first_shot_index += 2
            print(f"frame={frame}, frame_first_shot_index={frame_first_shot_index}, score={score}")
        return score

    def is_strike(self, frame_first_shot_index):
        return self._shots[frame_first_shot_index] == 10

    def strike_frame_score(self, frame_first_shot_index):
        return 10 + self._shots[frame_first_shot_index + 1] + self._shots[frame_first_shot_index + 2]

    def is_spare(self, frame_first_shot_index):
        return self._shots[frame_first_shot_index] + self._shots[frame_first_shot_index + 1] == 10

    def spare_frame_score(self, frame_first_shot_index):
        return 10 + self._shots[frame_first_shot_index + 2]

    def open_frame_score(self, frame_first_shot_index):
        return self._shots[frame_first_shot_index] + self._shots[frame_first_shot_index + 1]
