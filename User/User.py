from User import Language, Category, Help, Challenge, ReportUpdates
import random


class User:

    def __init__(self, logobj, user, database, isFirstTime):
        self.logObj = logobj
        self.logObj.simpleLog("Initializing user: \"%s\"" % user)
        self.username = user
        self.database = database
        self.xp = self.database.simpleSelectFromTable("Users", ["username"], [self.username])[0][3]
        self.level = 0
        self.isFirstTime = isFirstTime
        self.languages = []
        self.wordIDs = []
        self.categories = []
        self.helps = []
        self.challenges = []

        self.lastAnswers = []

        self.calculateLevel()
        self.fillLanguages()
        self.fillWordIDs()
        self.fillWords()
        self.fillCategories()
        self.fillHelps()
        self.fillChallenges(isFirstTime)

        for language in self.languages:
            language.calculateProgress()

    def calculateLevel(self):
        threshold = 30
        xp = self.xp
        self.level = 1
        while (xp-threshold) >= 0:
            self.level = self.level + 1
            xp = xp-threshold
            threshold = threshold + 10
        return [xp, threshold]

    def fillLanguages(self):
        self.logObj.simpleLog("Filling languages...")
        arr = self.database.simpleSelectFromTable("Languages", ["user"], [self.username])
        for ele in arr:
            self.languages.append(Language.Language(ele[0], ele[2]))

    def fillWordIDs(self):
        self.logObj.simpleLog("Filling word ID array...")
        arr = self.database.simpleSelectFromTable("WordID", ["username"], [self.username])
        for ele in arr:
            self.wordIDs.append(ele[1])

    def fillWords(self):
        self.logObj.simpleLog("Filling words into languages...")
        for lang in self.languages:
            self.logObj.simpleLog("Filling %s" % lang.language)
            selectResult = self.database.simpleSelectFromTable("l_" + lang.language)
            for id in self.wordIDs:
                for element in selectResult:
                    if id == element[0]:
                        lang.wordIDs.append(element[0])
                        lang.words.append(element[1])
                        lang.progresses.append(element[2])

    def fillCategories(self):
        self.logObj.simpleLog("Filling categories...")
        selectResult = self.database.simpleSelectFromTable("Categories", ["user"], [self.username])

        for categoryElement in selectResult:
            index = self.getCategoryIndex(categoryElement[0])

            if index is None:
                temp = Category.Category(categoryElement[0])
                temp.wordIDs.append(categoryElement[2])
                self.categories.append(temp)
            else:
                self.categories[index].wordIDs.append(categoryElement[2])

        for cat in self.categories:
            try:
                cat.wordIDs.remove(-1)
            except:
                pass

    def getCategoryIndex(self, category):
        for i in range(len(self.categories)):
            if self.categories[i].category == category:
                return i
        return None

    def fillHelps(self):
        self.logObj.simpleLog("Creating help objects...")

        helpsArr = [["Egész szó", "FullWord"], ["Kezdőbetű", "StartLetter"], ["Hibaellenőrzés", "Check"]]

        for h in helpsArr:
            self.helps.append(Help.Help(h[0], h[1]))

        self.fillHelpAmounts()

    def fillHelpAmounts(self):
        self.logObj.simpleLog("Filling up helps")

        selectResult = self.database.simpleSelectFromTable("Helps", ["username"], [self.username])

        for helpElement in selectResult:
            index = self.getHelpIndex(helpElement[0])

            self.helps[index].amount = int(helpElement[1])

    def getHelpIndex(self, type):
        for i in range(len(self.helps)):
            if self.helps[i].type == type:
                return i

    def fillChallenges(self, isFirstTime):
        result = self.database.simpleSelectFromTable("Challenge_Ongoings", ["username"], [self.username])

        for e in result:
            self.challenges.append(Challenge.Challenge(e[0], e[1], e[2], int(e[3]), e[4], int(e[5]), int(e[6])))

        if isFirstTime and len(self.challenges) != 3:
            result = self.database.simpleSelectFromTable("Challenge_Templates")
            templates = result.copy()
            random.shuffle(templates)

            while len(self.challenges) != 3:
                if not (len(self.languages) == 0 and (templates[0][1] == 'Y' or templates[0][2] == 'Y')):
                    self.challenges.append(Challenge.Challenge(templates[0][0],
                                                               templates[0][1],
                                                               templates[0][2],
                                                               int(templates[0][3]),
                                                               templates[0][4],
                                                               int(templates[0][5]),
                                                               0))
                    if self.challenges[-1].sourceLanguage == "Y":
                        i = random.randint(0, len(self.languages)-1)
                        self.challenges[-1].sourceLanguage = self.languages[i].language
                    if self.challenges[-1].destinationLanguage == "Y":
                        i = random.randint(0, len(self.languages)-1)
                        self.challenges[-1].destinationLanguage = self.languages[i].language

                    self.database.insertIntoTable("Challenge_Ongoings", [self.challenges[-1].description,
                                                                         self.challenges[-1].sourceLanguage,
                                                                         self.challenges[-1].destinationLanguage,
                                                                         self.challenges[-1].amount,
                                                                         self.challenges[-1].reward,
                                                                         self.challenges[-1].rewardAmount,
                                                                         self.challenges[-1].progress,
                                                                         self.username])
                templates.pop(0)

    def saveProgress(self):
        self.logObj.simpleLog("Starting progress saving")
        report = ReportUpdates.ReportUpdates(self.xp)

        for answer in self.lastAnswers:
            self.logObj.simpleLog("Answer processing: %i" % answer.wordID)
            for lang in self.languages:
                if lang.language == answer.answerLang:
                    if lang.updateWordProgress(answer.wordID, answer.progress):
                        self.database.updateProgress(lang.language, answer.wordID, lang.getProgressByWordID(answer.wordID))

            for challenge in self.challenges:
                if challenge.noLanguageRestriction or challenge.sourceLanguage == answer.sourceLang or challenge.destinationLanguage == answer.answerLang:
                    challenge.progress = challenge.progress + 1

            if answer.progress == 1:
                self.xp = self.xp + 5

        self.updateLevel(report)
        self.calculateChallenges()
        self.calculateProgresses(report)

        return report

    def updateLevel(self, report):
        self.logObj.simpleLog("Updating user level")
        self.database.updateXp(self.username, self.xp)
        report.calculateFinishXp(self.xp)

        prevLevel = self.level
        self.calculateLevel()
        while self.level > prevLevel:
            self.addLevelUpReward(report)
            report.amountOfLevelUps = report.amountOfLevelUps + 1
            prevLevel = prevLevel + 1

    def calculateChallenges(self):
        self.logObj.simpleLog("Calculating Challenges")
        for challenge in self.challenges:
            if challenge.progress >= challenge.amount:
                help, amount = challenge.getHelpAndAmount()
                index = self.getHelpIndex(help)
                self.helps[index].amount = self.helps[index].amount + amount
                self.database.updateHelp(self.helps[index].amount, self.helps[index].type, self.username)

                challenge.isDone = True
                self.database.deleteRow("Challenge_Ongoings",
                                        ["sourceLang", "destinationLang", "amount", "reward", "rewardAmount", "username"],
                                        [challenge.sourceLanguage, challenge.destinationLanguage, challenge.amount, challenge.reward, challenge.rewardAmount, self.username])
            else:
                self.database.updateChallenge(challenge.sourceLanguage, challenge.destinationLanguage, challenge.amount, challenge.reward, challenge.rewardAmount, self.username, challenge.progress)

    def calculateProgresses(self, report):
        self.logObj.simpleLog("Calculating language progresses")
        c = 0
        for lang in self.languages:
            helpsGained = lang.calculateProgress()
            c += helpsGained
            if helpsGained != 0:
                report.languageLevelUps.append([lang.language.capitalize(), lang.getLevelXpThreshold(lang.progress)[0]])

            self.database.updateLanguageXp(lang.language, self.username, lang.progress)

        for i in range(c):
            self.addLevelUpReward(report)

    def addLevelUpReward(self, report):
        help = random.choice(self.helps)
        plusAmount = random.randint(1, 5)
        report.rewards.append([help.text, plusAmount])
        help.amount = help.amount + plusAmount
        self.database.updateHelp(help.amount, help.type, self.username)
