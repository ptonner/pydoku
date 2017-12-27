import numpy as np
import Tkinter as tk

class Board():

	@classmethod
	def from_vector(v):

		n = int(np.cbrt(v.shape[0]))
		return Board(n)

	@classmethod
	def from_string(s,empty='.'):
		a = np.array([int(c) if not c == empty else 0 for c in s])
		n = int(np.sqrt(a.shape[0]))
		a = a.reshape((n,n))
		Board(a)

	@staticmethod
	def from_tk(n):
		root = tk.Tk()
		root.grid_rowconfigure(0, weight=1)
		root.grid_columnconfigure(0, weight=1)

		frames = []

		for r in range(n):
			for c in range(n):
				frame = tk.Frame(root)
				frame.grid(row=r,column=c,sticky='nsew',padx=10,pady=10)

				for rr in range(n):
					for cc in range(n):
						t = tk.Entry(frame,font=("Helvetica",32),width=1)
						# t = tk.Text(frame,width=1,height=1,padx=1,pady=1,font=("Helvetica",32),fg='red')
						# t = tk.Text(frame,width=1,height=1,padx=1,pady=1,font=("Helvetica",32),fg='red')
						t.grid(row=rr,column=cc)

				frames.append(frame)

		buttonFrame = tk.Frame(root)
		buttonFrame.grid(row=n+1,column=n/2,sticky='nswe',pady=5)


		board = np.zeros((n**2,n**2))
		def callback():
			for r in range(n):
				for c in range(n):
					f = frames[r*n+c]
					texts = f.grid_slaves()
					texts = list(reversed(texts))
					for rr in range(n):
						for cc in range(n):
							t = texts[rr*n+cc]
							try:
								v = int(t.get()[-1])
								d = t.grid_info()
								rrr,ccc = d['row'],d['column']
								board[r*n+rrr,c*n+ccc]=v
							except:
								continue


			root.quit()
			root.destroy()

		solve = tk.Button(buttonFrame, text="solve", command=callback)
		solve.grid(row=0,column=0)

		root.mainloop()
		return Board(board)

		# return frames
		
	def __init__(self,b):
		self.board = b
		self.n = self.board.shape[0]
		self.r = int(np.sqrt(self.n)) # root
		assert self.board.shape[0] == self.board.shape[1]

	def __eq__(self,other):
		if self.n == other.n:
			return all(self.board == other.board)
		return False

	# def __init__(self,n,init):
	# 	self.n = n
	# 	self.b = int(n**.5)

	# 	self.board = np.zeros((n,n))
	# 	self.board += init

	def _validate_group(self,l):
		"""
		check an array of numbers to contain exactly one of each of 1, 2, ..., n
		"""
		ret = True

		for i in range(self.n):
			ret = ret and sum(l==i+1) == 1

		ret = ret and l.shape[0] == self.n
		return ret

	def solved(self,):
		solved = True

		solved = solved and np.all(self.board>0)
		solved = solved and np.all(self.board<self.n+1)

		# check rows and columns
		for i in range(self.n):
			solved = solved and self._validate_group(self.board[:,i])
			solved = solved and self._validate_group(self.board[i,:])

		# check blocks
		for i in range(self.b):
			for j in range(self.b):
				g = self.board[i*self.b:(i+1)*self.b,j*self.b:(j+1)*self.b].ravel()
				solved = solved and self._validate_group(g)

		return solved