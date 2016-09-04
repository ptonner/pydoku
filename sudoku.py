from numpy import *
import numpy as np
import cvxopt
from cvxopt import solvers

def boardValueIndex(n,row,col,val):
    return (row)*n**2 + (col)*n + val-1
    
def boardIndextoRowColVal(n,ind):
    return ind/n**2, (ind%n**2)/n, ind%n

class Sudoku():

	def __init__(self,n,clues):
		
		self.n = n # row/height
		self.b = b = int(n**(.5)) # box size
		self.p = self.n**3 # size of objective
		
		# self.clues = array([int(c) if not c=="." else 0 for c in clues])
		# self.clues = self.clues.reshape((self.n,self.n))
		self.clues = clues
		self.c = sum(self.clues!=0)
		
		self.board = self.clues.copy()
		self.constraints = None
		self.x = None
		self.sol = None
		
	def constraintMatrix(self):
		"""Build a constraint matrix for this sudokue problem.

		A sudoku board is converted to a convex optimization problem
		by treating each cell as a size n binary vector, where a value
		of 1 at position k indicates that cell's value is k. There are
		n^2 cells on the board so a vector of size n*n^2=n^3 is needed
		to encode all cells.

		The constraint matrix is constructed with the following order:
		[[box], [row], [col], [cell],[clue]], for the constraints
		where each box, row and column have exactly one each of number
		1,...,n; each cell can only have a single value 0 < k < n+1;
		and any clues provided for the puzzle.
		"""
		
		if self.constraints:
			return self.constraints
			
		# self.constraints = zeros((0,self.n**3))
		self.constraints = zeros((4*self.n**2+self.c,self.n**3))
		
		n = self.n
		b = self.b
		
		### box constraints
		box_select = concatenate(
					(tile(concatenate([identity(n)]*self.b+[zeros((self.n,self.n))]*(self.n-self.b),1),(self.b-1)),
					concatenate([identity(self.n)]*self.b,1))
					,1)
                   
		m = zeros((n**2,n**3))
		for i in range(n):
		    m[i*n:i*n+n,
		      # offset last box row (floor) + offset last box (mod)
		      (i/b)*b*n**2+(i%b)*b*n:(i/b)*b*n**2+(i%b)*b*n+n*(n*(b-1)+b)] = box_select
		      
		# self.constraints = concatenate((self.constraints,m))
		self.constraints[:n**2,:] = m
		
		### row constraints
		row_select = concatenate([identity(n)]*n,1)
		m=zeros((n**2,n**3))
		for i in range(n):
		    m[i*n:(i+1)*n,i*n**2:(i+1)*n**2] = row_select
		    
		# self.constraints = concatenate((self.constraints,m))
		self.constraints[n**2:2*n**2,:] = m
		
		### column constraints
		m = concatenate([identity(n**2)]*n,1)
		# self.constraints = concatenate((self.constraints,m))
		self.constraints[2*n**2:3*n**2,:] = m
		
		### all cells
		m = zeros((n**2,n**3))

		for i in range(n**2):
		    m[i,i*n:(i+1)*n] = ones((n))    
		    
		# self.constraints = concatenate((self.constraints,m))
		self.constraints[3*n**2:4*n**2,:] = m

		### clues
		m = zeros((self.c,self.p))

		for i,cell in enumerate(column_stack(where(self.clues!=0))):
		    row,col = cell

		    m[i,boardValueIndex(n,row,col,self.clues[row,col])] = 1
		    
		# self.constraints = concatenate((self.constraints,m))
		self.constraints[4*n**2:,:] = m
		
		self.rhs = ones(self.constraints.shape[0])
		
		return self.constraints

	def solve_moreComplicated(self,verbose=False):
		if self.constraints is None:
			self.constraintMatrix()
			
		n = self.n

		"""
			| C  -C|
		G = |-C   C|
			|  -I  |
		"""
		G = cvxopt.matrix(row_stack((column_stack((self.constraints,-self.constraints)),
			       column_stack((-self.constraints,self.constraints)),
			       -identity(2*self.p))))
		h = cvxopt.matrix(concatenate((self.rhs,-self.rhs,zeros((2*n**3)))))

		cvxopt.solvers.options['show_progress'] = verbose

		self.u = solvers.lp(cvxopt.matrix(ones((2*n**3))),G,h)
		self.x = array(self.u['x'][:n**3])
		
		
	def solve(self,verbose=False):
		if self.constraints is None:
			self.constraintMatrix()
			
		n = self.n

		"""
			| C|
		G = |-C|
			|-I|
		"""

		G1 = self.constraints
		G2 = -self.constraints
		G3 = -identity(self.p)

		G = cvxopt.matrix(row_stack((G1,G2,G3)))
		h = cvxopt.matrix(concatenate((self.rhs,-self.rhs,np.zeros(G3.shape[0]))))
		
		c = cvxopt.matrix(ones(G.size[1]))

		cvxopt.solvers.options['show_progress'] = verbose

		self.u = solvers.lp(c,G,h,solver=None)
		self.x = array(self.u['x'][:n**3])
		self.xround = self.x.round()

	def solution(self,verbose=False):
	
		if self.x is None:
			self.solve()

		n = self.n
		self.sol = zeros((n,n))
		self.solved = True
		
		for ind in where(self.x!=0)[0]:
		    row,col,val = boardIndextoRowColVal(n,ind)
		    if self.x[ind] < 1e-4:
				continue
		
		    if not self.sol[row,col]==0:
		    	self.solved = False

		    	if verbose:
					print "Error: %d,%d already set!" % (row, col)	
					print ind,(ind/n)*n,((ind/n)+1)*n
					print self.x[(ind/n)*n:((ind/n)+1)*n]
		    
		    self.sol[row,col] = val+1
			    		
		return self.sol
		
	def check(self,verbose=False):
		
		if self.constraints is None:
			print "Build constraints..."
			self.constraintMatrix()
		if self.x is None:
			print "Solve board..."
			self.solve()
		if self.sol is None:
			print "Find solution..."
			self.solution(verbose=verbose)
	
		check = self.solved
		
		# check objective function
		check = check and np.all(np.round(dot(self.constraints,self.x)).astype(int)==1)
	
		self.solved = check
		return check
		