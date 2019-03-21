from tkinter import *


class ReportFrame(Frame):

    def __init__(self, logObj, root, user):
        self.logObj = logObj
        self.logObj.simpleLog("Creating questioning report frame...")

        self.root = root
        self.user = user

        Frame.__init__(self, master=self.root)
        self.grid()

        self.user.saveProgress()

        # TODO after showing, remove done challenges from user
