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

        self.setupWindow()
        self.placeWidgets()

        self.root.mainloop()

    def setupWindow(self):
        self.logObj.simpleLog("Creating Labels and Buttons...")

        for i in range(len(self.tableRow.buttons)):
            textTemp = self.tableRow.getButtonText(i)
            self.wordLabels.append(Label(self.root, text=textTemp))
            self.wordNewEntries.append(Entry(self.root))
            self.wordChangeButtons.append(Button(self.root, text='Megváltoztat', command=lambda x=i: self.changeLabelBasedOnEntry(x)))

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
        tempText = self.wordNewEntries[index].get()
        self.logObj.simpleLog("Changing Label based on entry: [%s] --> [%s]" % (self.wordLabels[index]['text'], tempText))
        self.wordLabels[index].configure(text=tempText)
        self.wordNewEntries[index].delete(0, END)
        self.root.update()

    def confimChanges(self):
        self.logObj.simpleLog("Updating database with new values...")

        if self.confirmChangesPopup():
            for i in range(len(self.tableRow.buttons)):
                newValue = self.wordLabels[i].cget('text')
                if self.tableRow.getButtonText(i) != newValue:
                    self.updateWord(i, newValue)

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

    def updateWord(self, index, newValue):
        previousValue = self.tableRow.getButtonText(index)

        self.logObj.simpleLog("Updating \"%s\" to \"%s\"" % (previousValue, newValue))

        self.user.database.changeWord(self.user.languages[index].language, previousValue, newValue, self.tableRow.wordID)
        self.user.languages[index].changeWord(newValue, self.tableRow.wordID)
        self.tableRow.changeButton(index, newValue)
