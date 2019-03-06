import random

class Questions:

    def __init__(self):
        self.wordIDs = []
        self.labelWords = []
        self.answers = []


def getQuestions(user, amount, options):
    questions = []
    randomWordIDs = getRandomizedWordIDs(user.wordIDs)
    fillQuestions(questions, randomWordIDs, amount, options, user)
    return questions


def getRandomizedWordIDs(array):
    returnArray = array.copy()
    random.shuffle(returnArray)
    return returnArray


def fillQuestions(questions, wordIDs, amount, options, user):
    for wordID in wordIDs:
        pass


def isCorrespondingOptions(wordID, options, user):
    pass
