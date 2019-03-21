from User import Language, Category, Help, Challenge
from random import shuffle


class User:
    def __init__(self, logobj, user, database, isFirstTime):
        self.logObj = logobj
        self.logObj.simpleLog("Initializing user: \"%s\"" % user)
        self.username = user
        self.database = database
        self.languages = []
        self.wordIDs = []
        self.categories = []
        self.helps = []
        self.challenges = []

        self.lastAnswers = []

        self.fillLanguages()
        self.fillWordIDs()
        self.fillWords()
        self.fillCategories()
        self.fillHelps()
        self.fillChallenges(isFirstTime)

    def fillLanguages(self):
        self.logObj.simpleLog("Filling languages...")
        arr = self.database.simpleSelectFromTable("Languages", ["user"], [self.username])
        for ele in arr:
            self.languages.append(Language.Language(ele[0]))

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

    def getCategoryIndex(self, category):
        for i in range(len(self.categories)):
            if self.categories[i].category == category:
                return i
        return None

    def fillHelps(self):
        self.logObj.simpleLog("Creating help objects...")

        helpsArr = [["Egész szó", "FullWord"], ["Kezdőbetű", "StartLetter"], ["Szó kihagyása", "Skip"]]

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
            self.challenges.append(Challenge.Challenge(e[0], e[1], e[2], int(e[3]), e[4], int(e[5])))

        if isFirstTime and len(self.challenges) != 3:
            result = self.database.simpleSelectFromTable("Challenge_Templates")
            templates = shuffle(result.copy())

            while len(self.challenges) != 3:
                if not (len(self.languages) == 0 and (templates[0][1] == 'Y' or templates[0][2] == 'Y')):
                    self.challenges.append(Challenge.Challenge(templates[0][0], templates[0][1], templates[0][2], int(templates[0][3]), templates[0][4], int(templates[0][5])))

                templates.pop(0)

    def saveProgress(self):
        for answer in self.lastAnswers:
            for lang in self.languages:
                if lang.language == answer.answerLang:
                    if lang.updateWordProgress(answer.wordID, answer.progress):
                        self.database.updateProgress(lang.language, answer.wordID, lang.getProgressByWordID(answer.wordID))
        self.calculateProgresses()

    def calculateProgresses(self):
        # TODO
        pass
