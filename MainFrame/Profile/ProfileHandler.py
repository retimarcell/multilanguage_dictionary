from tkinter import *

class ProfileFrame(Frame):

    def __init__(self, logObj, root, user):
        self.logObj = logObj
        self.logObj.simpleLog("Creating Profile Frame...")
        self.user = user

        Frame.__init__(self, master=root, width=1344, height=720)
        self.grid()
