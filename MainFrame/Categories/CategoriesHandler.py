from tkinter import *
from tkinter import ttk
from GUIAssets import CategoryDropdown, DictionaryTableRow
from MainFrame.Categories import AddCategory as ac


class CategoriesFrame(Frame):

    def __init__(self, logObj, root, user):
        self.logObj = logObj
        self.logObj.simpleLog("Creating Categories Frame...")
        self.user = user

        Frame.__init__(self, master=root, bg='white')
        self.pack_propagate(0)
        self.pack(fill=BOTH, expand=1)
        self.frame = Frame(self, bg='white')
        self.frame.pack(fill=BOTH, expand=True)
        self.categoryMainFrame = None

        self.tableRows = [None]

        self.topFrame = Frame(self.frame, bg='white')
        self.topFrame.pack_propagate(0)
        self.topFrame.pack(side=TOP, fill='x')
        Label(self.topFrame, text='Kategóriák', bg='white', font=("Helvetica", 38), anchor='w').grid(row=0, column=0)
        ttk.Separator(self.topFrame, orient=HORIZONTAL).grid(row=1, column=0, sticky="ew")
        Label(self.topFrame, text="Válasszon innen: ", bg='white', font=("Helvetica", 11)).grid(row=0, column=1, sticky=S, padx=(180,0))
        self.categoryDropdown = CategoryDropdown.CategoryDropdown(self.logObj, self.topFrame, self.user, self)

        self.botFrame = Frame(self.frame, bg='white')
        self.botFrame.pack(side='top')
        self.botInnerFrame = Frame(self.botFrame, bg='white')
        self.botInnerFrame.grid(sticky=N)
        self.header = DictionaryTableRow.TableHeader(self.logObj, self.user, self.botInnerFrame, self, False)

        self.addCategoryButton = Button(self.botInnerFrame, text='Új kategória', command=self.addNewCategory, bg='white', activebackground='white', font=('Helvetica', 11))
        try:
            self.addCategoryButton.grid(row=2, columnspan=len(self.user.languages), sticky=S+E, pady=(20,20))
        except TclError:
            self.addCategoryButton.grid(row=2, sticky=S+E, pady=(20,20))

        self.refreshBottomFrame()

    def refreshBottomFrame(self):
        try:
            self.categoryMainFrame.destroy()
        except AttributeError:
            pass

        cmfWidth = len(self.user.languages) * 22
        self.categoryMainFrame = Frame(self.botInnerFrame, bg='white')
        self.grid_propagate(0)

        try:
            self.categoryMainFrame.grid(row=1, columnspan=len(self.user.languages), sticky='news')
        except TclError:
            self.categoryMainFrame.grid(row=1, sticky='news')

        self.canvas = Canvas(self.categoryMainFrame, bg='white')
        self.canvas.config(width=cmfWidth)
        self.canvas.grid(row=0, column=0, sticky='news')

        self.scrollbar = Scrollbar(self.categoryMainFrame, orient="vertical", command=self.canvas.yview)
        self.scrollbar.grid(row=0, column=1, sticky='ns')
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.frameInCanvas = Frame(self.canvas, bg='white')
        self.window = self.canvas.create_window((0, 0), window=self.frameInCanvas, anchor='nw')

        self.categoryMainFrame.columnconfigure(0, weight=1)
        self.categoryMainFrame.rowconfigure(0, weight=1)

        self.frameInCanvas.bind("<Configure>", self.resize)
        self.canvas.bind("<Configure>", self.frameWidth)

    def resize(self, event=None):
        self.canvas.configure(scrollregion=self.canvas.bbox('all'))

    def frameWidth(self, event):
        canvasWidth = event.width
        self.canvas.itemconfig(self.window, width=canvasWidth)

    def displayTable(self, value):
        self.refreshBottomFrame()
        self.emptyListToNones()

        wordIDs = self.getWordIDsFromCategory(value)
        try:
            c = 0
            for wordID in wordIDs:
                self.tableRows.append(DictionaryTableRow.TableRow(self.logObj, wordID, self.user, self.frameInCanvas, self, c, False))
                c = c + 1
        except TypeError:
            pass

    def addNewCategory(self):
        ac.AddCategory(self.logObj, self.user)
        self.categoryDropdown.destroy()
        self.categoryDropdown = CategoryDropdown.CategoryDropdown(self.logObj, self.topFrame, self.user, self)

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
