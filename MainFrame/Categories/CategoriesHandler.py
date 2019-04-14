from tkinter import *
from GUIAssets import CategoryDropdown, DictionaryTableRow
from MainFrame.Categories import AddCategory as ac

class CategoriesFrame(Frame):

    def __init__(self, logObj, root, user):
        self.logObj = logObj
        self.logObj.simpleLog("Creating Categories Frame...")
        self.user = user

        Frame.__init__(self, master=root)
        self.pack_propagate(0)
        self.pack(fill=BOTH, expand=1)
        self.frame = Frame(self)
        self.frame.pack(anchor='c')

        self.tableRows = [None]

        self.topFrame = Frame(self.frame)
        self.topFrame.grid(row=0)
        self.categoryDropdown = CategoryDropdown.CategoryDropdown(self.logObj, self.topFrame, self.user, self)
        self.addCategoryButton = Button(self.topFrame, text='Új kategória', command=self.addNewCategory, relief=GROOVE)
        self.addCategoryButton.grid(row=0, column=1)

        self.botFrame = Frame(self.frame)
        self.botFrame.grid(row=1)
        self.header = DictionaryTableRow.TableHeader(self.logObj, self.user, self.botFrame, self, False)
        self.refreshBottomFrame()

    def refreshBottomFrame(self):
        try:
            self.categoryFrame.destroy()
        except:
            pass

        self.categoryFrame = Frame(self.botFrame)
        self.canvas = Canvas(self.categoryFrame)
        self.frameInCanvas = Frame(self.canvas)
        self.scrollbar = Scrollbar(self.frameInCanvas, orient="vertical", command=self.canvas.yview)

        self.categoryFrame.grid(row=1, columnspan=len(self.user.languages))
        self.canvas.pack(fill=BOTH, expand=1)
        self.canvas.create_window((0, 0), window=self.categoryFrame)
        self.frameInCanvas.pack()

    def displayTable(self, value):
        self.refreshBottomFrame()
        self.emptyListToNones()

        wordIDs = self.getWordIDsFromCategory(value)
        c = 0
        for wordID in wordIDs:
            self.tableRows.append(DictionaryTableRow.TableRow(self.logObj, wordID, self.user, self.frameInCanvas, c, False))
            c = c + 1

    def addNewCategory(self):
        ac.AddCategory(self.logObj, self.user)
        self.categoryDropdown = CategoryDropdown.CategoryDropdown(self.logObj, self.frame, self.user, self)

    def getWordIDsFromCategory(self, value):
        for cat in self.user.categories:
            if cat.category == value:
                return cat.wordIDs

    def emptyListToNones(self):
        for ele in self.tableRows:
            if ele is not None:
                try:
                    ele.destroy()
                except:
                    pass
