from tkinter import *
from MainFrame.Questioning.Objects import Questions, Answer
from GUIAssets import QuestionElement
from tkinter import messagebox


class QuestioningFrame(Frame):

    def __init__(self, logObj, root, setupOptions, user):
        self.logObj = logObj
        self.logObj.simpleLog("Creating Questioning Frame...")
        self.options = setupOptions
        self.user = user
        self.root = root
        self.isStart = True

        Frame.__init__(self, master=self.root, bg='white')
        self.pack_propagate(0)
        self.grid(row=2, sticky=NSEW, padx=355, pady=100)

        self.amountOf = self.getAmount()
        self.questions = Questions.getQuestions(logObj, self.user, self.amountOf, self.options)
        if len(self.questions) == 0:
            messagebox.showerror("Hiba", "A beállításokhoz nincs kikérdezhető szó.")
            self.destroy()
            self.root.createQuestioningSetupFrame()
        self.currentQuestion = 0
        self.rightAnswers = 0
        self.questionObject = None
        self.answers = []

        self.createFrames()

        self.play()

    def getAmount(self):
        if self.options.mode == "Normál":
            return 15
        elif self.options.mode == "Nehezitett":
            return 30
        return 10

    def createFrames(self):
        self.logObj.simpleLog("Creating Frames")

        self.leftFrame = Frame(self, bg='white')
        self.rightFrame = Frame(self, bg='white')
        self.rightFrame.pack_propagate(0)

        self.leftFrame.grid(row=0, column=0, padx=(0, 20))
        self.rightFrame.grid(row=0, column=1, padx=(20, 0))

        self.setupButtons()

        self.configureLeftFrame()

    def setupButtons(self):
        self.nextButton = Button(self.leftFrame, text='Következő', command=self.play, bg='white', activebackground='white', font=("Helvetica", 11))
        self.nextButton.bind('<Return>', self.play)
        self.nextButton.grid(row=3, columnspan=3, sticky=E, padx=(0,12))

    def configureLeftFrame(self):
        self.logObj.simpleLog("Creating left frame")

        Label(self.rightFrame, text="Haladás", font=("Helvetica", 14), bg='white').grid(row=0, sticky=W)
        self.questionsLeftLabel = Label(self.rightFrame, font=("Helvetica", 11), bg='white')
        self.questionsAnsweredLabel = Label(self.rightFrame, font=("Helvetica", 11), bg='white')

        self.questionsLeftLabel.grid(row=1, sticky=W)
        self.questionsAnsweredLabel.grid(row=2, sticky=W)

        self.helpAmounts = []
        Label(self.rightFrame, text="Segítségek", font=("Helvetica", 14), bg='white').grid(row=3, sticky=W, pady=(20,0))
        self.fullWordHelpButton = self.setupHelpButton("FullWord", 4)
        self.startLetterHelpButton = self.setupHelpButton("StartLetter", 5)
        self.checkHelpButton = self.setupHelpButton("Check", 6)

        self.helpButtons = [self.fullWordHelpButton, self.startLetterHelpButton, self.checkHelpButton]

    def setupHelpButton(self, hType, rowC):
        index = self.user.getHelpIndex(hType)
        self.helpAmounts.append(self.user.helps[index].amount)
        btn = Button(self.rightFrame,
                     text="%s: %i" % (self.user.helps[index].text, self.user.helps[index].amount),
                     font=("Helvetica", 11),
                     width=17,
                     bg='white',
                     activebackground='white',
                     command=lambda x=hType, z=rowC-4: self.helpActivated(x, z))
        btn.grid(row=rowC, sticky=W)

        return btn

    def play(self, event=None):
        self.logObj.simpleLog("[Questioning] Play pushed")
        if not self.isStart:
            self.analyzeAnswer()
            self.currentQuestion += 1
            self.questionObject.destroy()
            self.questionObject = None
        else:
            self.isStart = False

        self.questionsLeftLabel.config(text='Kérdések: %i/%i' % (self.currentQuestion + 1, len(self.questions)))
        self.questionsAnsweredLabel.config(text='Jól megválaszolt kérdések: %i/%i' % (self.rightAnswers, self.currentQuestion))

        if self.currentQuestion < len(self.questions):
            if self.amountOf == 30:
                self.questionObject = QuestionElement.QuestionElement(self.leftFrame, self.questions[self.currentQuestion].answerLang, self.questions[self.currentQuestion].label)
            else:
                self.questionObject = QuestionElement.QuestionElement(self.leftFrame, self.questions[self.currentQuestion].answerLang, self.questions[self.currentQuestion].label, self.questions[self.currentQuestion].sourceLang)
            self.questionObject.entry.bind('<Return>', self.play)
        else:
            self.finalizeQuestioning()

    def helpActivated(self, hType, index):
        if self.helpAmounts[index] != 0:

            remainingAmount = self.removeHelpFromUser(hType, index)
            prevText = self.helpButtons[index].cget('text').split(':')[0]
            self.helpButtons[index].configure(text="%s: %i" % (prevText, remainingAmount))
            self.helpAmounts[index] = self.helpAmounts[index] - 1

            if hType == "FullWord":
                self.setEntry(self.questions[self.currentQuestion].answer)
            elif hType == "StartLetter":
                self.setEntry(self.questions[self.currentQuestion].answer[0])
            elif hType == "Check":
                self.questionObject.colorText(self.questions[self.currentQuestion].answer)

    def removeHelpFromUser(self, hType, buttonIndex):
        helpIndex = self.user.getHelpIndex(hType)
        self.user.helps[helpIndex].amount = self.user.helps[helpIndex].amount - 1

        remainingAmount = self.user.helps[helpIndex].amount
        self.user.database.updateHelp(remainingAmount, hType, self.user.username)
        return remainingAmount

    def setEntry(self, value):
        self.questionObject.entry.delete(0, END)
        self.questionObject.entry.insert(0, value)
        self.questionObject.entry.configure(fg='#000000')

    def analyzeAnswer(self):
        givenAnswer = self.questionObject.getEntry()
        tempAnswerObj = Answer.Answer(self.logObj, self.questions[self.currentQuestion], givenAnswer)
        self.answers.append(tempAnswerObj)
        if givenAnswer.upper() == self.questions[self.currentQuestion].answer.upper():
            self.rightAnswers += 1

    def finalizeQuestioning(self):
        self.logObj.createQuestioningReport(self.answers)

        self.user.lastAnswers = self.answers.copy()
        self.root.finishQuestioning()

    def fullDestroy(self):
        self.leftFrame.destroy()
        self.rightFrame.destroy()
        self.destroy()
