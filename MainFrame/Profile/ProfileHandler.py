from tkinter import *
from tkinter import ttk

class ProfileFrame(Frame):

    def __init__(self, logObj, root, user):
        self.logObj = logObj
        self.logObj.simpleLog("Creating Profile Frame...")
        self.user = user

        Frame.__init__(self, master=root, bg='white')
        self.pack_propagate(0)
        self.pack(fill=BOTH, expand=1)

        self.profileFrame = Frame(self)
        self.challengeFrame = Frame(self)
        self.challengeFrame.pack_propagate(0)
        self.profileFrame.grid(row=0, column=0, sticky=W, pady=10, padx=10)
        self.challengeFrame.grid(row=0, column=1, sticky=E+N, padx=250)

        self.setupProfileFrame()

        self.setupChallengeFrame()

    def setupProfileFrame(self):
        self.usernameLabel = Label(self.profileFrame, text='%s' % self.user.username.capitalize(), anchor="w", font=("Helvetica", 44))
        ttk.Separator(self.profileFrame, orient=HORIZONTAL).grid(row=1, columnspan=5, sticky="ew")
        self.levelLabel = Label(self.profileFrame, text='%i. szint' % self.user.level, anchor="w", font=("Helvetica", 25))
        self.usernameLabel.grid(row=0, column=0, sticky=W)
        self.levelLabel.grid(row=2, column=0, rowspan=2, sticky=W)

        self.placeProgressBar()

        Label(self.profileFrame, text='Szavak: %i' % len(self.user.wordIDs), font=("Helvetica", 13)).grid(row=4, columnspan=2, sticky=W, pady=20)

        self.setupLanguageFrame()

        self.setupHelpFrame()

    def placeProgressBar(self):
        xp, threshold = self.user.calculateLevel()

        self.progressBarFrame = Frame(self.profileFrame)
        self.progressBarFrame.grid(row=2, column=1, rowspan=2, sticky=W)

        self.xpProgressBar = ttk.Progressbar(self.progressBarFrame, value=xp, maximum=threshold, length=200)
        self.xpProgressBar.grid(row=0, sticky=W)

        self.xpForLevelLabel = Label(self.progressBarFrame, text='%s/%s xp' % (xp, threshold), anchor="w", font=("Helvetica", 11))
        self.xpForLevelLabel.grid(row=1, sticky=W+E+S+N, padx=75)

    def setupLanguageFrame(self):
        self.languageFrame = Frame(self.profileFrame)
        self.languageFrame.grid(row=5, columnspan=5)

        Label(self.languageFrame, text='Nyelvek: ', font=("Helvetica", 11)).grid(row=0, column=0, sticky=W)
        for i in range(len(self.user.languages)):
            Label(self.languageFrame, text=self.user.languages[i].language.capitalize(), font=("Helvetica", 11)).grid(row=i+1, column=0, sticky=W, padx=40)
            level, xp, threshold = self.user.languages[i].getLevelXpThreshold(self.user.languages[i].progress)
            Label(self.languageFrame, text='%i. szint' % level, font=("Helvetica", 11)).grid(row=i+1, column=1)
            ttk.Progressbar(self.languageFrame, value=xp, maximum=threshold, length=200).grid(row=i+1, column=2, padx=10)
            Label(self.languageFrame, text='%s/%s xp' % (xp, threshold), font=("Helvetica", 11)).grid(row=i+1, column=3)

    def setupHelpFrame(self):
        helpFrame = Frame(self.profileFrame)
        helpFrame.grid(row=6, columnspan=5, sticky=W)

        Label(helpFrame, text='Segitségek: ', font=("Helvetica", 11)).grid(row=0, column=0, sticky=W, pady=(5,0))
        for i in range(len(self.user.helps)):
            Label(helpFrame, text="%s: " % self.user.helps[i].text, font=("Helvetica", 11)).grid(row=i+1, column=0, sticky=W, padx=40)
            Label(helpFrame, text=self.user.helps[i].amount, font=("Helvetica", 11)).grid(row=i+1, column=1, sticky=W, padx=1)

    def setupChallengeFrame(self):
        Label(self.challengeFrame, text='Kihivások', font=("Helvetica", 18)).grid(row=0, column=0, sticky=E+W)
        i = 1
        for challengeObj in self.user.challenges:
            self.createChallengeFrame(challengeObj, i)
            i = i + 1

    def createChallengeFrame(self, challengeObj, rowNum):
        challengeObjFrame = Frame(self.challengeFrame, bd=4, relief=GROOVE, width=700)
        challengeObjFrame.pack_propagate(0)
        challengeObjFrame.grid(row=rowNum, column=0, sticky=E)
        Label(challengeObjFrame, text=challengeObj.description).grid(row=0)
        ttk.Progressbar(challengeObjFrame, value=challengeObj.progress, maximum=challengeObj.amount, length=450).grid(row=1)
        Label(challengeObjFrame, text='%i/%i' % (challengeObj.progress, challengeObj.amount)).grid(row=2)
        reward = ""
        for help in self.user.helps:
            if help.type == challengeObj.reward:
                reward = help.text
        Label(challengeObjFrame, text='Jutalom: (%i) %s' % (challengeObj.rewardAmount, reward)).grid(row=3)
