from tkinter import *


class QuestionElement:

    def __init__(self, root, lang, label, sourceLang=""):

        if sourceLang == "":
            self.sourceLangLabel = Label(root, text="?", font=("Helvetica", 15), bg='white')
        else:
            self.sourceLangLabel = Label(root, text=sourceLang.capitalize(), font=("Helvetica", 15), bg='white')

        self.sourceWord = Label(root, text=label.capitalize(), font=("Helvetica", 23), bg='white')
        self.midLabel = Label(root, text="-->", font=("Helvetica", 11), bg='white')
        self.langLabel = Label(root, text=lang.capitalize(), font=("Helvetica", 15), bg='white')
        self.entry = Entry(root, width=30, borderwidth=2, fg='#000000', relief=GROOVE, font=("Helvetica", 13), bg='white', justify='center')
        self.noProgressGain = False

        self.sourceWord.grid(row=0, columnspan=3, pady=(0,5), sticky=W+E+S+N)
        self.sourceLangLabel.grid(row=1, column=0, pady=(0,5), sticky=E)
        self.midLabel.grid(row=1, column=1, pady=(0,5), padx=(3,3), sticky=W+E)
        self.langLabel.grid(row=1, column=2, pady=(0,5), sticky=W)
        self.entry.grid(row=2, columnspan=3, ipady=6, ipadx=3, pady=(0,5), sticky=W+E+S+N)

        self.entry.bind('<KeyPress>', self.colorToBlack)
        self.entry.focus()

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
        self.sourceLangLabel.destroy()
        self.midLabel.destroy()
