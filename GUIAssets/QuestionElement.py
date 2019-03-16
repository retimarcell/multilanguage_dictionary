from tkinter import *


class QuestionElement:

    def __init__(self, root, lang, label):

        self.langLabel = Label(root, text=lang)
        self.sourceWord = Label(root, text=label)
        self.entry = Entry(root, width=30)

        self.langLabel.grid(row=0, column=1)
        self.sourceWord.grid(row=1, column=0)
        self.entry.grid(row=1, column=1)

    def getEntry(self):
        return self.entry.get()

    def destroy(self):
        self.sourceWord.destroy()
        self.entry.destroy()
