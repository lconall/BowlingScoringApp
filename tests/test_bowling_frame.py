
import pytest
import random

from tests.pytest_base import PytestBase

from src.bowling_frame import BowlingFrame, TenthBowlingFrame


class TestBowlingFrame(PytestBase):

    def test_createBowlingFrame(self):
        bowling_frame = BowlingFrame()
        assert isinstance(bowling_frame, object)

    @pytest.mark.parametrize('frame_number', [(1), (2), (3), (4), (5), (6), (7), (8), (9), (10)])
    def test_frameNumberProperty(self, frame_number):
        bowling_frame = BowlingFrame(frame_number=frame_number)
        bowling_frame.frame_number = frame_number
        assert bowling_frame.frame_number == frame_number

    def test_addSingleGutterShot(self):
        frame1 = BowlingFrame(frame_number=1)
        frame1.add_shot(0)
        assert frame1.get_shots([0]) == [0]

    def test_addSingleScoringShot(self):
        frame1 = BowlingFrame(frame_number=1)
        frame1.add_shot(1)
        assert frame1.get_shots([0]) == [1]

    def test_setSuccessorFrame(self):
        frame1 = BowlingFrame(frame_number=1)
        frame2 = BowlingFrame(frame_number=2)
        frame1.successor = frame2
        assert frame1.successor == frame2

    def test_setFrameRawScore_spare(self):
        frame1 = BowlingFrame(frame_number=1)
        frame2 = BowlingFrame(frame_number=2)
        frame1.successor = frame2

        frame1.add_shot(5)
        frame1.add_shot(5)
        assert frame1.raw_score is None

        frame2.add_shot(5)

        assert frame1.raw_score == 15

    def test_setFrameRawScore_strike(self):
        frame1 = BowlingFrame(frame_number=1)
        frame2 = BowlingFrame(frame_number=2)
        frame1.successor = frame2

        frame1.add_shot(10)
        assert frame1.raw_score is None

        frame2.add_shot(5)
        frame2.add_shot(5)

        assert frame1.raw_score == 20

    def test_setFrameRawScore_TurkeyFrames(self):
        frame1 = BowlingFrame(frame_number=1)
        frame2 = BowlingFrame(frame_number=2)
        frame3 = BowlingFrame(frame_number=3)
        frame1.successor = frame2
        frame2.successor = frame3

        frame1.add_shot(10)
        assert frame1.raw_score is None

        frame2.add_shot(10)
        assert frame1.raw_score is None

        frame3.add_shot(10)
        assert frame1.raw_score == 30

    def test_setFrameRawScore_9thAnd10thFrames(self):
        frame10 = TenthBowlingFrame()

        frame9 = BowlingFrame(frame_number=9,
                              successor=frame10
                              )

        frame9.add_shot(10)
        assert frame9.raw_score is None

        frame10.add_shot(10)
        assert frame9.raw_score is None

        frame10.add_shot(10)
        assert frame9.raw_score == 30

        frame10.add_shot(10)
        assert frame10.raw_score == 30

    def test_addToManyShotsToNonTenthFrame(self):
        frame1 = BowlingFrame(frame_number=1,
                              successor=None
                              )
        frame1.add_shot(1)
        frame1.add_shot(1)
        expected_error_message = 'Non-Tenth bowling frames only allow two shots.'
        with pytest.raises(ValueError) as error:
            frame1.add_shot(1)
        assert expected_error_message == str(error.value)

    def test_addTooManyShotsToNonTenthFrame_OpenFrame(self):
        frame10 = TenthBowlingFrame()
        frame10.add_shot(1)
        frame10.add_shot(3)
        assert frame10.is_complete

        expected_error_message = 'The tenth bowling frame only allow three shots for strikes or spares.'
        with pytest.raises(ValueError) as error:
            frame10.add_shot(1)
        assert expected_error_message == str(error.value)

    @pytest.mark.parametrize('shots', [([5, 5, 1, 3]),
                                       (10, 1, 2, 3)])
    def test_addTooManyShotsToTenthFrame_strikeOrSpare(self, shots):
        frame10 = TenthBowlingFrame()
        for shot in shots[0:-1]:
            frame10.add_shot(shot)
        print(frame10._shots)
        assert frame10.is_complete

        expected_error_message = 'The tenth bowling frame only allows three shots maximum.'
        with pytest.raises(ValueError) as error:
            frame10.add_shot(shots[3])
        assert expected_error_message == str(error.value)

    def test_setSuccessorAlwaysReturnsNoneForTenthFrame(self):
        frame10 = TenthBowlingFrame()
        frame10.successor = "Should return None regardless."
        frame10.add_shot(1)
        frame10.add_shot(3)
        assert frame10.successor is None

    @pytest.mark.parametrize('shots', [([5, 5, 5]), (10, 10, 10)])
    def test_tenthFrameIsComplete_nonOpenFrame(self, shots):
        frame10 = TenthBowlingFrame()
        for shot in shots:
            frame10.add_shot(shot)
        assert frame10.is_complete

    def test_tenthFrameIsComplete_OpenFrame(self):
        frame10 = TenthBowlingFrame()
        frame10.add_shot(1)
        frame10.add_shot(3)
        assert frame10.is_complete
