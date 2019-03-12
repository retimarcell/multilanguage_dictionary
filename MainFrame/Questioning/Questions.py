import random
from MainFrame.Questioning import QuestionEligibilityTestings as QET

class Question:

    def __init__(self, wordID, sLang, aLang, sWord, aWord):
        self.wordID = wordID
        self.sourceLang = sLang
        self.answerLang = aLang
        self.label = sWord
        self.answer = aWord


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

            while len(randomWordIDs) != 0:
                selectedLanguage = QET.getRandomLanguage(logObj, options.languages, options.source, user.languages)
                answerWord, selectedWordID, removableIDs = QET.getRandomAnswerWord(logObj, randomWordIDs, user, selectedLanguage, options.categories)

                if answerWord == " - " and selectedWordID == -1:
                    removeWordIDs(logObj, None, removeWordIDs, randomWordIDs)
                    continue

                sourceWord, sourceLang, isSuccesful = QET.getSourceWord(logObj, user.languages, options.source, selectedWordID)

                removeWordIDs(logObj, None, removableIDs, randomWordIDs)

                if not isSuccesful:
                    removeWordIDs(logObj, selectedWordID, None, randomWordIDs)
                    continue

                logObj.simplelog("Creating question!")
                logObj.questionLog(selectedWordID, sourceLang, selectedLanguage, sourceWord, answerWord)
                questions.append(Question(selectedWordID, sourceLang, selectedLanguage, sourceWord, answerWord))


def removeWordIDs(logObj, singleID, arrayID, wordIDs):
    logObj.simplelog("Removing unwanted wordIDs from randomized array")
    logObj.arrayItemsLog("Previous word IDs: ", wordIDs)
    if singleID is None:
        logObj.simplelog("No single ID added")
    else:
        logObj.simplelog("Removing: %i" % singleID)
        wordIDs.remove(singleID)

    if arrayID is None:
        logObj.simplelog("No ID array added")
    else:
        for ID in arrayID:
            logObj.simplelog("Removing: %i" % ID)
            wordIDs.remove(ID)
    logObj.arrayItemsLog("Remaining word IDs: ", wordIDs)
