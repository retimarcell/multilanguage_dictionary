import random
from MainFrame.Questioning import QuestionEligibilityTestings as QET

class Question:

    def __init__(self):
        self.wordID = ""
        self.label = ""
        self.answers = []


def getQuestions(logObj, user, amount, options):
    questions = []
    randomWordIDs = QET.getRandomizedWordIDs(logObj, user.wordIDs)
    fillQuestions(logObj, questions, randomWordIDs, amount, options, user)
    return questions


def fillQuestions(logObj, questions, randomWordIDs, amount, options, user):
    logObj.simplelog("Starting Question creation.")
    for i in range(amount):
        if QET.isWordIDsEmpty(randomWordIDs):
            logObj.simplelog("Questions couldn't be filled by the required amount, since there is no more available WordID.")
            break
        else:
            optionsFailed = False

            while True:
                selectedLanguage = QET.getRandomLanguage(logObj, options.languages, options.source, user.languages)
                answerWord, selectedWordID, removableIDs = QET.getRandomAnswerWord(logObj, randomWordIDs, user, selectedLanguage, options.categories)
                # sourceWord = QET.getSourceWord(logObj, user.languages, options.source, )
