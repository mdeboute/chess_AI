import time
import chess
from random import randint, choice

board = chess.Board()

board_1 = chess.Board("r1bqkbnr/pppp1ppp/8/8/3nP3/8/PPP2PPP/RNBQKB1R w KQkq - 0 5")
board_2 = chess.Board("r1bqkb1r/ppppnpQp/8/8/4P3/8/PPP2PPP/RNB1KB1R b KQkq - 0 6")

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
    if(board.turn == chess.WHITE):
        return shannonWeight(white) - abs(shannonWeight(black))
    if(board.turn == chess.BLACK):
        return abs(shannonWeight(black)) - shannonWeight(white)

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
    return max(costs, key=costs.get)

#print(getBetterMove(board_1))
#print(getBetterMove(board_2))
# it's working!!