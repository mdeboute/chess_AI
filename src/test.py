from re import M
import time
import chess
from random import choice, shuffle


inf = 9999

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

# this function count the number of promoted pawns on the board
def pawn_has_promotion(board, player):
    if board.turn == player:
        for move in board.legal_moves:
            if move.promotion:
                return True
    return False

# print(pawn_has_promotion(chess.Board("rnbqkbnr/ppp3Pp/8/3p1p2/4p3/8/PPPPP1PP/RNBQKBNR w KQkq - 0 5"), chess.WHITE))
# print(pawn_has_promotion(chess.Board("rnbqkbnr/ppp3Pp/8/3p1p2/4p3/8/PPPPP1PP/RNBQKBNR b KQkq - 0 5"), chess.BLACK))

def switch_color(board):
    fen = board.fen().split()
    if fen[1] == 'w':
        fen[1] = 'b'
    else:
        fen[1] = 'w'
    return chess.Board(' '.join(fen))

# print(board.fen())
# print(switch_color(board).fen())

# this function determines the number of doubled pawns on the board
def doubled_pawns(board):
    count = 0
    for i in range(8):
        for j in range(8):
            if board.piece_at(chess.square(i, j)) != None and board.piece_at(chess.square(i, j)).color == board.turn and board.piece_at(chess.square(i, j)).piece_type == chess.PAWN and board.piece_at(chess.square(i, j+1)) != None and board.piece_at(chess.square(i, j+1)).color == board.turn and board.piece_at(chess.square(i, j+1)).piece_type == chess.PAWN:
                count += 1
    return count

# b = chess.Board("rnbqkbnr/p1ppppp1/4P3/8/8/1P1P1P1P/1PP4P/RNBQKBNR w KQkq - 0 7")
# print(doubled_pawns(b))
# b2 = switch_color(b)
# print(doubled_pawns(b2))

# this function determines if there is a rook in an open file
def has_rook_in_open_file(board):
    for i in range(8):
        for j in range(8):
            if board.piece_at(chess.square(i, j)) != None and board.piece_at(chess.square(i, j)).color == board.turn and board.piece_at(chess.square(i, j)).piece_type == chess.ROOK and board.piece_at(chess.square(i, j+1)) == None:
                return True
            return False

# print(has_rook_in_open_file(chess.Board("rnbqkbnr/pppppppp/8/8/8/8/1PPPPPPP/RNBQKBNR w KQkq - 0 1")))
# print(has_rook_in_open_file(chess.Board("rnbqkbnr/ppppppp1/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")))

# this function compute the white mobility (measured, say, as the number of legal moves)
def mobility(board):
    count = 0
    for move in board.legal_moves:
        board.push(move)
        count += 1
        board.pop()
    return count

# b = chess.Board("8/6k1/P7/8/8/8/5K2/8 b - - 0 1")
# print(mobility(b), mobility(switch_color(b)))

def shannonHeuristic(board):
    if board.is_checkmate():
        return inf
    if board.is_game_over():
        return -inf
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
    DD1 = doubled_pawns(board)
    DD2 = doubled_pawns(switch_color(board))
    M1 = mobility(board)
    M2 = mobility(switch_color(board))

    res = 9*(wQ-bQ) + 5*(wR-bR) + 3*(wB-bB + wN-bN) + (wP-bP) + 0.5*(DD2-DD1)

    # if a pawn can be promoted to a queen, it is a good move
    if pawn_has_promotion(board, chess.WHITE):
        return res + 8
    if pawn_has_promotion(board, chess.BLACK):
        return res - 8

    if board.turn == chess.WHITE and board.is_check():
        return res - 0.5
    if board.turn == chess.BLACK and board.is_check():
        return res + 0.5

    if board.turn == chess.WHITE and has_rook_in_open_file(board):
        return res + 1
    if board.turn == chess.BLACK and has_rook_in_open_file(board):
        return res - 1

    return res

# print(shannonHeuristic(board_1))
# print(shannonHeuristic(board_2))

# minimax function which return the best move to play for the current board
def minimax(board, depth):
    if depth == 0 or board.is_game_over():
        return None, shannonHeuristic(board)
    if board.turn == chess.WHITE:
        best_score = -inf
        best_move = None
        moves = list(board.legal_moves)
        shuffle(moves)
        for move in moves:
            board.push(move)
            score = minimax(board, depth - 1)[1]
            board.pop()
            if score > best_score:
                best_score = score
                best_move = move
        return best_move, best_score
    else:
        best_score = inf
        best_move = None
        moves = list(board.legal_moves)
        shuffle(moves)
        for move in moves:
            board.push(move)
            score = minimax(board, depth - 1)[1]
            board.pop()
            if score < best_score:
                best_score = score
                best_move = move
        return best_move, best_score

# print(minimax(board_1, 3))
# print(minimax(board_2, 3))

# Random Player match against Minimax root level 3
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
            move = minimax(board, 3)[0]
            board.push(move)
    print(board)

# match_1()

# minimax algorithm with alpha-beta pruning which return the best move to play for the current board
def minimax_pruning(board, depth, alpha, beta):
    if depth == 0 or board.is_game_over():
        return None, shannonHeuristic(board)
    if board.turn == chess.WHITE:
        best_score = -inf
        best_move = None
        moves = list(board.legal_moves)
        shuffle(moves)
        for move in moves:
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
        best_score = inf
        best_move = None
        moves = list(board.legal_moves)
        shuffle(moves)
        for move in moves:
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

# Random Player match against Minimax with alpha-beta pruning level 3
def match_2():
    board = chess.Board()
    while not board.is_game_over():
        if board.turn == chess.WHITE:
            print("---------------")
            print(board)
            move = input("\nEnter your move: ")
            print("\n")
            board.push_san(move)
        else:
            move = minimax_pruning(board, 3, -inf, inf)[0]
            board.push(move)
            print(move)

match_2()

# Minimax with alpha-beta pruning level 1 against Minimax with alpha-beta pruning level 3
def match_3():
    board = chess.Board()
    while not board.is_game_over():
        if board.turn == chess.WHITE:
            print("---------------")
            move, score = minimax_pruning(board, 3, -inf, inf)
            board.push(move)
            print(move, score)
        else:
            move, score = minimax_pruning(board, 3, -inf, inf)
            board.push(move)
            print(move, score)

#match_3()


# TODO:
# iterative deepening apllied to alpha-beta pruning
# shuffle the legal moves that have the same cost to avoid the same move being chosen
