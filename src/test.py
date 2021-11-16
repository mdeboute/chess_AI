import time
import chess
from random import randint, choice


board = chess.Board()

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

# print(board.piece_map().items())

def shannonWeight(list):
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
    return (shannonWeight(white)-abs(shannonWeight(black)))

def getBetterMove(board=board):
    costs = dict()
    moves = board.generate_legal_moves()
    for m in moves:
        board.push(m)
        costs[m] = evaluator(board)
        board.pop()
        print(m)
    return max(costs, key=costs.get), costs

