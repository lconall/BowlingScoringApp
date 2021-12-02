from typing import List

from src.bowling_frame import BowlingFrame, TenthBowlingFrame


class BowlingGame():
    def __init__(self, *args, **kwargs):
        ''' Initializes the bowling game.'''
        self._shots = []
        self._current_frame = 0
        self._frames = self._initialize_frames()

    def _initialize_frames(self) -> List[BowlingFrame]:
        ''' Initializes the bowling frames in reverse order to allow successor frames to be passed to previous
        frames.

        Returns:
            list[BowlingFrame]: A list of the ten bowling frames for the game.
        '''
        tenth_bowling_frame = TenthBowlingFrame()
        frames = [tenth_bowling_frame]
        successor = tenth_bowling_frame
        for frame_index in reversed(range(0, 9)):
            frame = BowlingFrame(frame_number=frame_index + 1, successor=successor)
            frames.insert(0, frame)
            successor = frame
        return frames

    def add_shot(self, shot: int) -> None:
        ''' Adds shots to each frame and increments the frame to the next one when the current frame is complete.

        Args:
            shot(int): the score for the shot to be added to the bowling games.

        Returns:
            None
        '''
        self._frames[self._current_frame].add_shot(shot)
        if self._frames[self._current_frame].is_complete and self._current_frame < 9:
            self._current_frame += 1
        else:
            self._current_frame += 0

    def get_shots_by_frame(self) -> List[list]:
        ''' Returns the shots for each frame as a list of lists.
        Returns:
            List[list]: A list of lists with each sub list representing a frame.
        '''
        shots_by_frame = []
        for frame in self._frames:
            shots_by_frame.append(frame.get_shots())
        return shots_by_frame

    @property
    def cumulative_score_by_frame(self) -> List[int]:
        ''' Returns a list of ints representing the cumulative score at each frame.

        Note:
            This function will return None values (displayed as blanks) if the frame is not complete.

        Returns:
            List[int]: The cumulative score at each frame.
        '''
        score = 0
        frame_raw_scores = [frame.raw_score for frame in self._frames]
        cumulative_frame_score = 0
        cumulative_frame_scores = []
        for raw_score in frame_raw_scores:
            if cumulative_frame_score is not None and raw_score is not None:
                cumulative_frame_score = cumulative_frame_score + raw_score
            else:
                cumulative_frame_score = None
            cumulative_frame_scores.append(cumulative_frame_score)
        return cumulative_frame_scores

    @property
    def final_score(self) -> int:
        '''Returns the final score for the game.

        Note:
            In the case of a game that is incomplete this will only score the completed frames. All incompleted
            frames will not be included in the score.

        Returns:
            int: The final score for the current bowling game.
        '''
        score = 0
        for frame in self._frames:
            score += frame.raw_score if frame.raw_score is not None else 0
        return score
