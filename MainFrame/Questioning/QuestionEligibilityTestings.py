import random


def getRandomizedWordIDs(logObj, array):
    logObj.simplelog("Creating randomized WordID array")
    returnArray = array.copy()
    random.shuffle(returnArray)
    return returnArray


def isWordIDsEmpty(wordIDs):
    if len(wordIDs) == 0:
        return True
    return False


def getRandomLanguage(logObj, languages, sourceLang, userLanguages):
    logObj.simplelog("Getting random language which is not the source language. [%s]" % sourceLang)
    selectedLang = ""
    searchedLanguageArray = []

    if len(languages) == 0:
        for lang in userLanguages:
            searchedLanguageArray.append(lang.language)
    else:
        searchedLanguageArray = languages

    while True:
        selectedLang = random.choice(searchedLanguageArray)

        logObj.simplelog("Dummychecking if source language is in selected languages...")
        if selectedLang != sourceLang:
            logObj.simplelog("Selected language: %s" % selectedLang)
            return selectedLang

        logObj.simplelog("Dummy check failed!")


def getRandomAnswerWord(logObj, wordIDs, user, selectedLanguage, eligibleCategories):
    logObj.simplelog("Getting random word")

    copyWordIDs = wordIDs.copy()
    filterCounter = 1
    removableIDs = []

    while len(copyWordIDs) != 0:
        selectedWordID = random.choice(copyWordIDs)

        wordAndProgress = getWordAndProgressFromLanguage(logObj, user, selectedLanguage, selectedWordID)
        if wordAndProgress[0] == "Failed" and str(wordAndProgress[1]) == "":
            logObj.simplelog("Failed with the wordID: %i" % selectedWordID)
            copyWordIDs.remove(selectedWordID)
            removableIDs.remove(selectedWordID)
            continue
        else:
            logObj.simplelog("Gotten the following word and progress: [%s | %i]" % (wordAndProgress[0], wordAndProgress[1]))

        isPassed = progressFilter(logObj, wordAndProgress[1], filterCounter)
        if isPassed:
            logObj.simplelog("Progress filter check passed.")
        else:
            logObj.simplelog("Progress filter failed! Try: %i" % filterCounter)
            filterCounter += 1
            continue

        isWordIDInCategory = wordIDInCategoryCheck(logObj, user.categories, eligibleCategories, selectedWordID)
        if isWordIDInCategory:
            logObj.simplelog("Category check passed.")
        else:
            logObj.simplelog("Category check failed.")
            copyWordIDs.remove(selectedWordID)
            removableIDs.append(selectedWordID)
            continue

        return [wordAndProgress[0], selectedWordID, removableIDs]

    return [" - ", -1, removableIDs]


def getWordAndProgressFromLanguage(logObj, user, lang, wordID):
    for ele in user.languages:
        if ele.language == lang:
            wordAndProgress = ele.getWordAndProgress(wordID)
            if wordAndProgress[0] is None or wordAndProgress[0] == "" or wordAndProgress[0] == " - ":
                return ["Failed"]
            return wordAndProgress
    return ["Failed"]


def progressFilter(logObj, progress, counter):
    randInt = random.randint(1, 10)
    logObj.simplelog("Progress filtering in progress with random number and progress: %i | %i" % (randInt, progress))

    if (randInt <= 5 and progress <= 20) or (5 < randInt <= 8 and 20 < progress <= 40) or (8 < randInt and 40 < progress):
        return True
    elif counter == 6:
        logObj.simplelog("Passing because of counter")
        return True
    return False


def wordIDInCategoryCheck(logObj, userCategories, eligibleCategories, wordID):
    logObj.simplelog("Checking if wordID in selected categories")

    if len(eligibleCategories) == 0:
        logObj.simplelog("Eligible Category list is empty, returning True")
        return True

    for category in userCategories:
        if category.category in eligibleCategories:
            if category.getWordIDIndex(wordID) != None:
                return True
    return False


def getSourceWord(logObj, languages, sourceLang, wordID):
    logObj.simplelog("Getting the source word.")

    if sourceLang == " - ":
        while True:
            randomLang = random.choice(languages)
            arrTemp = createReturnArrayForSourceWord(logObj, randomLang, wordID)
            return arrTemp

    for lang in languages:
        if lang.language == sourceLang:
            arrTemp = createReturnArrayForSourceWord(logObj, lang, wordID)

    return [" - ", None, False]

def createReturnArrayForSourceWord(logObj, languageObj, wordID):
    logObj.simplelog("Creating returnable array for source word")

    returnArray = []

    returnWord = languageObj.getWord(wordID)
    returnArray.append(returnWord)
    returnArray.append(languageObj.language)

    if returnWord == " - " or returnWord is None:
        logObj.simplelog("No word is found in source word")
        returnArray.append(False)
    else:
        logObj.simplelog("Found word: %s" % returnWord)
        returnArray.append(True)

    return returnArray
