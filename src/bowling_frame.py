
from __future__ import annotations
from socketserver import UnixStreamServer

from typing import Union
import unittest


class BowlingFrame():
    def __init__(self, *args, **kwargs):
        ''' This class represents a BowlingFrame within a bowling game.

        Keyword Args:
            frame_number(int): The frame number within the bowling game.
            successor(BowlingFrame): The frame that comes after this frame.

        '''
        self._frame_number = kwargs.get('frame_number', None)
        self._successor = kwargs.get('successor', None)
        self._first_shot_index = None
        self._shots = []

    @property
    def frame_number(self) -> int:
        '''int : returns the frame's number'''
        return self._frame_number

    @frame_number.setter
    def frame_number(self, value: int):
        '''None: Sets the frames number'''
        self._frame_number = value

    @property
    def successor(self) -> BowlingFrame:
        '''BowlingFrame : returns the successor bowling frame'''
        return self._successor

    @successor.setter
    def successor(self, value: BowlingFrame):
        '''BowlingFrame: Returns the frame that comes after this frame.'''
        self._successor = value

    def add_shot(self, pins_scored) -> None:
        '''None: Adds a shot to the frame and includes some error checking to
        ensure that the shot added is valid. It appends the shot to a class property on success.
        '''
        pins_scored = self.convert_pins_scored_from_string_to_int(pins_scored)
        self._check_shot_for_error(pins_scored)
        self._shots.append(pins_scored)

    def convert_pins_scored_from_string_to_int(self, pins_scored) -> int:
        '''int: Converts a string entered for the pins_scored to the proper integer value.

        Raises:
            ValueError: If the user passes a character that isn't recognized.
        '''
        if isinstance(pins_scored, str):
            if pins_scored.upper() == "X":
                pins_scored = 10
            elif (pins_scored == "/"):
                pins_scored = 10 - self._shots[0]
            else:
                error_msg = 'An invalid character was entered for the pins_scored'
                error_msg += f'pins_score = {pins_scored}'
                raise ValueError(error_msg)
        return pins_scored

    def _check_shot_for_error(self, shot: int) -> None:
        '''None: Delegates the error handling to sub functions.'''
        self._check_for_valid_shot_score(shot)
        self._check_correct_number_of_shots()
        self._check_combined_shot_total_for_errors(shot)

    def _check_for_valid_shot_score(self, shot: int) -> None:
        '''None: Error check to ensure the number of pins knocked down is in a the valid range [0, 10]

        Raises:
            ValueError: If the shot's score is smaller than 0 or greater than 10.
        '''
        if (shot < 0) or (shot > 10):
            error_message = "A valid shot must be in the range [0, 10]."
            error_message += f"shot = {shot}"
            raise ValueError(error_message)

    def _check_correct_number_of_shots(self) -> None:
        '''None: Ensures that a non-tenth frame doesn't have more than 2 shots.

        Raises:
            ValueError: If a shot is added after the frame is full.
        '''
        if self._frame_number < 10 and len(self._shots) == 2:
            error_msg = 'Non-Tenth bowling frames only allow two shots.'
            raise ValueError(error_msg)

    def _check_combined_shot_total_for_errors(self, shot):
        '''None: Ensures that a non-tenth frame doesn't have more than 10 total pins knocked
        down between the two shots.

        Raises:
            ValueError: The total of the two shots is greater than 10.
        '''
        if self._frame_number < 10 and len(self._shots) == 1:
            if sum(self._shots) + shot > 10:
                error_msg = 'For non-tenth frames shots should sum to a max of 10.'
                raise ValueError(error_msg)

    def get_shots(self, shot_numbers: list = None) -> list:
        '''A function to get shots from the frame.

        Args:
            shot_numbers(list): the shots to return as a list from this frame.

        Note:
            if no shot numbers are passed in this function will return all of the
            shots in this frame.

        Returns:
            list(int): A list of ints for each of the shots specified in the frame
        '''
        shots = self._shots
        if shot_numbers is not None:
            if len(self._shots) >= len(shot_numbers):
                shots = [self._shots[shot_number] for shot_number in shot_numbers]
        return shots

    @property
    def raw_score(self) -> Union[int, None]:
        '''Returns the score for the frame or None if it isn't calculated yet.'''
        return self.score_frame()

    def score_frame(self) -> int:
        '''int: Returns the frame's score using sub scoring functions for the special cases of
        a frame's score.'''
        frame_score = None
        if self.is_complete:
            if self.is_strike():
                frame_score = self.strike_frame_score()
            elif self.is_spare():
                frame_score = self.spare_frame_score()
            else:
                frame_score = self.open_frame_score()
        return frame_score

    def is_strike(self) -> Union[bool, None]:
        '''Returns a boolean indicating if this frame is a strike or None if it can't be calculated
        currently.'''
        return self._shots[0] == 10 if len(self._shots) > 0 else None

    def strike_frame_score(self) -> Union[int, None]:
        '''Scores a strike frame by adding 2 shots from successor frames.

        Note: If the successor is a strike as well this function will use the successor's successor
        to get the second shot.

        Returns:
            int or None: If the score can be calculated it will return an int otherwise this will return None.
        '''
        strike_frame_score = 10
        bonus_shots = [None, None]
        if self.successor.is_strike() is None:
            strike_frame_score = None
        elif (self.successor.is_strike()) and (self.successor.frame_number < 10):
            bonus_shots = self.successor.get_shots([0]) + self.successor.successor.get_shots([0])
        else:
            bonus_shots = self.successor.get_shots([0, 1])

        strike_frame_score = None
        if None not in bonus_shots and len(bonus_shots) == 2:
            strike_frame_score = 10 + sum(bonus_shots)
        return strike_frame_score

    def is_spare(self) -> Union[bool, None]:
        '''Returns a boolean indicating if this frame is a spare or None if it can't be calculated
        currently.'''
        return self._shots[0] + self._shots[1] == 10 if len(self._shots) >= 2 else None

    def spare_frame_score(self) -> Union[int, None]:
        '''Scores a spare frame by adding 1 shots from the successor frame.

        Returns:
            int or None: If the score can be calculated it will return an int otherwise this will return None.
        '''
        spare_frame_score = None
        if (self.frame_number < 10):
            first_successor_frame_shot = self.successor.get_shots([0])
            if first_successor_frame_shot:
                spare_frame_score = sum([10] + first_successor_frame_shot)
        return spare_frame_score

    def open_frame_score(self) -> Union[int, None]:
        ''' Scores an open frame by adding the scores from the two shots in the frame and
        returns None if it can't be calculated

        Return:
            int or None: int if the score can be calculated and None otherwise
        '''
        return self._shots[0] + self._shots[1] if len(self._shots) == 2 else None

    @property
    def is_complete(self):
        '''bool: Returns the completion status of the frame.'''
        return len(self._shots) == 1 if self.is_strike() else len(self._shots) == 2


