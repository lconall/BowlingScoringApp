
from src.bowling_game import BowlingGame


class BowlingScoringApp():
    def __init__(self, *args, **kwargs):
        self._bowling_game = BowlingGame()
        self._bowler_name = {}

    def score_user_shots(self):
        shots = self._get_user_input()
        for shot in shots:
            shot = int(shot) if shot.isnumeric() else shot
            self._bowling_game.add_shot(shot)
        self._display_shots_and_frame_totals()
        self.create_frame_string()

    def _get_user_input(self):
        input_message = "Welcome to the Levi Conall's Bowling Scoring Application!\n\n"
        input_message += "Please enter a list of shots you would like to score.\n"
        input_message += "Note: Please use commas as delimiters.\n"
        input_message += "X or 10 is a Srike, / can be used for spares.\n\n"
        input_message += "First Name: "
        self._bowler_name["first_name"] = input(input_message)
        self._bowler_name["last_name"] = input("Last Name: ")
        shots = input("Shots: ")
        shots = shots.replace(" ", "")
        shots = shots.split(",")
        return shots

    def _display_shots_and_frame_totals(self):
        shots_by_frame = self._bowling_game.get_shots_by_frame()
        cumulative_score_by_frame = self._bowling_game.cumulative_score_by_frame
        frame_number = 1
        display_lines = self.create_frame_string()
        for frame_shots, cumulative_score_for_frame in zip(shots_by_frame, cumulative_score_by_frame):
            new_frame_strings = self.create_bowling_frame_string(frame_number, cumulative_score_for_frame, *frame_shots)
            display_lines = [current_line + new_frame_string for current_line, new_frame_string in zip(display_lines, new_frame_strings)]
            frame_number += 1
        final_score_strings = self.create_final_score_string(self._bowling_game.final_score)
        display_lines = [current_line + new_frame_string for current_line, new_frame_string in zip(display_lines, final_score_strings)]

        for display_line in display_lines:
            print(display_line)

    def create_frame_string(self):
        bowler_initials = f"{self._bowler_name['first_name'][0]}{self._bowler_name['last_name'][0]}".upper()
        display_lines = [None] * 9
        display_lines[0] = "+" + "-" * 11 + "+"
        display_lines[1] = "|" + " Initials: " + "|"
        display_lines[2] = "+" + "-" * 11 + "+"
        display_lines[3] = "|" + " " * 11 + "|"
        display_lines[4] = "|" + " " * 11 + "|"
        display_lines[5] = "|" + " " * 4 + bowler_initials + " " * 5 + "|"
        display_lines[6] = "|" + " " * 11 + "|"
        display_lines[7] = "|" + " " * 11 + "|"
        display_lines[8] = "+" + "-" * 11 + "+"
        return display_lines

    def create_bowling_frame_string(self, frame_number, cumulative_score, shot1=None, shot2=None, shot3=None):
        frame_num_string = " " if frame_number < 10 else ""
        frame_num_string += f"{frame_number}"
        cumulative_score_str = f"{cumulative_score}"
        cumulative_score_spaces = 7 - len(cumulative_score_str) - 1
        display_lines = [None] * 9
        display_lines[0] = "+" + "-" * 11 + "+"
        display_lines[1] = "|" + " " * 5 + f"{frame_num_string}" + " " * 4 + "|"
        display_lines[2] = "+" + "-" * 11 + "+"
        display_lines[3], display_lines[4], display_lines[5] = self.create_shots_string_for_frame(frame_number, shot1, shot2, shot3)
        display_lines[6] = "|" + " " * 11 + "|"
        display_lines[7] = "|" + " " * 5 + f"{cumulative_score}" + " " * cumulative_score_spaces + "|"
        display_lines[8] = "+" + "-" * 11 + "+"
        return display_lines

    def create_shots_string_for_frame(self, frame_number, shot1=None, shot2=None, shot3=None):
        shots_line1 = f"|     |     |" if frame_number < 10 else f"|   |   |   |"
        shots_line2 = f"|     |     |" if frame_number < 10 else f"|   |   |   |"
        shots_line3 = f"|     +-----+" if frame_number < 10 else f"|---+---+---+"

        if frame_number == 10:
            shots_line2 = f"| {shot1} | {shot2} | {shot3} |"
            shots_line2 = shots_line2.replace("10", "X")
        else:
            if shot1 == 10:
                shots_line2 = f"|     |  X  |"
            elif shot1 is not None:
                if shot2 is not None:
                    if shot1 + shot2 == 10:
                        shots_line2 = f"|  {shot1}  |  /  |"
                    else:
                        shots_line2 = f"|  {shot1}  |  {shot2}  |"
                else:
                    shots_line2 = f"|  {shot1}  |     |"
        shots_line2 = shots_line2.replace("None", " ")
        return shots_line1, shots_line2, shots_line3

    def create_final_score_string(self, final_score):
        final_score_str = f"{final_score}"
        display_lines = [None] * 9
        display_lines[0] = "+" + "-" * 11 + "+"
        display_lines[1] = "|Final Score|"
        display_lines[2] = "+" + "-" * 11 + "+"
        display_lines[3] = "|" + " " * 11 + "|"
        display_lines[4] = "|" + " " * 11 + "|"
        display_lines[5] = "|" + " " * 4 + final_score_str + " " * (6 - len(final_score_str) + 1) + "|"
        display_lines[6] = "|" + " " * 11 + "|"
        display_lines[7] = "|" + " " * 11 + "|"
        display_lines[8] = "+" + "-" * 11 + "+"
        return display_lines


if __name__ == "__main__":
    bowling_scoring_app = BowlingScoringApp()
    bowling_scoring_app.score_user_shots()
