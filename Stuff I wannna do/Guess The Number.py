set_guess = lambda x: print(f"Guess")
from tkinter import *
tk = Tk()
btn = Button(tk, text='1-50', command=lambda: (set_guess((1, 50))))
btn.pack()