class TenthBowlingFrame(BowlingFrame):
    def __init__(self, *args, **kwargs):
        '''A special type of BowlingFrame

        Note:
            The frame_number is not passed in for this Class.
        '''
        kwargs["frame_number"] = 10
        super().__init__(*args, **kwargs)

    def add_shot(self, pins_scored) -> None:
        '''This class modifies the add shot method to allow a third shot if the user gets a
        strike or a spare within the first two shots of this frame.

        Raises:
            ValueError: If the number of shots exceeds 3 if a spare or a strike is earned.
            ValueError: if the number of shots exceeds 2 for an open 10th frame.
        '''
        pins_scored = self.convert_pins_scored_from_string_to_int(pins_scored)
        strike_or_spare_checks = [self.is_spare(), self.is_strike()]
        if any(strike_or_spare_checks):
            if len(self._shots) >= 3:
                error_msg = 'The tenth bowling frame only allows three shots maximum.'
                raise ValueError(error_msg)
        else:
            if len(self._shots) >= 2:
                error_msg = 'The tenth bowling frame only allow three shots for strikes or spares.'
                raise ValueError(error_msg)
        self._shots.append(pins_scored)

    @BowlingFrame.successor.setter
    def successor(self, value: BowlingFrame):
        '''Modifies the successor setter to always set it to None as the 10th frame is the last frame.'''
        self._successor = None

    @property
    def raw_score(self) -> int:
        '''int: returns the score for the frame using the score_frame function.'''
        return self.score_frame()

    def score_frame(self) -> int:
        '''The score_frame function was modified to return the sum of all the shots in the 10th
        frame as it's the last frame and there are no more shots allowed after it.

        Returns:
            int: The sum of all the shots in the 10th frame.
        '''
        return sum(self._shots)

    def is_spare(self):
        return super().is_spare()

    def is_strike(self):
        return super().is_strike()

    @property
    def is_complete(self):
        '''bool: modifies the is_complete method to support more shots in the frame.'''
        return len(self._shots) == 3 if self.is_spare() or self.is_strike() else len(self._shots) == 2
