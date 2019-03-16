from tkinter import *


class QuestionElement:

    def __init__(self, root, label):

        self.sourceWord = Label(root, text=label)
        self.entry = Entry(root, width=30)

        self.sourceWord.grid(row=0, column=0)
        self.entry.grid(row=0, column=1)

    def getEntry(self):
        return self.entry.get()

    def destroy(self):
        self.sourceWord.destroy()
        self.entry.destroy()
