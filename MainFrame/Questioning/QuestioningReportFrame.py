from tkinter import *
from tkinter import ttk


class ReportFrame(Frame):

    def __init__(self, logObj, root, user):
        self.logObj = logObj
        self.logObj.simpleLog("Creating questioning report frame...")

        self.root = root
        self.user = user
        self.rowHelper = 3

        Frame.__init__(self, master=self.root)
        self.pack(anchor='c')

        self.report = self.user.saveProgress()

        self.setupLabels()

        removeableChallenges = []
        challengeFrame = Frame(self)
        challengeFrame.grid(row=self.rowHelper)
        for i in range(len(self.user.challenges)):
            Label(challengeFrame, text=self.user.challenges[i].description, font=("Helvetica", 11)).grid(row=i, column=0, sticky=E, padx=(0,10))

            ttk.Progressbar(challengeFrame, value=self.user.challenges[i].progress, maximum=self.user.challenges[i].amount, length=100).grid(row=i, column=1, sticky=W, padx=(0,10))

            if self.user.challenges[i].isDone:
                labelText = "Kész"
                removeableChallenges.append(self.user.challenges[i])
            else:
                labelText = "%i/%i" % (self.user.challenges[i].progress, self.user.challenges[i].amount)
            Label(challengeFrame, text=labelText, font=("Helvetica", 11)).grid(row=i, column=2, sticky=W)
            self.increaseRowHelper()

        for remCh in removeableChallenges:
            for i in range(len(self.user.challenges)):
                if self.user.challenges[i] == remCh:
                    self.user.challenges.pop(i)
                    break

    def setupLabels(self):
        Label(self, text='A kikérdezés befejeződött.', font=("Helvetica", 15)).grid(row=0, pady=(10,20))

        correctAnswer = 0
        for answer in self.user.lastAnswers:
            if answer.progress == 1:
                correctAnswer = correctAnswer + 1
        Label(self, text='Helyes válaszok: %i/%i' % (correctAnswer, len(self.user.lastAnswers)), font=("Helvetica", 11)).grid(row=1, pady=(0,5))

        Label(self, text='Szerzett tapasztalati pontok: %i' % self.report.finishXp, font=("Helvetica", 11)).grid(row=2, pady=(0,5))

        if self.report.amountOfLevelUps != 0:
            Label(self, text='Szintlépés! Új szint: %i' % self.user.level, font=("Helvetica", 11)).grid(row=3, pady=(0,5))
            self.increaseRowHelper()

        if len(self.report.languageLevelUps) != 0:
            languageLevelUpFrame = Frame(self)
            languageLevelUpFrame.grid(row=self.rowHelper)
            Label(languageLevelUpFrame, text='Nyelv(ek) szintlépése: ', font=("Helvetica", 11)).grid(row=0, column=0)
            self.increaseRowHelper()

            for i in range(len(self.report.languageLevelUps)):
                Label(languageLevelUpFrame, text='- %s: %s. szint' % (self.report.languageLevelUps[i][0], self.report.languageLevelUps[i][1]), font=("Helvetica", 11)).grid(row=i, column=1)

        if len(self.report.rewards) != 0:
            rewardFrame = Frame(self)
            rewardFrame.grid(row=self.rowHelper)
            Label(rewardFrame, text='Szerzett jutalmak: ', font=("Helvetica", 11)).grid(row=0, column=0, pady=(5,0))
            self.increaseRowHelper()

            for i in range(len(self.report.rewards)):
                Label(rewardFrame, text='- %s: +%s' % (self.report.rewards[i][0], self.report.rewards[i][1]), font=("Helvetica", 11)).grid(row=i, column=1)

        Label(self, text='Kihivások állása:', font=("Helvetica", 11)).grid(row=self.rowHelper, pady=(10,0))
        self.increaseRowHelper()

    def increaseRowHelper(self):
        self.rowHelper = self.rowHelper + 1
