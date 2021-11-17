import time
import chess
from random import randint, choice, shuffle


board = chess.Board()
board_1 = chess.Board("r1bqkbnr/pppp1ppp/8/8/3nP3/8/PPP2PPP/RNBQKB1R w KQkq - 0 5")
board_2 = chess.Board("r1bqkb1r/ppppnpQp/8/8/4P3/8/PPP2PPP/RNB1KB1R b KQkq - 0 6")
checkmate = chess.Board("rnbqkbnr/ppppp2p/8/5PpQ/8/8/PPPP1PPP/RNB1KBNR b KQkq - 1 3")

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


def shannonHeuristic(board):
    if board.is_checkmate():
        return float('inf')
    if board.is_game_over():
        return -float('inf')
    if board.is_stalemate():
        return 0
    wP = len(board.pieces(chess.PAWN, chess.WHITE))
    bP = len(board.pieces(chess.PAWN, chess.BLACK))
    wN = len(board.pieces(chess.KNIGHT, chess.WHITE))
    bN = len(board.pieces(chess.KNIGHT, chess.BLACK))
    wB = len(board.pieces(chess.BISHOP, chess.WHITE))
    bB = len(board.pieces(chess.BISHOP, chess.BLACK))
    wR = len(board.pieces(chess.ROOK, chess.WHITE))
    bR = len(board.pieces(chess.ROOK, chess.BLACK))
    wQ = len(board.pieces(chess.QUEEN, chess.WHITE))
    bQ = len(board.pieces(chess.QUEEN, chess.BLACK))
    res = 9*(wQ-bQ) + 5*(wR-bR) + 3*(wB-bB + wN-bN) + (wP-bP)
    return res

#print(shannonHeuristic(board))
#print(shannonHeuristic(checkmate))

# minimax function which return the best move to play for the current board
def minimax(board, depth):
    if depth == 0 or board.is_game_over():
        return None, shannonHeuristic(board)
    if board.turn == chess.WHITE:
        best_score = float('-inf')
        best_move = None
        for move in board.legal_moves:
            board.push(move)
            score = minimax(board, depth - 1)[1]
            board.pop()
            if score > best_score:
                best_score = score
                best_move = move
        return best_move, best_score
    else:
        best_score = float('inf')
        best_move = None
        for move in board.legal_moves:
            board.push(move)
            score = minimax(board, depth - 1)[1]
            board.pop()
            if score < best_score:
                best_score = score
                best_move = move
        return best_move, best_score

#print(minimax(board_1, 3))
#print(minimax(board_2, 3))

def minimaxRoot(board, depth):
    if depth == 0 or board.is_game_over():
        return None, shannonHeuristic(board)
    best_score = float('-inf')
    best_move = None
    for move in board.legal_moves:
        board.push(move)
        score = minimax(board, depth - 1)[1]
        board.pop()
        if score > best_score:
            best_score = score
            best_move = move
    return best_move, best_score

# Random Player match against Minimax level 3
def match_1():
    board = chess.Board()
    while not board.is_game_over():
        if board.turn == chess.WHITE:
            print("---------------")
            print(board)
            move = input("\nEnter your move: ")
            print("\n")
            board.push_san(move)
        else:
            print(board)
            move = minimaxRoot(board, 3)[0]
            board.push(move)
    print(board)

# match_1()

# minimax algorithm with alpha-beta pruning which return the best move to play for the current board
def minimax_pruning(board, depth, alpha, beta):
    if depth == 0 or board.is_game_over():
        return None, shannonHeuristic(board)
    if board.turn == chess.WHITE:
        best_score = float('-inf')
        best_move = None
        for move in board.legal_moves:
            board.push(move)
            score = minimax_pruning(board, depth - 1, alpha, beta)[1]
            board.pop()
            if score > best_score:
                best_score = score
                best_move = move
            if best_score > beta:
                return best_move, best_score
            alpha = max(alpha, best_score)
        return best_move, best_score
    else:
        best_score = float('inf')
        best_move = None
        for move in board.legal_moves:
            board.push(move)
            score = minimax_pruning(board, depth - 1, alpha, beta)[1]
            board.pop()
            if score < best_score:
                best_score = score
                best_move = move
            if best_score < alpha:
                return best_move, best_score
            beta = min(beta, best_score)
        return best_move, best_score


# iterative deepening apllied to alpha-beta pruning