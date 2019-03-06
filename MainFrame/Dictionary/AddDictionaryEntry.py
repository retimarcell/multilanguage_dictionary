from tkinter import *


def addNewWord(logObj, user):
    logObj.simpleLog("Generating word addition window...")
    temp = IntVar()
    addedWords = []

    root = Tk()

    label = Label(root)
    entry = Entry(root, width=20)
    button = Button(root, text="OK", command=lambda temp=temp: confirmEntry(temp))

    label.grid(row=0, sticky=W)
    entry.grid(row=1)
    button.grid(row=2, sticky=E)

    root.mainloop()

    for language in user.languages:
        logObj.simpleLog("Waiting for word addition for language: %s" % language.language)
        temp.set(0)
        label.configure(text="%s:" % language.language)
        while temp != 1:
            pass
        addedWords.append(entry.get())
        logObj.simpleLog("Added \"%s\" for %s" % (addedWords[-1], language.language))

    root.destroy()
    pushNewWordsToDatabase(logObj, user, addedWords)


def pushNewWordsToDatabase(logObj, user, addedWords):
    logObj.simpleLog("Adding words to database...")

    user.database.insertIntoTable("WordID", [user.username, len(user.wordIDs) + 1])

    for i in range(len(addedWords)):
        createValuesForInsertAndSend(logObj, user, addedWords[i], i)


def createValuesForInsertAndSend(logObj, user, newWord, index):
    tableName = "l_" + user.languages[index].language
    logObj.simpleLog("Adding \"%s\" to \"%s\" database..." % (newWord, tableName))
    values = []
    values.append(len(user.wordIDs) + 1)
    values.append(newWord)
    values.append(0)

    user.database.insertIntoTable(tableName, values)


def confirmEntry(x):
    x.set(1)
