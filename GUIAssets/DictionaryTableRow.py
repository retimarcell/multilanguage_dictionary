from tkinter import *
from MainFrame.Dictionary import ModifyDictionaryEntry as mde
from MainFrame.Dictionary import DeleteDictionaryEntry as dde

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
        self.root = root
        self.user = user

        self.buttons = []

        for i in range(len(self.user.languages)):
            wordDataArr = self.user.languages[i].getWordAndProgress(wordID)
            self.buttons.append(Button(self.root, text=wordDataArr[0], borderwidth=1, relief="solid", width=20))
            self.setProgressColor(self.buttons[i], wordDataArr[1])
            self.buttons[i].grid(row=rowNum, column=i)
            self.buttons[i].bind('<Double-Button-1>', lambda x=i: self.doubleClick(x))
            self.buttons[i].bind('<Button-3>', lambda event, x=rowNum: self.showRightClickOptions(event, x))

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

    def showRightClickOptions(self, event, rowNum):
        popup = Menu(self.root, tearoff=0)
        popup.add_command(label='Szerkesztés', command=lambda x=rowNum: self.modify(rowNum))
        popup.add_command(label='Törlés', command=lambda x=rowNum: self.delete(rowNum))
        try:
            popup.tk_popup(event.x_root, event.y_root, 0)
        finally:
            popup.grab_release()

    def modify(self, rowNum):
        mde.ModifyEntryWindow(self.logObj, self.user, self)
        self.root.displayTable()

    def delete(self, rowNum):
        dde.deleteWholeEntry(self.logObj, self.user, self)
        self.root.tableRows.pop(rowNum)
        self.root.displayTable()
