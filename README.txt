This project represents the development of a reinforcement agent to play simple
m,n,k games such as Tic-Tac-Toe.

Upper bound on complexity (number of states) for a 3x3 board is 3^9 = 19,683
(three states for each cell and nine cells).
Excluding illegal moves (e.g. five noughts and no crosses), the number of
possible states is 5478.
Most of these are rotations or reflections of other states; excluding these
gives 765 unique states.

The documentation follows the Google Python docstring style for readability,
and requires the Sphinx Napoleon extension for conversion to restructured text.
See:
https://sphinxcontrib-napoleon.readthedocs.org/en/latest/
http://google.github.io/styleguide/pyguide.html#Comments
