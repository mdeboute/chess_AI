from re import A
import time
import chess
from random import randint, choice
import math
import sys


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


# 2-1

# Cette fonction fait une recherche exaustive de toute les parties d'échecs à une certaine profondeur.
# # Retourne le nombre de partie possible.

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

#------------------------------------------------------------------------------#

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

# Cette fonction calcule la formule heuristique uniquement avec les poids des pieces.


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

#------------------------------------------------------------------------------#

# 2-3 MINIMAX

nbNoeuds = 0


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

#------------------------------------------------------------------------------#

# 2-4 GAMES

# joueur aléatoire contre minimax niveau 3:


def match1(board):
    board = chess.Board()
    while not board.is_game_over():
        if board.turn == chess.WHITE:
            print("--------------")
            print(board)
            board.push(randomMove(board))
        else:
            print("--------------")
            print(board)
            move = MiniMax(board, 3)[1]
            board.push(move)
    if board.is_game_over():
        print("Resultat : ", board.result())
        return


# print(match1(board))

# MiniMax niveau 1 contre MiniMax niveau 3:


def match2(board):
    board = chess.Board()
    while not board.is_game_over():
        if board.turn == chess.WHITE:
            print("--------------")
            print(board)
            move = MiniMax(board, 1)[1]
            board.push(move)
        else:
            print("--------------")
            print(board)
            move = MiniMax(board, 3)[1]
            board.push(move)
    print("---------------")
    print(board)
    if board.is_game_over():
        print("Resultat : ", board.result())
        return


# print(match2(board))

#------------------------------------------------------------------------------#

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


#print(alphaBeta(board, 2, -math.inf, math.inf))

#------------------------------------------------------------------------------#

# COMPARAISON ALPHA BETA / MINIMAX

# Time comparison between alphbeta and minimax

# start = time.time()
# print(alphaBeta(board, 2, math.inf, -math.inf))
# end = time.time()
# elapsed = end - start
# print(f'Execution time: {elapsed:.2}ms')

# start = time.time()
# print(MiniMax(board, 2))
# end = time.time()
# elapsed = end - start
# print(f'Execution time: {elapsed:.2}ms')

#------------------------------------------------------------------------------#

# Match minimax against alphabeta


def match3(board):
    board = chess.Board()
    while not board.is_game_over():
        if board.turn == chess.WHITE:
            print("--------------")
            print(board)
            move = MiniMax(board, 2)[1]
            board.push(move)
        else:
            print("--------------")
            print(board)
            move = alphaBeta(board, 2, -math.inf, math.inf)[1]
            board.push(move)
    if board.is_game_over():
        print("Resultat : ", board.result())
        return


# print(match3(board))

#------------------------------------------------------------------------------#

# 3-2:

# Le but de l'iterative deepening c'est d'augmenter la profondeur au maximum et on veut être sur qu'on ne
# dépasse pas le temps impartis (10s) à chaque résultat renvoyé.
# La fonction renvoie le meilleur score et move à une profondeur donnée tel que le temps pour toruver
# ces résultats est inférieur à 10 secondes.

start_time = time.time()
move_time = 10  # 10 seconds per move


def iterativeDeepeningAlphaBeta(board):
    MaxDepth = sys.maxsize
    start_time = time.time()
    bestMove = None
    for depth in range(1, MaxDepth):
        if time.time() - start_time > move_time:
            break
        val = -math.inf
        for move in board.generate_legal_moves():
            score = alphaBetaSearch(board, depth, -math.inf, math.inf)[0]
            if score > val:
                val = score
                bestMove = move
    return val, bestMove


def alphaBetaSearch(board, depth, alpha, beta):

    if depth <= 0 or time.time() - start_time > move_time:
        return formuleHeuristique(board), None
    if (depth == 0 or board.is_game_over()):
        return formuleHeuristique(board), None
    if board.turn == chess.WHITE:
        maxEval = -math.inf
        best_move = None
        for move in board.generate_legal_moves():
            board.push(move)
            eval = alphaBetaSearch(board, depth-1, alpha, beta)[0]
            board.pop()
            if(eval > maxEval):
                maxEval = eval
                best_move = move
            alpha = max(alpha, eval)
            if(beta <= alpha):
                break
        return maxEval, best_move
    else:
        minEval = math.inf
        best_move = None
        for move in board.generate_legal_moves():
            board.push(move)
            eval = alphaBetaSearch(board, depth-1, alpha, beta, )[0]
            board.pop()
            if(eval < minEval):
                minEval = eval
                best_move = move
            beta = min(beta, eval)
            if(beta <= alpha):
                break
        return minEval, best_move


# print(iterativeDeepeningAlphaBeta(board))


# def matchVsIA(board):
 #   board = chess.Board()
  #  while not board.is_game_over():
   #     if board.turn == chess.WHITE:
    #        print("--------------")
     #       print(board)
      #      ch = input()
       #     n = int(ch)
        #    move = chess.Move(from_square(n, n), chess.to_square(n, n))
        #   board.push(move)
        # else:
        #   print("--------------")
        #  print(board)
        # move = alphaBeta(board, 2, -math.inf, math.inf)[1]
        # board.push(move)
    # if board.is_game_over():
     #   print("Resultat : ", board.result())
      #  return


# print(matchVsIA(board))
