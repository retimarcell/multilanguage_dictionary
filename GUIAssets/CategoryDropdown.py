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


class CategorySelectionDropdown(OptionMenu):

    def __init__(self, logObj, root, user, wordID, mainRoot):
        self.logObj = logObj
        self.logObj.simpleLog("Creating Category Selection dropdown for word editing")
        self.user = user
        self.mainRoot = mainRoot
        self.options = [" - "]

        for cat in self.user.categories:
            self.options.append(cat.category)

        self.selected = StringVar(root)
        self.selected.set(self.options[0])

        OptionMenu.__init__(self, root, self.selected, *self.options, command=self.addToList)
        self.configure(width=32, indicatoron=True, relief=RIDGE, borderwidth=1, bg='white', activebackground='white')
        self.grid(row=0, column=1, sticky=E, padx=(0,108))

    def addToList(self, event=None):
        selected = self.selected.get()
        if selected != " - ":
            self.mainRoot.appendToCategories(selected)
            self.selected.set(self.options[0])
