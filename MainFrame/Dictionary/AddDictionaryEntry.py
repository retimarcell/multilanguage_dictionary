from tkinter import *
from tkinter.messagebox import *


class AddEntry:

    def __init__(self, logObj, user):
        self.logObj = logObj
        self.logObj.simpleLog("Generating word addition window...")

        self.user = user
        self.addedWords = []
        self.counter = 0

        self.root = Tk()

        self.label = Label(self.root, text="%s:" % self.user.languages[0].language)
        self.entry = Entry(self.root, width=20)
        self.forwardButton = Button(self.root, text="OK", command=self.play)
        self.cancelButton = Button(self.root, text="Mégse", command=self.cancelAddition)

        self.label.grid(row=0, sticky=W, columnspan=2)
        self.entry.grid(row=1, columnspan=2)
        self.cancelButton.grid(row=2, column=1, sticky=E)
        self.forwardButton.grid(row=2, column=0, sticky=E)

        self.logObj.simpleLog("Waiting for word addition for language: %s" % self.user.languages[0].language)

        self.root.mainloop()

    def play(self):
        temp = self.entry.get()
        self.addedWords.append(temp)
        self.logObj.simpleLog("Added \"%s\" for %s" % (temp, self.user.languages[self.counter].language))

        if (self.counter + 1) != len(self.user.languages):
            self.counter += 1
            self.logObj.simpleLog("Waiting for word addition for language: %s" % self.user.languages[self.counter].language)
            self.label['text'] = "%s:" % self.user.languages[self.counter].language
            self.entry.delete(0, END)
        else:
            self.logObj.simpleLog("Words gathered.")
            self.pushNewWordsToDatabase()

            self.logObj.simpleLog("Word addition finished.")
            showinfo("Siker!", "Sikeresen hozzáadva!")

            self.root.destroy()

    def pushNewWordsToDatabase(self):
        self.logObj.simpleLog("Adding words to database...")

        self.user.database.insertIntoTable("WordID", [self.user.username, len(self.user.wordIDs) + 1])

        for i in range(len(self.addedWords)):
            self.createValuesForInsertAndSend(self.addedWords[i], i)

    def createValuesForInsertAndSend(self, newWord, index):
        tableName = "l_" + self.user.languages[index].language
        self.logObj.simpleLog("Adding \"%s\" to \"%s\" database..." % (newWord, tableName))
        values = []
        values.append(len(self.user.wordIDs) + 1)
        values.append(newWord)
        values.append(0)

        self.user.database.insertIntoTable(tableName, values)

    def cancelAddition(self):
        if askyesno("Megszakítás", "Biztosan megszakítja a hozzáadást?"):
            self.logObj.simpleLog("Word addition cancelled.")
            self.root.destroy()
        self.logObj.simpleLog("Word addition cancel cancelled.")
