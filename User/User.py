from User import Language
from User import Category


class User:
    def __init__(self, logobj, user, database):
        self.logObj = logobj
        self.logObj.simpleLog("Initializing user: \"%s\"" % user)
        self.username = user
        self.database = database
        self.languages = []
        self.wordIDs = []
        self.categories = []
        self.lastAnswers = []

        self.fillLanguages()
        self.fillWordIDs()
        self.fillWords()
        self.fillCategories()

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
