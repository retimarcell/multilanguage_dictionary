from tkinter import *
from MainFrame.Questioning import QuestioningSetup as qs
from MainFrame.Questioning import QuestioningFrame as qf
from MainFrame.Questioning import QuestioningReportFrame as qrf


class QuestioningFrame(Frame):

    def __init__(self, logobj, root, user):
        self.logObj = logobj
        self.logObj.simpleLog("Creating base frame for questioning...")
        self.user = user

        Frame.__init__(self, master=root, width=1344, height=720)
        self.grid()

        self.createQuestioningSetupFrame()

    def createQuestioningSetupFrame(self):
        self.showedFrame = qs.QuestioningSetupFrame(self.logObj, self, self.user)

        self.submitButton = Button(self, text="OK", width=10, command=self.startQuestioning)
        self.submitButton.grid(row=1, sticky=E)

    def startQuestioning(self):
        self.setupOptions = self.showedFrame.getSetup()
        self.showedFrame.destroy()
        self.submitButton.destroy()

        self.createQuestioningFrame()

    def createQuestioningFrame(self):
        self.showedFrame = qf.QuestioningFrame(self.logObj, self, self.setupOptions, self.user)

    def finishQuestioning(self):
        self.showedFrame.destroy()
        self.showedFrame = qrf.ReportFrame(self.logObj, self, self.user)
