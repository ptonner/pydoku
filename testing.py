import unittest
import sudoku as sd
import problems

class ParametrizedTestCase(unittest.TestCase):

    def __init__(self, methodName='runTest', param=None):
        super(ParametrizedTestCase, self).__init__(methodName)
        self.param = param

    @staticmethod
    def parametrize(testcase_klass, param=None):
        """ Create a suite containing all tests taken from the given
            subclass, passing them the parameter 'param'.
        """
        testloader = unittest.TestLoader()
        testnames = testloader.getTestCaseNames(testcase_klass)
        suite = unittest.TestSuite()
        for name in testnames:
            suite.addTest(testcase_klass(name, param=param))
        return suite

class SudFileTest(ParametrizedTestCase):

    def setUp(self):
        self.puzzle = problems.puzzles(self.param)()

    def tearDown(self):
        self.puzzle = None

    def test_size(self):
        print 'param =', self.param
        self.assertEqual(self.puzzle.shape,(9,9))


class SudokuTest(ParametrizedTestCase):

    def setUp(self):
        self.puzzle = problems.puzzles(self.param)()
        self.sudoku = sd.Sudoku(9,self.puzzle)

    def tearDown(self):
        self.puzzle = None

    def test_solved(self):
        # print 'param =', self.param
        self.assertTrue(self.sudoku.check())

    def test_solveComplicated(self):
        self.sudoku.solve_moreComplicated()
        self.assertTrue(self.sudoku.check())


if __name__=="__main__":

    suite = unittest.TestSuite()

    for i in range(len(problems._puzzles)):
        suite.addTest(ParametrizedTestCase.parametrize(SudFileTest,param=i))
        suite.addTest(ParametrizedTestCase.parametrize(SudokuTest,param=i))
    unittest.TextTestRunner(verbosity=2).run(suite)
