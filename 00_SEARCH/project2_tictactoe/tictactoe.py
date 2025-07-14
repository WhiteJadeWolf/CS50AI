"""
Tic Tac Toe Player
"""

import math

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
    if [ele for nested in board for ele in nested].count(EMPTY) % 2 == 0:
        return O
    else:
        return X


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    s = set()
    for i in range(3):
        for j in range(3):
            if board[i][j] == EMPTY:
                s.add((i,j))
    return s


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    newboard = [nested[:] for nested in board]
    i, j = action
    if board[i][j] != EMPTY:
        raise Exception("Invalid Action")
    else:
        newboard[i][j] = player(newboard)
        return newboard


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    win = False
    
    for i in range(3):
        if board[i].count(board[i][0]) == 3:
            win = True
            return board[i][0]
        counter = 1
        for j in range(3):
            if j == 0:
                temp = board[j][i]
            elif temp == board[j][i]:
                counter += 1
        if counter == 3:
            win = True
            return board[0][i]
        
    if (board[0][0] == board[1][1] == board[2][2]) or (board[0][2] == board[1][1] == board[2][0]):
        win = True
        return board[1][1]
    
    if not win:
        return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    if winner(board) is not None or not(EMPTY in [ele for nested in board for ele in nested]):
        return True
    else:
        return False


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    if winner(board) == X:
        return 1
    elif winner(board) == O:
        return -1
    else:
        return 0


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    if terminal(board):
        return None
    
    bestmove = None
    bestval = -2 if player(board) == X else 2
    
    for action in actions(board):
        newboard = result(board, action)
        val = minval(newboard) if player(board) == X else maxval(newboard)  # simply means player(newboard) == O and it aims to minimize utility
        if player(board) == X and val > bestval:
            bestmove = action
            bestval = val
        elif player(board) == O and val < bestval:
            bestmove = action
            bestval = val
    return bestmove        

def maxval(board):
    if terminal(board):
        return utility(board)
    v = -2
    for action in actions(board):
        v = max(v, minval(result(board, action)))
    return v

def minval(board):
    if terminal(board):
        return utility(board)
    v = 2
    for action in actions(board):
        v = min(v, maxval(result(board, action)))
    return v