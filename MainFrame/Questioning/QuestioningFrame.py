from tkinter import *

class QuestioningFrame(Frame):

    def __init__(self, logObj, root, setupOptions, user):
        self.logObj = logObj
        self.logObj.simpleLog("Creating Questioning Frame...")
        self.options = setupOptions

        Frame.__init__(self, master=root)
        self.grid()
        self.amountOf = self.getAmount()



    def getAmount(self):
        if self.options.mode == "Normál":
            return 15
        elif self.options.mode == "Nehezitett":
            return 30
        return 10
