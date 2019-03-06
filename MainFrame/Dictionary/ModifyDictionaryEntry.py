from tkinter import *
import tkinter.messagebox as mb


class ModifyEntryWindow:

    def __init__(self, logObj, user, tableRow):
        self.logObj = logObj
        self.logObj.simpleLog("Opening entry modification window...")
        self.tableRow = tableRow
        self.user = user

        self.root = Tk()
        self.wordLabels = []
        self.wordNewEntries = []
        self.wordChangeButtons = []
        self.bottomFrame = Frame(self.root)
        self.confirmButton = None
        self.cancelButton = None

        self.root.mainloop()

        self.setupWindow()
        self.placeWidgets()

    def setupWindow(self):
        self.logObj.simpleLog("Creating Labels and Buttons...")

        for i in range(len(self.tablerow.buttons)):
            self.labels.append(Label(self.root, text=(self.tablerow.buttons[i]['text'])))
            self.entries.append(Entry(self.root))
            self.buttons.append(Button(self.root, text='Megváltoztat', command=lambda: self.changeLabelBasedOnEntry(i)))

        self.confirmButton = Button(self.bottomFrame, text='Véglegesités', command=self.confimChanges)
        self.cancelButton = Button(self.bottomFrame, text='Mégse', command=self.cancelChanges)

    def placeWidgets(self):
        self.logObj.simpleLog("Placing widgets on grid...")

        for i in range(len(self.wordLabels)):
            self.wordLabels[i].configure(width=30)
            self.wordLabels[i].grid(row=i, column=0)
            self.wordNewEntries[i].configure(width=[30])
            self.wordNewEntries[i].grid(row=i, column=1)
            self.wordChangeButtons[i].grid(row=i, column=2)

        bottomButtonRow = len(self.wordLabels)
        self.bottomFrame.grid(row=bottomButtonRow, columnspan=3)
        self.confirmButton.configure(width=10)
        self.cancelButton.configure(width=10)
        self.confirmButton.grid(row=0, column=0, sticky=E)
        self.cancelButton.grid(row=0, column=1, sticky=E)

    def changeLabelBasedOnEntry(self, index):
        self.logObj.simpleLog("Changing Label based on entry: [%s] --> [%s]" % (self.wordLabels[index]['text'], self.wordNewEntries[index]['text']))
        self.wordLabels[index].configure(text=self.wordNewEntries[index]['text'])
        self.wordNewEntries[index].delete(0, END)

    def confimChanges(self):
        self.logObj.simpleLog("Updating database with new values...")

        if self.confirmChangesPopup():
            for i in range(len(self.tableRow.buttons)):
                if self.tableRow.buttons[i]['text'] != self.wordNewEntries[i].get():
                    self.updateWord(i)

        self.root.destroy()

    def cancelChanges(self):
        self.logObj.simpleLog("Left word editing window.")
        self.root.destroy()

    def confirmChangesPopup(self):
        self.logObj.simpleLog("Messagebox popup: Word change confirmation.")
        value = mb.askyesno("Megerősités", "A megváltoztatott szavak haladása vissza lesz állitva, igy is folytatni szeretné?")

        if value:
            self.logObj.simpleLog("Confirmed changing values.")
        else:
            self.logObj.simpleLog("Word change confirmation cancelled.")

        return value

    def updateWord(self, index):
        previousValue = self.tableRow.buttons[index]['text']
        newValue = self.wordNewEntries[index].get()
        self.logObj.simpleLog("Updating \"%s\" to \"%s\"" % (previousValue, newValue))

        self.user.database.changeWord(self.user.languages[index].language, previousValue, newValue)
        self.user.languages[index].changeWord(previousValue, newValue)
        self.tableRow.changeButton(index, newValue)
