class Language:

    def __init__(self, lang, xp):
        self.language = lang
        self.progress = xp
        self.words = []
        self.progresses = []
        self.wordIDs = []
        self.temporaryWordProgressGains = 0

        self.calculateProgress()

    def calculateProgress(self):
        gains = self.temporaryWordProgressGains * 5
        helpsGained = 0

        if gains > 0:
            newProgress = self.progress + gains
            oldLevel = self.getLevelXpThreshold(self.progress)[0]
            newLevel = self.getLevelXpThreshold(newProgress)[0]

            while newLevel > oldLevel:
                helpsGained = helpsGained + 1
                oldLevel = oldLevel + 1

            self.progress = newProgress

        self.temporaryWordProgressGains = 0

        return helpsGained

    def getLevelXpThreshold(self, progress):
        threshold = 30
        xp = progress
        level = 1
        while (xp - threshold) > 0:
            xp = xp - threshold
            threshold = threshold + 10
            level = level + 1
        return [level, xp, threshold]

    def getLanguageAndWord(self, wordID):
        for i in range(len(self.wordIDs)):
            if self.wordIDs[i] == wordID:
                return [self.language, self.words[i]]
        return None

    def getWord(self, wordID):
        for i in range(len(self.wordIDs)):
            if self.wordIDs[i] == wordID:
                return self.words[i]
        return [" - "]

    def getWordAndProgress(self, wordID):
        for i in range(len(self.wordIDs)):
            if self.wordIDs[i] == wordID:
                return [self.words[i], self.progresses[i]]
        return [" - ", -1]

    def changeWord(self, new, wordID):
        index = self.wordIDs.index(wordID)
        self.progresses[index] = 0
        self.words[index] = new

    def removeWordID(self, wordID):
        index = self.wordIDs.index(wordID)

        self.wordIDs.pop(index)
        self.words.pop(index)
        self.progresses.pop(index)

    def containsWordID(self, wordID):
        if wordID in self.wordIDs:
            return True
        return False

    def updateWordProgress(self, wordID, amount):
        index = self.wordIDs.index(wordID)

        if amount == 1:
            self.temporaryWordProgressGains = self.temporaryWordProgressGains + 1

        if (self.progresses[index] != 0 or amount != -1) and (self.progresses[index] != 30 or amount != 1):
            self.progresses[index] = self.progresses[index] + amount
            return True
        return False

    def getProgressByWordID(self, wordID):
        index = self.wordIDs.index(wordID)
        return self.progresses[index]

    def addWord(self, wordID, word):
        self.wordIDs.append(wordID)
        self.words.append(word)
        self.progresses.append(0)
