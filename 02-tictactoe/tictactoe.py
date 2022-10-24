"""
Tic Tac Toe Player
"""

import math
import copy
import random

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    count_x = 0
    count_o = 0
    for row in board:
        count_x += row.count(X)
        count_o += row.count(O)

    if count_x > count_o:
        return O

    return X


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    available_actions = []
    for i in range(3):
        for j in range(3):
            if board[i][j] is None:
                available_actions.append( (i, j) )
    return available_actions


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    if action is None:
        return board

    if board[action[0]][action[1]] is not None:
        raise Exception('Action not allowed')

    mark = player(board)
    board[action[0]][action[1]] = mark
    return board


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    if terminal(board):
        return three_on_line(board)

    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    if three_on_line(board) is not None:
        return True

    # validate board it's not full
    full = True
    for row in board:
        if row.count(EMPTY) > 0:
            full = False

    return full


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    if terminal( board ):
        aux = winner( board )

        if aux is None:
            return 0
        elif aux == X:
            return 1
        else:
            return -1
    else:
        return 0


def three_on_line(board):
    """
    Return who done 3 on line
    """
    # validate all rows
    for row in board:
        if row.count(X) == 3:
            return X
        if row.count(O) == 3:
            return O

    # validate all columns
    for i in range(3):
        if board[1][i] is not None and board[0][i] == board[1][i] == board[2][i]:
            return board[1][i]

    # validate diagonal
    if board[1][1] is not None:
        if board[0][0] == board[1][1] == board[2][2]:
            return board[1][1]
        if board[0][2] == board[1][1] == board[2][0]:
            return board[1][1]


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    ia_player = player(board)
    is_maximizing = False
    evaluate = math.inf
    test = -10
    if ia_player == X:
        is_maximizing = True
        evaluate = -math.inf
        test = 10

    for current_action in actions(board):
        board = result(board, current_action)
        score = evaluate_minimax(board, is_maximizing, test)
        board[current_action[0]][current_action[1]] = EMPTY

        print(current_action, score)

        if ia_player == X:
            if score > evaluate:
                evaluate = score
                best_movement = current_action
            elif score == 1:
                evaluate = score
                best_movement = current_action
        else:
            if score < evaluate:
                evaluate = score
                best_movement = current_action

    print( 'best movement', best_movement, score)

    return best_movement


def evaluate_minimax(board, is_maximizing, memory):

    if terminal(board):
        return utility(board)

    available_actions = actions(board)
    scores = []
    for current_action in available_actions:
        board = result(board, current_action)
        if is_maximizing:
            scores.append( max(-math.inf, evaluate_minimax(board, not is_maximizing, memory)) )
        else:
            scores.append( min(math.inf, evaluate_minimax(board, not is_maximizing, memory)) )
        board[current_action[0]][current_action[1]] = EMPTY

    if is_maximizing:
        return memory + max( scores )
    else:
        return memory + min( scores )



