from tkinter import *

class ChallengesFrame(Frame):

    def __init__(self, logObj, root, user):
        self.logObj = logObj
        self.logObj.simpleLog("Creating Challenges Frame...")
        self.user = user

        Frame.__init__(self, master=root, width=1344, height=720)
        self.grid()
