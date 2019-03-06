from tkinter import *

class TableHeader:

    def __init__(self, logobj, user, root):
        self.logObj = logobj
        self.logObj.simpleLog("Creating table header row for dictionary")

        for i in range(len(user.languages)):
            e = Label(root, text=user.languages[i].language, borderwidth=4, relief="solid", width=20)
            e.grid(row=0, column=i)


class TableRow:

    def __init__(self, logobj, wordID, user, root, rowNum):
        self.logObj = logobj
        self.logObj.simpleLog("Creating table row for wordID: %i" % wordID)
        self.wordID = wordID

        self.buttons = []

        for i in range(len(user.languages)):
            wordDataArr = user.languages[i].getWordAndProgress(wordID)
            self.buttons.append(Button(root, text=wordDataArr[0], borderwidth=1, relief="solid", width=20))
            self.setProgressColor(self.buttons[i], wordDataArr[1])
            self.buttons[i].grid(row=rowNum, column=i)
            self.buttons[i].bind('<Double-Button-1>', lambda x=i: self.doubleClick(x))

    def setProgressColor(self, button, progress):
        if progress < 20:
            button.configure(bg='red', activebackground='red')
        elif 20 <= progress < 40:
            button.configure(bg='yellow', activebackground='yellow')
        else:
            button.configure(bg='green', activebackground='green')

    def changeButton(self, index, newValue):
        self.buttons[index].configure(text=newValue)
        self.setProgressColor(self.buttons[index], 0)

    def doubleClick(self, index):
        pass
