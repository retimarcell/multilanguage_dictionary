from tkinter import *

from MainFrame.Dictionary.EntryModifications import DeleteDictionaryEntry as dde, ModifyDictionaryEntry as mde
from MainFrame.Dictionary.LanguageModifications import DeleteLanguage as dl


class TableHeader:

    def __init__(self, logobj, user, root, mainRoot, isDictionary=True):
        self.logObj = logobj
        self.logObj.simpleLog("Creating table header row for dictionary")
        self.user = user
        self.root = root
        self.mainRoot = mainRoot

        self.headers = []

        self.refresh(isDictionary)

    def refresh(self, isDictionary=True):
        for e in self.headers:
            e.destroy()
        for i in range(len(self.user.languages)):
            e = Button(self.root, text=self.user.languages[i].language.upper(), borderwidth=2, relief="solid", width=19, font=("Helvetica", 12))
            e.bind('<Button-1>', lambda x: 'break')
            e.grid(row=0, column=i, pady=(12,0))
            if isDictionary:
                e.bind('<Button-3>', lambda event, x=i: self.handleDelete(event, x))
            self.headers.append(e)

    def handleDelete(self, event, column):
        popup = Menu(self.root, tearoff=0)
        popup.add_command(label='Törlés', command=lambda x=column: self.delete(column))
        try:
            popup.tk_popup(event.x_root, event.y_root, 0)
        finally:
            popup.grab_release()

    def delete(self, column):
        dl.deleteLanguage(self.logObj, self.user, self.headers[column].cget('text'))
        self.mainRoot.displayTable()


class TableRow:

    def __init__(self, logobj, wordID, user, root, rowNum, isDictionary=True):
        self.logObj = logobj
        self.logObj.simpleLog("Creating table row for wordID: %i" % wordID)
        self.wordID = wordID
        self.root = root
        self.user = user

        self.buttons = []

        for i in range(len(self.user.languages)):
            wordDataArr = self.user.languages[i].getWordAndProgress(wordID)
            try:
                self.buttons.append(Button(self.root, text=wordDataArr[0], borderwidth=1, relief=SOLID, width=22, font=("Helvetica", 10)))
            except TclError:
                pass
            #self.setProgressColor(self.buttons[i], wordDataArr[1])
            self.buttons[i].grid(row=rowNum, column=i)
            self.buttons[i].bind('<Button-1>', lambda e: 'break')
            if isDictionary:
                self.buttons[i].bind('<Button-3>', lambda event, x=rowNum: self.showRightClickOptions(event, x))

    def getButtonText(self, i):
        self.logObj.simpleLog("Returning table row text: %s" % self.buttons[i].cget('text'))
        return self.buttons[i].cget('text')

    def setProgressColor(self, button, progress):
        if progress < 20:
            button.configure(bg='red', activebackground='red')
        elif 20 <= progress < 40:
            button.configure(bg='yellow', activebackground='yellow')
        else:
            button.configure(bg='green', activebackground='green')

    def changeButton(self, index, newValue):
        self.buttons[index].configure(text=newValue)
        #self.setProgressColor(self.buttons[index], 0)

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

    def destroyButtons(self):
        for button in self.buttons:
            button.destroy()
