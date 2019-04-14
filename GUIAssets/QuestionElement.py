from tkinter import *


class QuestionElement:

    def __init__(self, root, lang, label, sourceLang=""):

        if sourceLang == "":
            text = label
        else:
            text = label + " (" + sourceLang + ")"

        self.sourceWord = Label(root, text=text.capitalize(), font=("Helvetica", 15))
        self.langLabel = Label(root, text=lang.capitalize(), font=("Helvetica", 10))
        self.entry = Entry(root, width=30, borderwidth=2, fg='#000000', relief=GROOVE, font=("Helvetica", 13))
        self.noProgressGain = False

        self.langLabel.grid(row=2, column=0, pady=(0,5))
        self.sourceWord.grid(row=0, column=0, pady=(0,5))
        self.entry.grid(row=1, column=0, ipady=6, ipadx=3, pady=(0,5))

        self.entry.bind('<KeyPress>', self.colorToBlack)

    def getEntry(self):
        return self.entry.get()

    def colorToBlack(self, event):
        self.entry.configure(fg='#000000')

    def colorText(self, answer):
        entry = self.entry.get()
        if answer.upper() == entry.upper():
            self.entry.configure(fg='#09C703')
        else:
            self.entry.config(fg='#F31414')

    def destroy(self):
        self.langLabel.destroy()
        self.sourceWord.destroy()
        self.entry.destroy()
