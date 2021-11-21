import time
import chess
from random import randint, choice
import math


def randomMove(b):
    '''Renvoie un mouvement au hasard sur la liste des mouvements possibles. Pour avoir un choix au hasard, il faut
    construire explicitement tous les mouvements. Or, generate_legal_moves() nous donne un itérateur.'''
    return choice([m for m in b.generate_legal_moves()])


def deroulementRandom(b):
    '''Déroulement d'une partie d'échecs au hasard des coups possibles. Cela va donner presque exclusivement
    des parties très longues et sans gagnant. Cela illustre cependant comment on peut jouer avec la librairie
    très simplement.'''
    print("----------")
    print(b)
    if b.is_game_over():
        print("Resultat : ", b.result())
        return
    b.push(randomMove(b))
    deroulementRandom(b)
    b.pop()


board = chess.Board(
    "r1bqkbnr/pppp1ppp/8/8/3nP3/8/PPP2PPP/RNBQKB1R w KQkq - 0 5")
board_2 = chess.Board(
    "r1bqkb1r/ppp2p1p/3p1p2/8/3QP1n1/8/PPP3PP/RNB1KB1R w KQkq - 0 9")
# r1bqkbnr/pppp1ppp/8/8/3nP3/8/PPP2PPP/RNBQKB1R w KQkq - 0 5
# Q7/p3k3/7p/8/8/8/PPPP1PPP/RNBQKBNR b KQ - 0 15

# this function makes an exhaustive search of all the chess games by limiting the depth of
# the search by a search parameter with the chess library and return the number of possibilities


# 2-1


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


#start = time.time()
#print(exhaustiveSearch(board, 4))
#end = time.time()
#elapsed = end - start
#print(f'Execution time: {elapsed:.2}ms')


# print(board.piece_map().items())


# 2-2 HEURISITQUE DE SHANNON

# chess.SQUARES =[chess.A1,chess.]
chess.A8
chess.B8
chess.C8
chess.D8
chess.E8
chess.F8
chess.G8
chess.H8

# calculer la distance entre le pion est la fin du plateau
# si le pion est à la fin on retourne 8 sinon
# on avance le pion d'une case

# def preference(board):
#   for n in board.piece_map():
#      piece = board.piece_map()[n]
#     if(piece.piece_type==1):
#        chess.square_name
#       if(board.square_distance(piece,chess.A8)!=0):


def formuleHeuristique(board):
    if(board.is_game_over()):
        return -math.inf
    if board.is_checkmate():
        if (board.turn == chess.WHITE):
            return -math.inf
        if(board.turn == chess.BLACK):
            return math.inf
    if board.is_stalemate():
        return 0
    # if board.square_distance()
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
# print(formuleHeuristique(board_2))
nbNoeuds = 0

# 2-3 MINIMAX


def MiniMax(board, depth, compter=False):
    global nbNoeuds
    if compter:
        nbNoeuds += 1
    if (depth == 0 or board.is_game_over()):
        return formuleHeuristique(board), None

    if board.turn == chess.WHITE:
        maxEval = -math.inf
        best_move = None
        for move in board.generate_legal_moves():
            board.push(move)
            eval = MiniMax(board, depth-1, compter)[0]
            board.pop()
            if(eval > maxEval):
                maxEval = eval
                best_move = move
        return maxEval, best_move, nbNoeuds
    else:
        minEval = math.inf
        best_move = None
        for move in board.generate_legal_moves():
            board.push(move)
            eval = MiniMax(board, depth-1, compter)[0]
            board.pop()
            if(eval < minEval):
                minEval = eval
                best_move = move
        return minEval, best_move, nbNoeuds


#print(MiniMax(board_2, 2))

# 2-4 GAMES

# joueur aléatoire contre minimax niveau 3:


def match1(board, depth):
    if board.is_game_over():
        print("Resultat : ", board.result())
        return
    if board.turn == chess.WHITE:
        e, move, n = MiniMax(board, depth)
        board.push(move)
        match1(board, depth)
        board.pop()
    if board.turn == chess.BLACK:
        board.push(randomMove(board))
        match1(board, depth)
        board.pop()


#print(match1(board, 3))


# def preference(board):
#   for move in board.piece_map():
#      piece = board.piece_map()[move.to_square]
#     if piece.piece_type == 1:
#        return 8
# else:
#   return 0


# MiniMax niveau 1 contre MiniMax niveau 3:


def match2(board):
    move = None
    while board.is_game_over() != False:
        if board.turn == chess.WHITE:
            move = MiniMax(board, 1)
            board.push(move)
        else:
            move = MiniMax(board, 3)
            board.push(move)
        board.pop()
    if board.is_game_over():
        print("Resultat : ", board.result())
        return


# print(match2(board))

# 3-1 ALPHA-BETA


def alphaBeta(board, depth, alpha, beta, compter=False):
    global nbNoeuds
    if compter:
        nbNoeuds += 1
    if (depth == 0 or board.is_game_over()):
        return formuleHeuristique(board), None
    if board.turn == chess.WHITE:
        maxEval = -math.inf
        best_move = None
        for move in board.generate_legal_moves():
            board.push(move)
            eval = alphaBeta(board, depth-1, alpha, beta, compter)[0]
            board.pop()
            if(eval > maxEval):
                maxEval = eval
                best_move = move
            alpha = max(alpha, eval)
            if(beta <= alpha):
                break
        return maxEval, best_move, nbNoeuds
    else:
        minEval = math.inf
        best_move = None
        for move in board.generate_legal_moves():
            board.push(move)
            eval = alphaBeta(board, depth-1, alpha, beta, compter)[0]
            board.pop()
            if(eval < minEval):
                minEval = eval
                best_move = move
            beta = min(beta, eval)
            if(beta <= alpha):
                break
        return minEval, best_move, nbNoeuds


#print(alphaBeta(board_2, 2, math.inf, -math.inf))

# COMPARAISON ALPHA BETA / MINIMAX

# Time comparison between alphbeta and minimax

#start = time.time()
#print(alphaBeta(board, 2, math.inf, -math.inf))
#end = time.time()
#elapsed = end - start
#print(f'Execution time: {elapsed:.2}ms')

#start = time.time()
#print(MiniMax(board_2, 2))
#end = time.time()
#elapsed = end - start
#print(f'Execution time: {elapsed:.2}ms')

# Match minimax against alphabeta


def match3(board):
    n_move = 0
    while board.is_game_over() != False:
        if board.turn == chess.WHITE:
            n_move = MiniMax(board, 2)
        else:
            n_move = alphaBeta(board, 2)
        board.push(board)
    return n_move


# print(match3(board))
