from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from GUIAssets import DictionaryTableRow as dtr
from MainFrame.Dictionary.EntryModifications import AddDictionaryEntry as ade
from MainFrame.Dictionary.LanguageModifications import AddLanguage as al


class DictionaryFrame(Frame):

    def __init__(self, logObj, root, user):
        self.logObj = logObj
        self.logObj.simpleLog("Creating Dictionary Frame...")
        self.user = user

        Frame.__init__(self, master=root, bg='white')
        self.pack_propagate(0)
        self.pack(fill=BOTH, expand=True)

        self.headerFrame = Frame(self, bg='white')
        self.headerFrame.pack(fill='x')
        self.setupHeader()

        self.topFrame = Frame(self, bg='white')
        self.topFrame.pack(side='top')
        self.topInnerFrame = Frame(self.topFrame, bg='white')
        self.topInnerFrame.grid(sticky=N)

        self.tableHeader = dtr.TableHeader(self.logObj, self.user, self.topInnerFrame, self)

        self.tableRows = [None for i in range(15)]

        self.pageNumber = 0
        self.maxPageNumber = int(len(self.user.wordIDs) / 15)

        self.displayTable(self.pageNumber)
        self.createPageButtons()

    def setupHeader(self):
        Label(self.headerFrame, text='Szótár', bg='white', font=("Helvetica", 38), anchor='w').grid(row=0, column=0, pady=(0,5), padx=(5,0), sticky=W)
        ttk.Separator(self.headerFrame, orient=HORIZONTAL).grid(row=1, column=0, sticky="ew")
        self.helpButton = Button(self.headerFrame, text='? ', font=("Helvetica", 11), anchor='e', relief=GROOVE, bg='white', height=1, width=2)
        self.helpButton.bind('<Button-1>', lambda x: 'break')
        self.helpButton.bind('<Enter>', self.enter)
        self.helpButton.bind('<Leave>', self.leave)
        self.helpButton.grid(row=0, column=1, pady=(0,5), padx=(1000,5))

    def enter(self, event=None):
        x, y, cx, cy = self.helpButton.bbox("insert")
        x += self.helpButton.winfo_rootx() - 500
        y += self.helpButton.winfo_rooty() + 20
        self.topLevelWidget = Toplevel(self.helpButton)
        self.topLevelWidget.wm_overrideredirect(True)
        self.topLevelWidget.wm_geometry("+%d+%d" % (x,y))
        Label(self.topLevelWidget, text="Szavak színei: (Minél begyakoroltabb, annál kevesebbszer fordul elő kikérdezésen)\n Piros -> Sárga -> Zöld", bg='white', font=("Helvetica", 11), relief=RIDGE, borderwidth=2, anchor='w').pack(fill=BOTH)

    def leave(self, event=None):
        self.topLevelWidget.destroy()

    def displayTable(self, section=None):
        if section is None:
            section = self.pageNumber

        self.emptyListToNones()

        self.logObj.simpleLog("Displaying Page Number %i." % (self.pageNumber+1))
        i = 15*section
        while i != (15 * (section+1)):
            rowNum = int(i % 15)
            if i < len(self.user.wordIDs):
                self.tableRows[rowNum] = dtr.TableRow(self.logObj, self.user.wordIDs[i], self.user, self.topInnerFrame, self, rowNum + 1)
            i += 1

    def createPageButtons(self):
        try:
            colnum = len(self.tableRows[0].buttons)
        except AttributeError:
            colnum = 0

        self.botFrame = Frame(self, bg='white')
        self.botFrame.pack_propagate(0)
        self.botFrame.pack(side="bottom", pady=(0,40))

        self.prevButton = Button(self.botFrame, text="Előző", command=lambda x=-1: self.changeDisplay(x), bg='white', font=("Helvetica", 11), activebackground='white', width=10)
        self.nextButton = Button(self.botFrame, text="Következő", command=lambda x=1: self.changeDisplay(x), bg='white', font=("Helvetica", 11), activebackground='white', width=10)
        self.addEntryButton = Button(self.botFrame, text="Új szó", command=self.addWord, bg='white', font=("Helvetica", 11), activebackground='white', width=10)
        self.addLanguageButton = Button(self.botFrame, text="Új nyelv", command=self.addLanguage, bg='white', font=("Helvetica", 11), activebackground='white', width=10)

        self.prevButton.grid(row=0, column=2, sticky=S+E, padx=(20,0))
        self.nextButton.grid(row=0, column=3, sticky=S+E)
        self.addEntryButton.grid(row=0, column=0, sticky=S+W)
        self.addLanguageButton.grid(row=0, column=1, sticky=S+W, padx=(0,20))

    def changeDisplay(self, changeNum):
        if (changeNum == -1 and self.pageNumber == 0) or (changeNum == 1 and self.pageNumber == self.maxPageNumber):
            self.logObj.simpleLog("Button not changing display on purpose")
        else:
            self.logObj.simpleLog("Changing displayed words in table...")
            self.pageNumber += changeNum
            self.displayTable(self.pageNumber)

    def addWord(self):
        if len(self.user.languages) == 0:
            messagebox.showerror("Hiba", "Előbb vegyen fel nyelvet, hogy hozzá tudjon adni szót!")
        else:
            ade.AddEntry(self.logObj, self.user)
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
