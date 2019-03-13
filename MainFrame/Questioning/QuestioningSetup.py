from tkinter import *
from GUIAssets import QuestioningSetupDropdown as qsd
from MainFrame.Questioning.Objects import SetupOptions as so


class QuestioningSetupFrame(Frame):

    def __init__(self, logObj, root, user):
        self.logObj = logObj
        self.logObj.simpleLog("Creating Questioning Setup Frame...")
        self.user = user

        Frame.__init__(self, master=root)
        self.grid(row=0)

        self.setupLabels()
        self.setupDropdowns()

    def setupLabels(self):
        self.logObj.simpleLog("Creating setup Labels.")
        self.categoryLabel = Label(self, text='Kategória: ')
        self.languageFilterLabel = Label(self, text='Nyelv: ')
        self.sourceLanguageLabel = Label(self, text='Source Nyelv: ')
        self.modeLabel = Label(self, text='Modifikáció: ')

        self.categoryLabel.grid(row=0, column=0)
        self.languageFilterLabel.grid(row=1, column=0)
        self.sourceLanguageLabel.grid(row=2, column=0)
        self.modeLabel.grid(row=3, column=0)

    def setupDropdowns(self):
        self.categoryDropdown = qsd.QuestioningDropdown(self.logObj, self, "category", self.user, 0, 1)
        self.languageDropdown = qsd.QuestioningDropdown(self.logObj, self, "language", self.user, 1, 1)
        self.sourceLanguageDropdown = qsd.QuestioningOptionMenu(self.logObj, self, "source language", self.user, 2, 1)
        self.modeDropdown = qsd.QuestioningOptionMenu(self.logObj, self, "mode", self.user, 3, 1)

    def getSetup(self):
        setupOptions = so.SetupOptions()
        setupOptions.languages = self.languageDropdown.getSelectedOptions()
        setupOptions.categories = self.categoryDropdown.getSelectedOptions()
        setupOptions.source = self.sourceLanguageDropdown.getSelectedOption()
        setupOptions.mode = self.modeDropdown.getSelectedOption()
        return setupOptions
