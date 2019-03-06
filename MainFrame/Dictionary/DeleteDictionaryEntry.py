from tkinter.messagebox import *


def deleteWholeEntry(logObj, user, tableRow):
    if confirmDelete(logObj):
        wordID = tableRow.wordID

        deleteFromUser(logObj, user, wordID)


def deleteFromUser(logObj, user, wordID):
    logObj.simpleLog("Deleting wordID...")
    user.wordIDs.remove(wordID)
    user.database.deleteRow("WordID", ["username", "wordID"], [user.username, wordID])

    for language in user.languages:
        deleteFromLanguage(logObj, user, language, wordID)

    for category in user.categories:
        deleteFromCategory(logObj, user, category, wordID)


def deleteFromLanguage(logObj, user, language, wordID):
    logObj.simpleLog("Deleting word from language: %s" % language.language)
    language.removeWordID(wordID)
    user.database.deleteRow("l_" % language.language, ["wordID"], [wordID])


def deleteFromCategory(logObj, user, category, wordID):
    logObj.simpleLog("Deleting word from category: %s" % category.category)
    category.removeWordID(wordID)
    user.database.deleteRow("Categories", ["wordID"], [wordID])


def confirmDelete(logObj):
    logObj.simpleLog("Entry delete started...")
    if askyesno("Törlés", "Biztos törölni akarod?"):
        logObj.simpleLog("Entry delete confirmed.")
        return True
    logObj.simpleLog("Entry delete cancelled.")
    return False
