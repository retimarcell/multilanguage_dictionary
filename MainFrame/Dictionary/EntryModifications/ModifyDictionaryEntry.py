from tkinter import *
import tkinter.messagebox as mb
from GUIAssets import CategoryDropdown


class ModifyEntryWindow:

    def __init__(self, logObj, user, tableRow):
        self.logObj = logObj
        self.logObj.simpleLog("Opening entry modification window...")
        self.tableRow = tableRow
        self.user = user

        self.root = Tk()
        self.root.title("Szó módosítása")
        self.root.configure(bg='white')
        ws = self.root.winfo_screenwidth() / 2 - 300
        hs = self.root.winfo_screenheight() / 2 - 300
        self.root.geometry('+%d+%d' % (ws, hs))
        self.root.resizable(width=FALSE, height=FALSE)

        self.wordLabels = []
        self.wordNewEntries = []
        self.wordChangeButtons = []
        self.middleFrame = Frame(self.root, bg='white')
        self.bottomFrame = Frame(self.root, bg='white')
        self.confirmButton = None
        self.cancelButton = None

        self.setupWindow()
        self.placeWidgets()

        self.wordNewEntries[0].focus_force()

        self.root.mainloop()

    def setupWindow(self):
        self.logObj.simpleLog("Creating Labels and Buttons...")

        for i in range(len(self.tableRow.buttons)):
            textTemp = self.tableRow.getButtonText(i)
            self.wordLabels.append(Label(self.root, text="%s (%s)" % (textTemp, self.user.languages[i].language), font=("Helvetica", 13), bg='white'))
            self.wordNewEntries.append(Entry(self.root, width=25, borderwidth=2, fg='#000000', relief=GROOVE, font=("Helvetica", 13), bg='white'))
            self.wordChangeButtons.append(Button(self.root, text='Megváltoztat', command=lambda x=i: self.changeLabelBasedOnEntry(x), bg='white', font=("Helvetica", 11)))

        Label(self.middleFrame, text="Kategóriák:", font=("Helvetica", 13), bg='white').grid(row=0, column=0, sticky=E, padx=(0,10))
        self.categories = CategoryDropdown.CategorySelectionDropdown(self.logObj, self.middleFrame, self.user, self.tableRow.wordID, self)
        self.categoriesCheckLabel = Label(self.middleFrame, text="Kiválasztott kategóriák: ", font=("Helvetica", 13), bg='white')

        text = ""
        for cat in self.user.categories:
            if self.tableRow.wordID in cat.wordIDs:
                text = "%s%s " % (text, cat.category)
        if len(text) != 0:
            text = text[:-1]
        self.categoriesListLabel = Label(self.middleFrame, text=text, font=("Helvetica", 13), bg='white')

        self.categoriesCheckLabel.grid(row=1, column=0, sticky=E, padx=(0,10))
        self.categoriesListLabel.grid(row=1, column=1, sticky=W, padx=(0,10))

        self.confirmButton = Button(self.bottomFrame, text='Véglegesités', command=self.confimChanges, bg='white', font=("Helvetica", 11), activebackground='white')
        self.cancelButton = Button(self.bottomFrame, text='Mégse', command=self.cancelChanges, bg='white', font=("Helvetica", 11), activebackground='white')

    def placeWidgets(self):
        self.logObj.simpleLog("Placing widgets on grid...")

        for i in range(len(self.wordLabels)):
            self.wordLabels[i].configure(width=30)
            self.wordLabels[i].grid(row=i, column=0, sticky=E, pady=(3,0))
            self.wordNewEntries[i].grid(row=i, column=1, sticky=E, padx=(10,0), pady=(3,0))
            self.wordChangeButtons[i].grid(row=i, column=2, sticky=E, padx=(10,2), pady=(3,0))

        bottomButtonRow = len(self.wordLabels)
        self.middleFrame.grid(row=bottomButtonRow, columnspan=3, sticky=E, pady=(12,10))
        self.bottomFrame.grid(row=bottomButtonRow + 1, columnspan=3, pady=(0,5))
        self.confirmButton.configure(width=10)
        self.cancelButton.configure(width=10)
        self.confirmButton.grid(row=0, column=0, sticky=E, padx=(0,2))
        self.cancelButton.grid(row=0, column=1, sticky=E, padx=(2,0))

    def changeLabelBasedOnEntry(self, index):
        tempText = self.wordNewEntries[index].get()
        self.logObj.simpleLog("Changing Label based on entry: [%s] --> [%s]" % (self.wordLabels[index]['text'], tempText))
        self.wordLabels[index].configure(text="%s (%s)" % (tempText, self.user.languages[index].language))
        self.wordNewEntries[index].delete(0, END)
        self.root.update()

    def confimChanges(self):
        self.logObj.simpleLog("Updating database with new values...")

        if self.confirmChangesPopup():
            for i in range(len(self.tableRow.buttons)):
                newValue = self.wordLabels[i].cget('text')
                word = newValue.split()[0]
                if self.tableRow.getButtonText(i) != word:
                    self.updateWord(i, word)

            labelText = self.categoriesListLabel['text']
            for cat in self.user.categories:
                if cat.category in labelText and self.tableRow.wordID not in cat.wordIDs:
                    self.addWordToCategory(cat)
                elif cat.category not in labelText and self.tableRow.wordID in cat.wordIDs:
                    self.removeWordFromCategory(cat)

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

    def addWordToCategory(self, categoryObj):
        self.user.database.insertIntoTable("Categories", [categoryObj.category, self.user.username, self.tableRow.wordID])
        categoryObj.wordIDs.append(self.tableRow.wordID)

    def removeWordFromCategory(self, categoryObj):
        self.user.database.deleteRow("Categories", ["category", "wordID", "username"], [categoryObj.category, self.tableRow.wordID, self.user.username])
        categoryObj.wordIDs.remove(self.tableRow.wordID)

    def appendToCategories(self, item):
        labelText = self.categoriesListLabel['text']
        if item in labelText:
            labelText = labelText.replace(item, '')
            labelText = labelText.replace('  ', ' ')
        else:
            labelText = "%s %s" % (labelText, item)
        self.categoriesListLabel.configure(text=labelText)
