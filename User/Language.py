class Language:

    def __init__(self, lang):
        self.language = lang
        self.progress = 0
        self.words = []
        self.progresses = []
        self.wordIDs = []

        self.calculateProgress()

    def calculateProgress(self):
        self.progress = 0
        for prog in self.progresses:
            self.progress += prog

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

        if (self.progresses[index] != 0 or amount != -1) and (self.progresses[index] != 60 or amount != 1):
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
