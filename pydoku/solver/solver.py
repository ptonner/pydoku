from numpy import *
import numpy as np
import cvxopt
from cvxopt import solvers
from ..board import Board


class Solver(object):

    # are solutions deterministic? e.g. same answer every time
    deterministic = True

    # is the solution broken into iterative updates?
    iterative = True

    def __init__(self, board, *args, **kwargs):

        assert issubclass(type(board), Board)
        self.clues = board

        self.solution = self.clues.copy()
        self.solved = False

    def solve(self):
        s = self._solve_sanitize()

        # is this a solution to my board?
        assert self.clues < s

        self.solution = s
        self.solved = True

    def _solve_sanitize(self):
        s = self._solve()

        if type(s) is np.ndarray:
            return Board(s)

        return s

    def _solve(self):
        raise NotImplemented()
