from . import Board
import Tkinter as tk
import numpy as np


def board(n, clues=None):
    root = tk.Tk()
    root.grid_rowconfigure(0, weight=1)
    root.grid_columnconfigure(0, weight=1)

    frames = []

    for r in range(n):
        for c in range(n):
            frame = tk.Frame(root)
            frame.grid(row=r, column=c, sticky='nsew', padx=10, pady=10)

            for rr in range(n):
                for cc in range(n):
                    if not clues is None and clues[rr + r * n, cc + c * n] != 0:
                        t = tk.Label(
                            frame, font=("Helvetica", 32), text=str(clues[rr + r * n, cc + c * n]), width=1)
                        t.grid(row=rr, column=cc)
                    else:
                        t = tk.Entry(frame, font=("Helvetica", 32), width=1)
                        t.grid(row=rr, column=cc)

            frames.append(frame)

    buttonFrame = tk.Frame(root)
    buttonFrame.grid(row=n + 1, column=n / 2, sticky='nswe', pady=5)

    board = np.zeros((n**2, n**2))

    def callback():
        for r in range(n):
            for c in range(n):
                f = frames[r * n + c]
                texts = f.grid_slaves()
                texts = list(reversed(texts))
                for rr in range(n):
                    for cc in range(n):
                        t = texts[rr * n + cc]
                        try:
                            v = int(t.get()[-1])
                            d = t.grid_info()
                            rrr, ccc = d['row'], d['column']
                            board[r * n + rrr, c * n + ccc] = v
                        except:
                            continue

        root.quit()
        root.destroy()

    solve = tk.Button(buttonFrame, text="solve", command=callback)
    solve.grid(row=0, column=0)

    root.mainloop()
    return Board(board)
