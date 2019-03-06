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

    def getWordAndProgress(self, wordID):
        for i in range(len(self.wordIDs)):
            if self.wordIDs[i] == wordID:
                return [self.words[i], self.progresses[i]]
        return [" - ", -1]

    def changeWord(self, previous, new):
        index = self.words.index(previous)
        self.progresses[index] = 0
        self.words[index] = new

    def removeWordID(self, wordID):
        index = self.wordIDs.index(wordID)

        self.wordIDs.pop(index)
        self.words.pop(index)
        self.progresses.pop(index)
