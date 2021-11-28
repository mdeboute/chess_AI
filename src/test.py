import time
import chess
from random import shuffle
import signal
from contextlib import contextmanager
class TimeoutException(Exception): pass


inf = 99999

board = chess.Board()
board_1 = chess.Board("r1bqkbnr/pppp1ppp/8/8/3nP3/8/PPP2PPP/RNBQKB1R w KQkq - 0 5")
board_2 = chess.Board("r1bqkb1r/ppppnpQp/8/8/4P3/8/PPP2PPP/RNB1KB1R b KQkq - 0 6")


@contextmanager
def time_limit(seconds):
    def signal_handler(signum, frame):
        raise TimeoutException("Timed out!")
    signal.signal(signal.SIGALRM, signal_handler)
    signal.alarm(seconds)
    try:
        yield
    finally:
        signal.alarm(0)

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

def test_exhaustiveSearch(board, time):
    depth = 1
    while True:
        try:
            with time_limit(time):
                nbNodes = exhaustiveSearch(board, depth)
                print(f"Depth={depth}, number of nodes={nbNodes}")
                depth += 1
        except:
            print("Timed out!")
            break

# test_exhaustiveSearch(board, 30)


# this function return if a pawn has a promotion move on the board
def pawn_has_promotion(board):
    for move in board.legal_moves:
        if move.promotion:
            return True
    return False

#print(pawn_has_promotion(chess.Board("rnbqkbnr/ppp3Pp/8/3p1p2/4p3/8/PPPPP1PP/RNBQKBNR w KQkq - 0 5")))
#print(pawn_has_promotion(chess.Board("rnbqkbnr/ppp3Pp/8/3p1p2/4p3/8/PPPPP1PP/RNBQKBNR b KQkq - 0 5")))


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


# this function compute the mobility (measured, say, as the number of legal moves)
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
    if board.is_checkmate() and board.turn == chess.BLACK:
        return inf
    if board.is_checkmate() and board.turn == chess.WHITE:
        return -inf
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
    # M1 = mobility(board)
    # M2 = mobility(switch_color(board))

    res = 9*(wQ-bQ) + 5*(wR-bR) + 3*(wB-bB + wN-bN) + (wP-bP) + 0.5*(DD2-DD1)

    # if a pawn can be promoted to a queen, it is a good move
    if board.turn == chess.WHITE and pawn_has_promotion(board):
        return res + 8
    if board.turn == chess.BLACK and pawn_has_promotion(board):
        return res - 8

    if board.turn == chess.WHITE and board.is_check():
        return res - 0.5
    if board.turn == chess.BLACK and board.is_check():
        return res + 0.5

    if board.turn == chess.WHITE and has_rook_in_open_file(board):
        return res + 0.1
    if board.turn == chess.BLACK and has_rook_in_open_file(board):
        return res - 0.1

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
# cf. the boards in the jupyter notebook


def cuttoff_test(board):
    if board.is_stalemate():
        return True
    elif board.is_fivefold_repetition():
        return True
    elif board.is_seventyfive_moves():
        return True
    elif board.is_insufficient_material():
        return True
    elif board.is_checkmate():
        return True
    else:
        return False

# Random Player match against Minimax level 3
def match_1():
    board = chess.Board()
    print(board)
    print("---------------")
    while not cuttoff_test(board):
        if board.turn == chess.WHITE:
            move = input("\nEnter your move: ")
            print("\n")
            board.push_san(move)
            print(board)
            print("---------------")
        else:
            move = minimax(board, 3)[0]
            board.push(move)
            print(board)
            print("---------------")
    print(board)
    print("---------------")
    print(board.outcome())

# match_1()


# Minimax lvl 1 VS minimax lvl 3
def match_2():
    board = chess.Board()
    print(board)
    print("---------------")
    while not cuttoff_test(board):
        if board.turn == chess.WHITE:
            move = minimax(board, 1)[0]
            board.push(move)
            print(board)
            print("---------------")
        else:
            move = minimax(board, 3)[0]
            board.push(move)
            print(board)
            print("---------------")
    print(board)
    print("---------------")
    print(board.outcome())

# match_2()


# Minimax algorithm with alpha-beta pruning which return the best move to play for the current board
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

# speed test benchmark for the minimax algorithm against the minimax_pruning algorithm at the same depth on the same board
def speed_test(board, depth):
    start = time.time()
    minimax(board, depth)[0]
    end = time.time()
    print("Minimax: " + str(end - start))
    start = time.time()
    minimax_pruning(board, depth, -inf, inf)[0]
    end = time.time()
    print("Minimax_pruning: " + str(end - start))

# print("On board 1 with depth 3:\n")
# speed_test(board_1, 3)
# print("\nOn board 2 with depth 2:\n")
# speed_test(board_2, 2)


# Minimax level 3 against minimax with alpha-beta pruning level 3
def match_3():
    board = chess.Board()
    print(board)
    print("---------------")
    while not cuttoff_test(board):
        if board.turn == chess.WHITE:
            move = minimax(board, 3)[0]
            board.push(move)
            print(board)
            print("---------------")
        else:
            move = minimax_pruning(board, 3, inf, -inf)[0]
            board.push(move)
            print(board)
            print("---------------")
    print(board)
    print("---------------")
    print(board.outcome())

# match_3()


# this function is an iterative deepening algorithm of alpha-beta pruning
# it take a time limit and a board as input
# return the best move compute in this time limit
def iterative_deepening(board, time):
    depth = 1
    while True:
        try:
            with time_limit(time):
                move, score = minimax_pruning(board, depth, -inf, inf)
                depth += 1
        except:
            break
    return move

#print(iterative_deepening(board, 5))


# this function create a match between a human and an iterative deepening
def match_4():
    board = chess.Board()
    print(board)
    print("---------------")
    while not cuttoff_test(board):
        if board.turn == chess.WHITE:
            move = input("\nEnter your move: ")
            print("\n")
            board.push_san(move)
            print(board)
            print("---------------")
        else:
            move = minimax_pruning(board, 3, inf, -inf)[0]
            board.push(move)
            print(board)
            print("---------------")
    print(board)
    print("---------------")
    print(board.outcome())

# match_4()