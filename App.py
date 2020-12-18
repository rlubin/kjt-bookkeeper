from tkinter import *


class App():
    def __init__(self):
        """window setup"""
        self.root = Tk()
        self.root.title('KJT Bookkeeper')
        self.root.geometry('500x500')
        self.root.minsize(300, 225)

        self.root.mainloop()


app = App()
