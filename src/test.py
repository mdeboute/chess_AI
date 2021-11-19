import time
import chess
from random import randint, choice
import math


def randomMove(b):
    '''Renvoie un mouvement au hasard sur la liste des mouvements possibles. Pour avoir un choix au hasard, il faut
    construire explicitement tous les mouvements. Or, generate_legal_moves() nous donne un itérateur.'''
    return choice([m for m in b.generate_legal_moves()])


board = chess.Board()
board_2 = chess.Board(
    "r1bqkb1r/ppppnpQp/8/8/4P3/8/PPP2PPP/RNB1KB1R b KQkq - 0 6")
# r1bqkbnr/pppp1ppp/8/8/3nP3/8/PPP2PPP/RNBQKB1R w KQkq - 0 5
# Q7/p3k3/7p/8/8/8/PPPP1PPP/RNBQKBNR b KQ - 0 15

# this function makes an exhaustive search of all the chess games by limiting the depth of
# the search by a search parameter with the chess library and return the number of possibilities


def exhaustiveSearch(board, depth):
    if depth == 0 or board.is_game_over():
        return 1
    else:
        count = 0
        for move in board.legal_moves:
            board.push(move)
            count += exhaustiveSearch(board, depth - 1)
            board.pop()
        return count


# start = time.time()
# print(exhaustiveSearch(board, 4))
# end = time.time()
# elapsed = end - start
# print(f'Execution time: {elapsed:.2}ms')


# print(board.piece_map().items())


# HEURISITQUE DE SHANNON VERSION 2

def formuleHeuristique(board):
    if(board.is_game_over()):
        return 0
    if board.is_checkmate():
        if (board.turn == chess.WHITE):
            return -math.inf
        if(board.turn == chess.BLACK):
            return math.inf
    heuristic = 0
    for n in board.piece_map():
        piece = board.piece_map()[n]
        score = 0
        if piece.piece_type == 1:
            score = 1
        elif piece.piece_type == 2 or piece.piece_type == 3:
            score = 3
        elif piece.piece_type == 4:
            score = 5
        elif piece.piece_type == 5:
            score = 9
        elif piece.piece_type == 6:
            score = 200
        if piece.color:
            heuristic += score
        else:
            heuristic -= score

    return heuristic


# print(board.piece_map()[2])
print(formuleHeuristique(board))


def MiniMax(board, depth):

    if (depth == 0 or board.is_game_over()):
        return formuleHeuristique(board), None

    if board.turn == chess.WHITE:
        maxEval = -math.inf
        best_move = None
        for move in board.generate_legal_moves():
            board.push(move)
            eval = MiniMax(board, depth-1)
            board.pop()
            if(eval > maxEval):
                maxEval = eval
                best_move = move
        return maxEval, best_move
    else:
        minEval = math.inf
        best_move = None
        for move in board.generate_legal_moves():
            board.push(move)
            eval = MiniMax(board, depth-1)
            board.pop()
            if(eval < minEval):
                minEval = eval
                best_move = move
        return minEval, best_move


print(MiniMax(board, 2))


# def minimax(board, depth, maximizingPlayer):

#   if (depth == 0 or board.is_game_over()):
#      return formuleHeuristique(board), None

# if (maximizingPlayer):
#    maxEval = -math.inf
#   best_move = None
#  for move in board.generate_legal_moves():
#     board.push(move)
#    eval = minimax(board, depth-1, False)
#   board.pop()
#  if(eval > maxEval):
#     maxEval = eval
#    best_move = move
# return maxEval, best_move
# else:
#   minEval = math.inf
#  best_move = None
# for move in board.generate_legal_moves():
#    board.push(move)
#   eval = minimax(board, depth-1, True)
#  board.pop()
# if(eval < minEval):
#    minEval = eval
#   best_move = move
# return minEval, best_move
#print(minimax(board, 3, True))


def alphaBeta(board, depth, alpha, beta, maximizingPlayer):
    if (depth == 0 or board.is_game_over()):
        return formuleHeuristique(board)
    if(maximizingPlayer):
        maxEval = -math.inf
        for move in board.generate_legal_moves():
            board.push(move)
            eval = alphaBeta(board, depth-1, alpha, beta, False)
            board.pop()
            maxEval = max(maxEval, eval)
            alpha = max(alpha, eval)
            if(beta <= alpha):
                break
            return maxEval
    else:
        minEval = math.inf
        for move in board.generate_legal_moves():
            board.push(move)
            eval = alphaBeta(board, depth-1, alpha, beta, True)
            board.pop()
            minEval = min(minEval, eval)
            beta = min(beta, eval)
            if(beta <= alpha):
                break
            return minEval


# print(alphaBeta(board, 3, math.inf, -math.inf, True))

# joueur aléatoire contre minimax niveau 3:

def match1(board):

    while board.is_game_over() != False:
        if board.turn == chess.WHITE:
            n_move = randomMove(board)
        else:
            n_move = MiniMax(board, 3)
        board.push(board)
    return n_move

# MiniMax niveau 1 contre MiniMax niveau 3:


def match2(board):

    while board.is_game_over() != False:
        if board.turn == chess.WHITE:
            n_move = MiniMax(board, 1)
        else:
            n_move = MiniMax(board, 3)
        board.push(board)
    return n_move
