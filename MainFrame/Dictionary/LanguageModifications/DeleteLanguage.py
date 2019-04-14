from tkinter.messagebox import *


def deleteLanguage(logObj, user, language):
    if confirmDelete(logObj, language):
        for i in range(len(user.languages)):
            if user.languages[i].language.upper() == language:
                deleteFromDatabase(logObj, user, user.languages[i])
                user.languages.pop(i)


def deleteFromDatabase(logObj, user, language):
    logObj.simpleLog("Deleting [%s] from Languages database..." % language.language)
    user.database.deleteRow("Languages", ["language", "user"], [language.language, user.username])

    logObj.simpleLog("Dropping language table...")
    user.database.dropTable("l_%s" % language.language)


def confirmDelete(logObj, language):
    logObj.simpleLog("Language delete started...")
    if askyesno("Törlés", "Biztos törölni akarod az egész nyelvet?"):
        logObj.simpleLog("Language delete confirmed.")
        return True
    logObj.simpleLog("Language delete cancelled.")
    return False
