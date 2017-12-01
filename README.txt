This project represents the development of a reinforcement agent to play simple
m,n,k games such as Tic-Tac-Toe.

It provides a simulation engine to model the flow of a game, requesting moves
from each player in turn and storing the state of the game board.

The test_rl_agents module contains methods to batch run the TicTacToe simulator
with reinforcement learning agents.

`Wikipedia <https://en.wikipedia.org/wiki/M,n,k-game>`_:
"An m,n,k-game is an abstract board game in which two players take turns in
placing a stone of their color on an m*n board, the winner being the player
who first gets k stones of their own color in a row, horizontally,
vertically, or diagonally. Thus, tic-tac-toe is the 3,3,3-game and
free-style gomoku is the 19,19,5-game. m,n,k-game is also called a
k-in-a-row game on m*n board."

The upper bound on complexity (number of states) for a 3x3 board is 3^9 = 19,683
(three states for each cell and nine cells). Excluding illegal moves (e.g. five
noughts and no crosses), the number of possible states is 5478. Most of these
are rotations or reflections of other states; excluding these gives 765 unique
states.

The documentation follows the Google Python docstring style for readability,
and requires the Sphinx Napoleon extension for conversion to restructured text.
See https://sphinxcontrib-napoleon.readthedocs.org/en/latest/ and
http://google.github.io/styleguide/pyguide.html#Comments
