"""
This module contains methods to batch run the TicTacToe simulator with 
reinforcement learning agents. 
"""

from tictactoe import *
from players import *
from agents.reinforcement import *
from agents.minimax import *
import logging
import sys
import cProfile
import sys
import os
from datetime import datetime


def batch_run(game, runs):
    """
    Executes the game over a number of runs, displays the moving average results
    and optionally saves the results to a csv file.

    Args:
        game (TicTacToe): instance of the game to run
        runs (int): number of times to run the game
    Returns:
        string: csv of the results
    """
    # TODO: remove specific player refs and just store results for all players
    # in game.players() (Create a results class?)
    player_1 = game.players()[0]
    player_2 = game.players()[1]

    # Set up the MOEs
    player_1_wins = 0
    player_2_wins = 0
    total_draws = 0
    total_played = 0
    results = ""

    # Batch run the game
    for _ in range(0, runs):
        winner = game.run()

        if not winner:
            total_draws += 1
        elif winner is player_1.side:
            player_1_wins += 1
        elif winner is player_2.side:
            player_2_wins += 1
        else:
            raise ValueError("Unexpected winner: {0}".format(winner))

        # Update MOEs
        total_played += 1
        if total_played % 100 == 0:
            print "Total games: {}  Moving average: {}% {}% {}%  Bias={}  States={}".format(
                    total_played, player_1_wins / 1, total_draws / 1, player_2_wins / 1,
                    player_1.bias, len(player_1.state_values))

            results += "{}, {}, {}, {}\n".format(total_played,
                player_1_wins / 1, total_draws / 1, player_2_wins / 1)

            total_draws = 0
            player_1_wins = 0
            player_2_wins = 0

    # Uncomment to print the recorded states and associated values
    # print "Agent state values:"
    # for array, value in player_1.state_values_list():
    #     print "{0}\nValue: {1}\n".format(rules.board_str(array), value)

    # Print the training results
    print "Player 1: {0}\nPlayer 2: {1}\nDraw: {2}\nTotal: {3}".format(
        player_1_wins, player_2_wins, total_draws, total_played)
    print "Number of states stored for Agent: {0}".format(len(
        player_1.state_values))

    return results


def main():
    # Set up the logger
    logger = logging.getLogger()
    logging.basicConfig(stream=sys.stdout, level=logging.FATAL,
            format="\n%(message)s")

    # Create the players
    agent = ReinforcementAgent2(logger=logger)
    trainer = WinBlockRandomCellAgent(logger=logger)
    human = Human(logger=logger)

    # Set up the game
    game = TicTacToe([agent, trainer], shuffle=False, logger=logger)
    results = "Runs, Player 1, Draw, Player 2\n"

    # Train the agent against the simple agent
    results += batch_run(game, 20000)

    # Reduce bias
    agent.bias = 0.5
    results += batch_run(game, 5000)

    # Reduce bias
    agent.bias = 0.2
    results += batch_run(game, 5000)

    # Once the state values have converged stop exploring
    agent.bias = 0
    results += batch_run(game, 1000)

    # Use optimal minimax agent
    agent.bias = 0
    trainer = MiniMaxAgent(logger=logger)
    game.set_players([agent, trainer])
    results += batch_run(game, 300)

    # Write results to file
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    if not os.path.exists("results"):
        os.makedirs("results")
    with open("results\Results_{}.csv".format(timestamp), "w") as text_file:
        text_file.write(results)

    # Insert a human player
    logger.setLevel(logging.INFO)
    player_2 = human
    game.set_players([agent, human])
    while True:
        game.run()


if __name__ == "__main__":
    main()
