from tkinter import *


class CategoryDropdown(OptionMenu):

    def __init__(self, logObj, root, user, mainRoot):
        self.logObj = logObj
        self.logObj.simpleLog("Creating Category Dropdown")
        self.user = user
        self.options = [" - "]

        for cat in self.user.categories:
            self.options.append(cat.category)

        self.selected = StringVar(root)
        self.selected.set(self.options[0])

        OptionMenu.__init__(self, root, self.selected, *self.options, command=mainRoot.displayTable)
        self.configure(width=20, indicatoron=True, relief=RIDGE, borderwidth=1, bg='white', activebackground='white')
        self["menu"].config(bg='white')
        self.grid(row=0, column=2, sticky=S)


class CategorySelectionDropdown(Menubutton):

    def __init__(self, logObj, root, user, wordID):
        self.logObj = logObj
        self.logObj.simpleLog("Creating Category Selection dropdown for word editing")
        self.user = user
        self.root = root
        self.wordID = wordID
        self.choices = {}

        Menubutton.__init__(self, self.root, width=32, indicatoron=True, relief=GROOVE, borderwidth=1, bg='white', activebackground='white')
        self.menu = Menu(self, tearoff=False)
        self.configure(menu=self.menu)
        self.grid(row=0, column=1, sticky=E, padx=(0,108))
        self.fillMenu()

    def fillMenu(self):
        for cat in self.user.categories:
            category = cat.category

            s = IntVar()
            if self.wordID in cat.wordIDs:
                s.set(1)
            else:
                s.set(0)

            self.choices[category] = s
            self.menu.add_checkbutton(label=category, variable=self.choices[category], onvalue=1, offvalue=0, background='white')

    def getSelectedOptions(self):
        returnArray = []
        for text, value in self.choices.items():
            if str(value) == "PY_VAR1":
                returnArray.append(text)
        return returnArray

    def getNotSelectedOptions(self):
        returnArray = []
        for text, value in self.choices.items():
            if str(value) == "PY_VAR0":
                returnArray.append(text)
        return returnArray
