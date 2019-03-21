from tkinter import *
from GUIAssets import HeaderButton as hb
from MainFrame.Questioning import QuestioningHandler as qh
from MainFrame.Dictionary import DictionaryHandler as dh
from MainFrame.Challenges import ChallengesHandler as ch
from MainFrame.Profile import  ProfileHandler as ph

class MainWindow:

    def __init__(self, logObj, user, database):
        self.logObj = logObj
        self.user = user
        self.database = database
        self.logObj.simpleLog("Creating Main window...")

        self.createRoot()

        self.createHeaderFrame()

        self.createMainFrame()

        self.root.mainloop()

    def createRoot(self):
        self.logObj.simpleLog("Creating root")

        self.root = Tk()
        self.root.title("Többnyelvű szótár")
        self.root.resizable(width=FALSE, height=FALSE)
        self.root.geometry("1344x756")
        self.root.columnconfigure((0, 1, 2, 3), weight=1, minsize=336)
        self.logObj.simpleLog("Root created")

    def createHeaderFrame(self):
        self.logObj.simpleLog("Creating header frame")
        self.headerButtons = []

        self.headerButtons.append(hb.HeaderButton(self.logObj, self.root, 'Szótár', 0))
        self.headerButtons[0].configure(command=lambda x=0: self.activateFrame(x))
        self.headerButtons.append(hb.HeaderButton(self.logObj, self.root, 'Kikérdezés', 1))
        self.headerButtons[1].configure(command=lambda x=1: self.activateFrame(x))
        self.headerButtons.append(hb.HeaderButton(self.logObj, self.root, 'Kihívások', 2))
        self.headerButtons[2].configure(command=lambda x=2: self.activateFrame(x))
        self.headerButtons.append(hb.HeaderButton(self.logObj, self.root, 'Profil', 3))
        self.headerButtons[3].configure(command=lambda x=3: self.activateFrame(x))

        self.logObj.simpleLog("Header created")

    def createMainFrame(self):
        self.mainFrame = Frame(self.root, background="black", width=1344, height=720)
        self.mainFrame.grid(columnspan=4, row=1)
        self.activateFrame(0, True)

    def activateFrame(self, id, isLaunch=False):
        self.logObj.simpleLog("Frame changing button pushed...")

        if not isLaunch:
            self.deactivatePreviousFrame()

        if id == 0:
            self.showedFrame = dh.DictionaryFrame(self.logObj, self.mainFrame, self.user)
        elif id == 1:
            self.showedFrame = qh.QuestioningFrame(self.logObj, self.mainFrame, self.user)
        elif id == 2:
            self.showedFrame = ch.ChallengesFrame(self.logObj, self.mainFrame, self.user)
        elif id == 3:
            self.showedFrame = ph.ProfileFrame(self.logObj, self.mainFrame, self.user)
        else:
            self.logObj.simpleLog("Frame selection failure!")

    def deactivatePreviousFrame(self):
        self.showedFrame.destroy()
