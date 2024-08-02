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
            # TODO: Implement Scoring/Heuristic Function
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
    
def check_patterns(board, player):
    rows = len(board)
    cols = len(board[0])
    center_col = cols // 2
    count_two = 0
    count_three = 0
    total_pieces = 0
    num_center = 0
    num_adj = 0
    used_indices = set()

    for row in range(rows):
        for col in range(cols):
            # Count the number of pieces on the board
            if board[row][col] == player:
                total_pieces += 1
                if col == center_col:
                    num_center += 1
                elif col == center_col + 1 or col == center_col - 1:
                    num_adj += 1

            # Check horizontal for three-in-a-row first
            if col <= cols - 4:
                indices = [(row, col), (row, col+1), (row, col+2)]
                if all(index not in used_indices for index in indices):
                    sequence = [board[row][col], board[row][col+1], board[row][col+2]]
                    adjacent1 = board[row][col+3] if col+3 < cols else -1
                    if sequence.count(player) == 3 and adjacent1 == 0:
                        count_three += 1
                        used_indices.update(indices)

            # Check vertical for three-in-a-row first
            if row <= rows - 4:
                indices = [(row, col), (row+1, col), (row+2, col)]
                if all(index not in used_indices for index in indices):
                    sequence = [board[row][col], board[row+1][col], board[row+2][col]]
                    adjacent1 = board[row+3][col] if row+3 < rows else -1
                    if sequence.count(player) == 3 and adjacent1 == 0:
                        count_three += 1
                        used_indices.update(indices)

            # Check positively sloped diagonal for three-in-a-row first
            if row <= rows - 4 and col <= cols - 4:
                indices = [(row, col), (row+1, col+1), (row+2, col+2)]
                if all(index not in used_indices for index in indices):
                    sequence = [board[row][col], board[row+1][col+1], board[row+2][col+2]]
                    adjacent1 = board[row+3][col+3] if row+3 < rows and col+3 < cols else -1
                    if sequence.count(player) == 3 and adjacent1 == 0:
                        count_three += 1
                        used_indices.update(indices)

            # Check negatively sloped diagonal for three-in-a-row first
            if row >= 3 and col <= cols - 4:
                indices = [(row, col), (row-1, col+1), (row-2, col+2)]
                if all(index not in used_indices for index in indices):
                    sequence = [board[row][col], board[row-1][col+1], board[row-2][col+2]]
                    adjacent1 = board[row-3][col+3] if row-3 >= 0 and col+3 < cols else -1
                    if sequence.count(player) == 3 and adjacent1 == 0:
                        count_three += 1
                        used_indices.update(indices)

    # Check for two-in-a-row after three-in-a-row
    for row in range(rows):
        for col in range(cols):
            # Check horizontal for two-in-a-row
            if col <= cols - 3:
                indices = [(row, col), (row, col+1)]
                if all(index not in used_indices for index in indices):
                    sequence = [board[row][col], board[row][col+1]]
                    adjacent1 = board[row][col+2] if col+2 < cols else -1
                    adjacent2 = board[row][col-1] if col-1 >= 0 else -1
                    if sequence.count(player) == 2:
                        if adjacent1 == 0:
                            count_two += 1
                        if adjacent2 == 0:
                            count_two += 1

            # Check vertical for two-in-a-row
            if row <= rows - 3:
                indices = [(row, col), (row+1, col)]
                if all(index not in used_indices for index in indices):
                    sequence = [board[row][col], board[row+1][col]]
                    adjacent1 = board[row+2][col] if row+2 < rows else -1
                    if sequence.count(player) == 2 and adjacent1 == 0:
                        count_two += 1

            # Check positively sloped diagonal for two-in-a-row
            if row <= rows - 3 and col <= cols - 3:
                indices = [(row, col), (row+1, col+1)]
                if all(index not in used_indices for index in indices):
                    sequence = [board[row][col], board[row+1][col+1]]
                    adjacent1 = board[row+2][col+2] if row+2 < rows and col+2 < cols else -1
                    adjacent2 = board[row-1][col-1] if row-1 >= 0 and col-1 >= 0 else -1
                    if sequence.count(player) == 2:
                        if adjacent1 == 0:
                            count_two += 1
                        if adjacent2 == 0:
                            count_two += 1

            # Check negatively sloped diagonal for two-in-a-row
            if row >= 2 and col <= cols - 3:
                indices = [(row, col), (row-1, col+1)]
                if all(index not in used_indices for index in indices):
                    sequence = [board[row][col], board[row-1][col+1]]
                    adjacent1 = board[row-2][col+2] if row-2 >= 0 and col+2 < cols else -1
                    adjacent2 = board[row+1][col-1] if row+1 < rows and col-1 >= 0 else -1
                    if sequence.count(player) == 2:
                        if adjacent1 == 0:
                            count_two += 1
                        if adjacent2 == 0:
                            count_two += 1

    return count_two, count_three, total_pieces, num_center, num_adj
                
def score_position(board, player, weights=None, column_weights=None):
    if weights is None:
        weights = {
            'total_pieces': 0.1,
            'count_two': 0.3,
            'count_three': 0.9,
        }

    if column_weights is None:
        column_weights = {
            'center': 0.15,
            'adjacent': 0.125,
        }

    count_two, count_three, total_pieces, num_center, num_adj = check_patterns(board, player)

    score = (total_pieces * weights.get('total_pieces') +
             count_two * weights.get('count_two') +
             count_three * weights.get('count_three') +
             num_center * column_weights.get('center') +
             num_adj * column_weights.get('adjacent'))
    
    score = round(score, 3)
    return score


def ai_move(game):
    pass

# board = [
#     [0, 0, 0, 0, 0, 0, 0],
#     [0, 0, 0, 0, 0, 0, 0],
#     [0, 0, 0, 0, 0, 0, 2],
#     [0, 0, 0, 0, 0, 1, 0],
#     [0, 0, 0, 0, 1, 0, 0],
#     [0, 0, 0, 1, 0, 0, 0]
# ]

# player = 1

# print(score_position(board, player))

#EV: 3 two-inna-rows, + 3 pieces total
# 3 * 0.3 + 3 * 0.1
#  0.9 + 0.3 = 1.2 

# 1.475
# .575