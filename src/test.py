import time
import chess
from random import randint, choice
import math


board = chess.Board(
    "Q7/p3k3/7p/8/8/8/PPPP1PPP/RNBQKBNR b KQ - 0 15")
board_2 = chess.Board(
    "r1bqkb1r/ppppnpQp/8/8/4P3/8/PPP2PPP/RNB1KB1R b KQkq - 0 6")
# r1bqkbnr/pppp1ppp/8/8/3nP3/8/PPP2PPP/RNBQKB1R w KQkq - 0 5

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


# HEURISTIQUE SHANNON VERSION 1

def getPiece(board=board):
    white_piece = []
    black_piece = []
    for piece in board.piece_map().items():
        symbol = str(piece[1])
        if(symbol.islower()):
            black_piece.append(symbol)
        if(symbol.isupper()):
            white_piece.append(symbol)
    return black_piece, white_piece


print(board.piece_map().items())


def shannonWeight(list):
    if(board.is_game_over()):
        return 0
    if board.is_checkmate():
        if (board.turn == chess.WHITE):
            return -math.inf
        if(board.turn == chess.BLACK):
            return math.inf
    score = 0
    for piece in list:
        if(piece == 'k'):
            score -= 200
        elif(piece == 'K'):
            score += 200
        elif(piece == 'q'):
            score -= 9
        elif (piece == 'Q'):
            score += 9
        elif(piece == 'r'):
            score -= 5
        elif(piece == 'R'):
            score += 5
        elif(piece == 'b'):
            score -= 3
        elif(piece == 'B'):
            score += 3
        elif(piece == 'n'):
            score -= 3
        elif(piece == 'N'):
            score += 3
        elif(piece == 'p'):
            score -= 1
        else:
            score += 1
    return score


def evaluator(board=board):
    black, white = getPiece(board)
    if(board.turn == chess.WHITE):
        return shannonWeight(white) - abs(shannonWeight(black))
    if(board.turn == chess.BLACK):
        return abs(shannonWeight(black)) - shannonWeight(white)


# print(evaluator(board))

def getBetterMove(board=board):
    costs = dict()
    moves = board.generate_legal_moves()
    for m in moves:
        board.push(m)
        if(board.turn == chess.WHITE):
            costs[m] = abs(evaluator(board))
        if(board.turn == chess.BLACK):
            costs[m] = -abs(evaluator(board))
        board.pop()
    return max(costs, key=costs.get), costs


# print(getBetterMove(board))
# print(getBetterMove(board_2))
# it's working!!


# HEURISITQUE DE SHANNON VERSION 2

def evaluate(board):
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
print(evaluate(board))

MAXDEPTH = 4


def MiniMax(board, depth, maximizingPlayer):

    if (depth == 0 or board.is_game_over()):
        return evaluate(board)

    if(maximizingPlayer):
        maxEval = -math.inf
        for move in board.generate_legal_moves():
            board.push(move)
            eval = MiniMax(board, depth-1, False)
            # board.pop()
            if(eval > maxEval):
                maxEval = eval
            board.pop()
            return maxEval
    else:
        minEval = math.inf
        for move in board.generate_legal_moves():
            board.push(move)
            eval = MiniMax(board, depth-1, True)
            # board.pop()
            if(eval < minEval):
                minEval = eval
            board.pop()
        return minEval


# print(MiniMax(board, 2, True))


def alphaBeta(board, depth, alpha, beta, maximizingPlayer):
    if (depth == 0 or board.is_game_over()):
        return evaluator(board)
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


# def match1(board):
