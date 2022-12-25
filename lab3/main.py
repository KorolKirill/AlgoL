import chess
import chess.engine
import time
import chess.svg
from IPython.display import SVG, display

engine = chess.engine.SimpleEngine.popen_uci(
    "C:\Users\korol\OneDrive\Desktop\piss\lab3\stockfish_15_win_x64_avx2")


def stockfish_eval(board_instance, isMax):
    info = engine.analyse(board_instance, chess.engine.Limit(depth=1))

    if not isMax:
        res = chess.engine.PovScore(info['score'], chess.BLACK).pov(chess.BLACK).relative.score()
    else:
        res = chess.engine.PovScore(info['score'], chess.WHITE).pov(chess.WHITE).relative.score()
    # print(result)
    if res is None:
        res = 0
    return res


def best_move_using_negaMax(board_instance, depth):
    def negaMax(table, depth, is_max):
        if depth == 0:
            return stockfish_eval(table, is_max)

        maxValueIn = -1_000_000
        for legal_move in table.legal_moves:
            move = chess.Move.from_uci(str(legal_move))
            boardCopy = table.copy()
            boardCopy.push(move)
            value = -negaMax(boardCopy, depth - 1, 1 - is_max)
            if value > maxValueIn:
                maxValueIn = value
        return maxValueIn

    maxValue = -1_000_000
    best = None
    for legal_move in board_instance.legal_moves:
        move = chess.Move.from_uci(str(legal_move))
        boardCopy = board_instance.copy()
        boardCopy.push(move)
        value = -negaMax(boardCopy, depth, 1 - boardCopy.turn)
        if value > maxValue:
            maxValue = value
            best = move
    return best


def best_move_using_negaScout(board_instance, depth, alpha=-999999, beta=999999):
    def negaScout(table, depthIn, alphaIn, betaIn):
        if depthIn == 0:
            return stockfish_eval(table, table.turn)
        scoreIn = -1_000_000
        n = betaIn
        for legal_move in table.legal_moves:
            move = chess.Move.from_uci(str(legal_move))
            boardCopy = table.copy()
            boardCopy.push(move)
            cur = -negaScout(boardCopy, depthIn - 1, -n, -alphaIn)
            if cur > scoreIn:
                if n == beta or depthIn <= 2:
                    scoreIn = cur
                else:
                    scoreIn = -negaScout(boardCopy, depthIn - 1, -betaIn, -cur)
            if scoreIn > alphaIn:
                alphaIn = scoreIn
            if alphaIn >= betaIn:
                return alphaIn
            n = alphaIn + 1
        return scoreIn

    score = -1_000_000
    bestMove = None
    for legal_move in board_instance.legal_moves:
        move = chess.Move.from_uci(str(legal_move))
        boardCopy = board_instance.copy()
        boardCopy.push(move)
        value = -negaScout(boardCopy, depth, alpha, beta)
        if value > score:
            score = value
            bestMove = move

    return bestMove


def best_move_using_pvs(board_instance, depth, alpha=-999999, beta=999999):
    def pvs(table, depthiIn, alphaiIn, betaiIn):
        if depthiIn == 0:
            return stockfish_eval(table, table.turn)
        bSearchPvIn = True
        for legal_move in table.legal_moves:
            move = chess.Move.from_uci(str(legal_move))
            boardCopy = table.copy()
            boardCopy.push(move)
            if bSearchPvIn:
                cur = -pvs(boardCopy, depthiIn - 1, -betaiIn, -alphaiIn)
            else:
                cur = -pvs(boardCopy, depthiIn - 1, -alphaiIn - 1, -alphaiIn)
                if alphaiIn < cur < betaiIn:
                    cur = -pvs(boardCopy, depthiIn - 1, -betaiIn, -alphaiIn)
            if cur >= betaiIn:
                return betaiIn
            if cur > alphaiIn:
                alphaiIn = cur
                bSearchPvIn = False

        return alphaiIn

    score = -1_000_000
    best = None
    for legal_move in board_instance.legal_moves:
        move = chess.Move.from_uci(str(legal_move))
        boardCopy = board_instance.copy()
        boardCopy.push(move)
        value = -pvs(boardCopy, depth, alpha, beta)
        if value > score:
            score = value
            best = move

    return best


def game_between_two_computers_pvs(depth=1):
    table = chess.Board()
    n = 0

    while table.is_checkmate() != True and table.is_fivefold_repetition() != True and table.is_seventyfive_moves() != True:
        str = time.time()
        if n % 2 == 0:
            print("WHITE Turn")
            move = best_move_using_pvs(table, depth)
        else:

            print("BLACK Turn")
            move = best_move_using_pvs(table, depth)
        end = time.time()

        if move == None:
            print("GG, checkmate")
            break

        print("Move in UCI format:", move)
        print("Time taken by Move:", end - str)
        print("Moves taken:", n)
        print("FiveFold", table.is_fivefold_repetition())

        table.push(move)
        # display(SVG(chess.svg.board(board, size=400)))
        print(table)
        print("\n")
        n = n + 1
    if table.is_fivefold_repetition():
        print("GG, fivefold")


def game_between_two_computers_negaScout(depth=1):
    table = chess.Board()
    n = 0

    while table.is_checkmate() != True and table.is_fivefold_repetition() != True and table.is_seventyfive_moves() != True:
        start = time.time()
        if n % 2 == 0:
            print("WHITE Turn")
            move = best_move_using_negaScout(table, depth)
        else:

            print("BLACK Turn")
            move = best_move_using_negaScout(table, depth)
        end = time.time()

        if move == None:
            print("GG, checkmate")
            break

        print("Move in UCI format:", move)
        print("Time taken by Move:", end - start)
        print("Moves taken:", n)
        print("FiveFold", table.is_fivefold_repetition())

        table.push(move)
        # display(SVG(chess.svg.board(board, size=400)))
        print(table)
        print("\n")
        n = n + 1
    if table.is_fivefold_repetition():
        print("GG, fivefold")


def game_between_two_computers_negaMax(depth=1):
    table = chess.Board()
    n = 0

    while table.is_checkmate() != True and table.is_fivefold_repetition() != True and table.is_seventyfive_moves() != True:
        str = time.time()
        if n % 2 == 0:
            print("WHITE Turn")
            move = best_move_using_negaMax(table, depth)
        else:

            print("BLACK Turn")
            move = best_move_using_negaMax(table, depth)
        end = time.time()

        if move == None:
            print("GG, checkmate")
            break

        print("Move in UCI format:", move)
        print("Time taken by Move:", end - str)
        print("Moves taken:", n)
        print("FiveFold", table.is_fivefold_repetition())

        table.push(move)
        # display(SVG(chess.svg.board(board, size=400)))
        print(table)
        print("\n")
        n = n + 1
    if table.is_fivefold_repetition():
        print("GG, fivefold")


if __name__ == '__main__':
    # game_between_two_computers_negaMax()
    # game_between_two_computers_negaScout()
    game_between_two_computers_pvs()
    engine.quit()
