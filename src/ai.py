# AI to pick best move based on board state, minimax + alpha-beta pruning
# TODO: Find all possible moves
# TODO: Check if move results in a win or draw/full board
# TODO: Minimax (Recursive)
# TODO: Maximizing Player
# TODO: Determine heuristic(s) for evaluating game position
#           - Num of 2, and 3 in a rows on board
#           - 3 in a rows that can be created in 1 move, w/ an open connect 4 sq
#           - Determine weights. self-tuning? Can play against itself until it beats itself, then iterate until
#                   weights seem to stagnate (?)
#           - Research potential connect 4 heuristics
# TODO: Evaluate + select best option
# TODO: Create visuals for the algorithm. Display the process of selecting.
        # - tree search visual, where one player is maximizing on their turn and other minimizing to determine best move
# TODO: Encapsulate all AI logic into a class so I can have them self-tune

import random
import copy
from game import Connect4

def get_valid_columns(board):
    return [col for col in range(len(board[0])) if board[0][col] == 0]

def is_terminal_node(board, game):
    return game.check_win(1) or game.check_win(2) or len(get_valid_columns(board)) == 0

def minimax(board, depth, alpha, beta, maximizingPlayer, game):
    valid_columns = get_valid_columns(board)
    is_terminal = is_terminal_node(board, game)

    if depth == 0 or is_terminal:
        if is_terminal:
            if game.check_win(1):
                return (None, 1000)
            elif game.check_win(2):
                return (None, -1000)
            else:
                return (None, 0)
        else:
            # TODO: Implement Scoring Function
            return (None, score_position(board, 1))

    if maximizingPlayer:
        value = -float('inf')
        column = random.choice(valid_columns)
        for col in valid_columns:
            board_copy = copy.deepcopy(board)
            game.drop_disc(col, board_copy, 1)
            new_score = minimax(board_copy, depth-1, alpha, beta, False, game)[1]
            if new_score > value:
                value = new_score
                column = col
            alpha = max(alpha, value)
            if alpha >= beta:
                break
        return column, value
    else:                           # Minimizing Player
        value = float('inf')
        column = random.choice(valid_columns)
        for col in valid_columns:
            board_copy = copy.deepcopy(board)
            game.drop_disc(col, board_copy, 2)
            new_score = minimax(board_copy, depth-1, alpha, beta, True, game)[1]
            if new_score < value:
                value = new_score
                column = col
            beta = min(beta, value)
            if alpha >= beta:
                break
        return column, value
    


def score_position(board, player):
    score = 0
    def two_in_row(board, player):              # Return number of 2 in a row
        pass
    def open_three_in_row(board, player):             # Return number of 3 in a row
        pass
    def one_ply_three_in_row(board, player):    # Return number of ways to create a three in a row in one move
        pass                                        # If moving to some pos. creates 3 open spots where a 4 in a row could be acheived, count etc.
    
    return score


def ai_move(game):
    pass

