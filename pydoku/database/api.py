import re
import time


def solve(puzzle, solver, ):

    slvr = re.findall("<class '(.*)'>", str(solver.__class__))[0]

    s = solver(puzzle.board())

    starttime = time.time()
    s.solve()
    runtime = time.time() - starttime

    sol = Solution(puzzle=puzzle, correct=s.solution.solved(), runtime=runtime, solver=slvr,
                   integer=s.solution.toInt(), n=s.solution.n, wordSize=s.solution.wordSize)

    return sol
