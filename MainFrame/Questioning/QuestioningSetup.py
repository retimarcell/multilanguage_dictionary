from tkinter import *
from GUIAssets import QuestioningSetupDropdown as qsd
from MainFrame.Questioning.Objects import SetupOptions as so


class QuestioningSetupFrame(Frame):

    def __init__(self, logObj, root, user):
        self.logObj = logObj
        self.logObj.simpleLog("Creating Questioning Setup Frame...")
        self.user = user

        Frame.__init__(self, master=root)
        self.pack_propagate(0)
        self.grid(row=0, sticky=NSEW, padx=(440,0), pady=(60,0))

        self.setupLabels()
        self.setupDropdowns()

    def setupLabels(self):
        self.logObj.simpleLog("Creating setup Labels.")
        Label(self, text='Kérem válassza ki a kikérdezéshez tartozó modifikációkat!', font=("Helvetica", 15)).grid(row=0, columnspan=2, pady=(0,20))
        self.categoryLabel = Label(self, text='Kategória: ', font=("Helvetica", 11))
        self.languageFilterLabel = Label(self, text='Nyelv: ', font=("Helvetica", 11))
        self.sourceLanguageLabel = Label(self, text='Source Nyelv: ', font=("Helvetica", 11))
        self.modeLabel = Label(self, text='Modifikáció: ', font=("Helvetica", 11))

        self.categoryLabel.grid(row=1, column=0, sticky=E, padx=(0,10), pady=(5,0))
        self.languageFilterLabel.grid(row=2, column=0, sticky=E, padx=(0,10), pady=(5,0))
        self.sourceLanguageLabel.grid(row=3, column=0, sticky=E, padx=(0,10), pady=(5,0))
        self.modeLabel.grid(row=4, column=0, sticky=E, padx=(0,10), pady=(5,0))

    def setupDropdowns(self):
        self.categoryDropdown = qsd.QuestioningDropdown(self.logObj, self, "category", self.user, 1, 1)
        self.languageDropdown = qsd.QuestioningDropdown(self.logObj, self, "language", self.user, 2, 1)
        self.sourceLanguageDropdown = qsd.QuestioningOptionMenu(self.logObj, self, "source language", self.user, 3, 1)
        self.modeDropdown = qsd.QuestioningOptionMenu(self.logObj, self, "mode", self.user, 4, 1)

    def getSetup(self):
        lang = self.languageDropdown.getSelectedOptions()
        cat = self.categoryDropdown.getSelectedOptions()
        source = self.sourceLanguageDropdown.getSelectedOption()
        mode = self.modeDropdown.getSelectedOption()
        setupOptions = so.SetupOptions(self.logObj, lang, cat, source, mode)
        return setupOptions
