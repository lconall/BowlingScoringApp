# BowlingScoringApplication
## Author: Levi Conall <Levi.Conall@gmail.com>
---
### Description:
This application is a submittal to a coding challenge to build an application that can score a list bowling shots.

### Methoology:
My methodology diagraming out the core components for the application to be designed. I started with the idea for a BowlingGame class and a Bowling Frame class. After I had an initial design thought in mind my next step is to look for resources online to see if the problem or something similar has been solved before. I know for a fact this problem has been solved and an author I follow (Robert C. Martin) has a TDD practice for it on his blog (http://butunclebob.com/ArticleS.UncleBob.TheBowlingGameKata). As a result, I thought It would a good starting place to use his teaching material as a practice and to get me started on writing the app.

After I finished the exercise. I had a functional code block that scored a game, but I didn't feel it would not have met the requirements for the challenge I was given so I thought I would refactor the work I had done and expand upon it adding in error handling and more robust logic.

### Dependencies:
python == 3.7
### Installing the App:
This application only needs pure python to run, but for testing purposes I've created a environment.yml that has my testing dependencies.

The main libraries I utilize are:
- pytest: for testing
- sphinx-docs: for autodoc generation

### Running the App:
To run this application please make sure that you have python installed.
0) Install python
1) Navigate to the root directory in this repo via your command line or terminal
2) In the your terminal run  `python bowling_scoring_app.py`

### Running the Unit Tests:
To install the conda environment use the following command in your terminal
0) Install Anaconda
1) Navigate to the root directory in this repo via your command line or terminal
2) In the your terminal run `conda env create --file=environment.yaml`
3) After the conda environment is setup run `python -m pytest` in the root directory

### Next Steps:
If I were to continue to work on this application more there would be a few things I would modify
1) Move the app to a more clean archecture with an input/output boundary interface so that there is a standard interface for interacting with the app.
2) Build 2 display mechanism layers ontop of the boundaries as an example of the dependency inversion principle.
    a) I would convert the code that displays the app via command line into one
    b) I would create a web application display mechanism (most likely react.js) to show a different style interface
