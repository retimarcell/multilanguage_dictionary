class Category:

    def __init__(self, category):
        self.category = category
        self.progress = 0
        self.wordIDs = []

    def getCategory(self, wordID):
        if wordID in self.wordIDs:
            return self.category
        return None

    def removeWordID(self, wordID):
        self.wordIDs.remove(wordID)
