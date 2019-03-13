from tkinter import *
from MainFrame.Questioning.Objects import Questions, Answer
from GUIAssets import QuestionElement


class QuestioningFrame(Frame):

    def __init__(self, logObj, root, setupOptions, user):
        self.logObj = logObj
        self.logObj.simpleLog("Creating Questioning Frame...")
        self.options = setupOptions
        self.user = user

        Frame.__init__(self, master=root)
        self.grid()

        self.amountOf = self.getAmount()
        self.questions = Questions.getQuestions(logObj, self.user, self.amountOf, self.options)
        self.currentQuestion = 0
        self.questionObject = None
        self.answers = []

        self.createFrames()

        self.play(True)

    def getAmount(self):
        if self.options.mode == "Normál":
            return 15
        elif self.options.mode == "Nehezitett":
            return 30
        return 10

    def createFrames(self):
        self.logObj.simplelog("Creating Frames")

        self.leftFrame = Frame(self)
        self.rightFrame = Frame(self)

        self.leftFrame.grid(row=0, column=0)
        self.rightFrame.grid(row=0, column=1)

        self.setupButtons()

        self.configureLeftFrame()

    def setupButtons(self):
        self.nextButton = Button(self.leftFrame, text='Következő', command=self.play)

    def configureLeftFrame(self):
        self.questionsLeftLabel = Label(self.rightFrame, text='Hátralévő kérdések: ')
        self.questionsAnsweredLabel = Label(self.rightFrame, text='Jól megválaszolt kérdések: ')

        self.questionsLeftLabel.grid(row=0)
        self.questionsAnsweredLabel.grid(row=1)

    def play(self, isStart=False):

        if not isStart:
            self.analizeAnswer()
            self.currentQuestion += 1

        if self.currentQuestion < len(self.questions):
            self.questionObject = QuestionElement.QuestionElement(self.leftFrame, self.questions[self.currentQuestion])
        else:
            self.finalizeQuestioning()

    def analizeAnswer(self):
        givenAnswer = self.questionObject.getEntry()
        tempAnswerObj = Answer.Answer(self.questions[self.currentQuestion], givenAnswer)
        self.answers.append(tempAnswerObj)

    def finalizeQuestioning(self):
        pass
