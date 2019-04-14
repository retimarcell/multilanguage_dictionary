from tkinter import *
from GUIAssets import DictionaryTableRow as dtr
from MainFrame.Dictionary.EntryModifications import AddDictionaryEntry as ade
from MainFrame.Dictionary.LanguageModifications import AddLanguage as al


class DictionaryFrame(Frame):

    def __init__(self, logObj, root, user):
        self.logObj = logObj
        self.logObj.simpleLog("Creating Dictionary Frame...")
        self.user = user

        Frame.__init__(self, master=root)
        self.pack_propagate(0)
        self.pack(fill=BOTH, expand=1)
        self.frame = Frame(self)
        self.frame.pack(anchor='c')

        self.topFrame = Frame(self.frame)
        self.topFrame.grid(row=0)

        self.tableHeader = dtr.TableHeader(self.logObj, self.user, self.topFrame, self)

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
                self.tableRows[rowNum] = dtr.TableRow(self.logObj, self.user.wordIDs[i], self.user, self.topFrame, rowNum + 1)
            i += 1

    def createPageButtons(self):
        colnum = len(self.tableRows[0].buttons)

        self.botFrame = Frame(self.frame)
        self.botFrame.grid(row=1, sticky=S)
        self.botInnerFrame = Frame(self.botFrame)
        self.botInnerFrame.pack_propagate(0)
        self.botInnerFrame.pack(side=BOTTOM, anchor='c')

        self.prevButton = Button(self.botInnerFrame, text="Előző", command=lambda x=-1: self.changeDisplay(x), relief=GROOVE, font=("Helvetica", 11), width=10)
        self.nextButton = Button(self.botInnerFrame, text="Következő", command=lambda x=1: self.changeDisplay(x), relief=GROOVE, font=("Helvetica", 11), width=10)
        self.addEntryButton = Button(self.botInnerFrame, text="Új szó", command=self.addWord, relief=GROOVE, font=("Helvetica", 11), width=10)
        self.addLanguageButton = Button(self.botInnerFrame, text="Új nyelv", command=self.addLanguage, relief=GROOVE, font=("Helvetica", 11), width=10)

        self.prevButton.grid(row=0, column=2, sticky=S+E)
        self.nextButton.grid(row=0, column=3, sticky=S+E)
        self.addEntryButton.grid(row=0, column=0, sticky=S+W)
        self.addLanguageButton.grid(row=0, column=1, sticky=S+W)

    def changeDisplay(self, changeNum):
        if (changeNum == -1 and self.pageNumber == 0) or (changeNum == 1 and self.pageNumber == self.maxPageNumber):
            self.logObj.simpleLog("Button not changing display on purpose")
        else:
            self.logObj.simpleLog("Changing displayed words in table...")
            self.pageNumber += changeNum
            self.displayTable(self.pageNumber)

    def addWord(self):
        ADE = ade.AddEntry(self.logObj, self.user)
        self.displayTable()

    def addLanguage(self):
        AL = al.AddLanguage(self.logObj, self.user)
        self.tableHeader.refresh()
        self.displayTable()

    def emptyListToNones(self):
        for ele in self.tableRows:
            if ele is not None:
                try:
                    ele.destroyButtons()
                except:
                    pass
