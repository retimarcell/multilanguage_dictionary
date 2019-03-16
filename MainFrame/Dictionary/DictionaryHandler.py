from tkinter import *
import math
from GUIAssets import DictionaryTableRow as dtr
from MainFrame.Dictionary import AddDictionaryEntry as ade

class DictionaryFrame(Frame):

    def __init__(self, logObj, root, user):
        self.logObj = logObj
        self.logObj.simpleLog("Creating Dictionary Frame...")
        self.user = user

        Frame.__init__(self, master=root, width=1344, height=720)
        self.grid()

        self.tableHeader = dtr.TableHeader(self.logObj, self.user, self)

        self.tableRows = [None for i in range(15)]

        self.pageNumber = 0
        self.maxPageNumber = int(len(self.user.wordIDs) / 15)

        self.displayTable(self.pageNumber)
        self.createPageButtons()

    def displayTable(self, section=None):
        if section is None:
            section = self.pageNumber

        self.emptyListToNones()

        self.logObj.simpleLog("Displaying Page Number %i." % (self.pageNumber+1))
        i = 15*section
        while i != (15 * (section+1)):
            rowNum = int(i % 15)
            if i < len(self.user.wordIDs):
                self.tableRows[rowNum] = dtr.TableRow(self.logObj, self.user.wordIDs[i], self.user, self, rowNum + 1)
            i += 1

    def createPageButtons(self):
        self.addEntryButton = Button(self, text="Új", command=self.addWord)
        self.prevButton = Button(self, text="Előző", command=lambda x=-1: self.changeDisplay(x))
        self.nextButton = Button(self, text="Következő", command=lambda x=1: self.changeDisplay(x))

        colnum = len(self.tableRows[0].buttons)
        self.addEntryButton.grid(row=16, column=colnum-2)
        self.prevButton.grid(row=16, column=colnum-1)
        self.nextButton.grid(row=16, column=colnum)

    def changeDisplay(self, changeNum):
        if (changeNum != -1 or self.pageNumber != 0) or (changeNum != 1 or self.pageNumber != self.maxPageNumber):
            self.logObj.simpleLog("Changing displayed words in table...")
            self.pageNumber += changeNum
            self.displayTable(self.pageNumber)
        else:
            self.logObj.simpleLog("Button not changing display on purpose")

    def addWord(self):
        ADE = ade.AddEntry(self.logObj, self.user)
        self.displayTable()

    def emptyListToNones(self):
        for ele in self.tableRows:
            if ele is not None:
                try:
                    ele.destroy()
                except:
                    pass
