from tkinter import *


class QuestioningDropdown(Menubutton):

    def __init__(self, logObj, root, type, user, row, col):
        self.logObj = logObj
        self.type = type
        self.logObj.simpleLog("Creating setup Dropdowns for \"%s\"" % self.type)
        self.user = user
        self.choices = {}

        Menubutton.__init__(self, master=root, width=20, indicatoron=True, relief=GROOVE, borderwidth=1)
        self.menu = Menu(self, tearoff=False)
        self.configure(menu=self.menu)
        self.grid(row=row, column=col, sticky=W, padx=(10,0), pady=(5,0))
        self.fillMenu()

    def fillMenu(self):
        self.logObj.simpleLog("Filling Dropdown menu with items for %s" % self.type)
        if self.type == "language":
            for langObj in self.user.languages:
                lang = langObj.language
                self.choices[lang] = IntVar(value=0)
                self.menu.add_checkbutton(label=lang, variable=self.choices[lang], onvalue=1, offvalue=0)
        else:
            for catObj in self.user.categories:
                cat = catObj.category
                self.choices[cat] = IntVar(value=0)
                self.menu.add_checkbutton(label=cat, variable=self.choices[cat], onvalue=1, offvalue=0)

    def getSelectedOptions(self):
        self.logObj.simpleLog("Returning Selected options from %s" % self.type)
        returnArray = []
        for text, value in self.choices.items():
            if value.get() == 1:
                returnArray.append(text)
        self.logObj.arrayItemsLog("The selected items:", returnArray)
        return returnArray


class QuestioningOptionMenu(OptionMenu):

    def __init__(self, logObj, root, type, user, row, col):
        self.logObj = logObj
        self.logObj.simpleLog("Creating setup Option Menu for \"%s\"" % type)

        if type == "mode":
            options = ["Normál", "Nehezitett", "Könnyitett"]
        else:
            options = [" - "]
            for lang in user.languages:
                options.append(lang.language)

        self.selected = StringVar(root)
        self.selected.set(options[0])

        OptionMenu.__init__(self, root, self.selected, *options)
        self.configure(width=20, indicatoron=True, relief=GROOVE, borderwidth=1)
        self.grid(row=row, column=col, sticky=W, padx=(8,0), pady=(5,0))

    def getSelectedOption(self):
        self.logObj.simpleLog("Returning selected option from mode: %s" % self.selected.get())
        return self.selected.get()
