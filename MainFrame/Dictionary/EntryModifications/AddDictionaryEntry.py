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
        self.root.geometry("420x80")
        self.root.resizable(width=FALSE, height=FALSE)

        self.frame = Frame(self.root)
        self.frame.pack()
        self.topFrame = Frame(self.frame)
        self.bottomFrame = Frame(self.frame)
        self.topFrame.grid(row=0, sticky=E+W, pady=(10,0))
        self.bottomFrame.grid(row=1, sticky=E)

        self.label = Label(self.topFrame, text="%s:" % self.user.languages[0].language.capitalize(), font=("Helvetica", 15))
        self.entry = Entry(self.topFrame, width=30, borderwidth=2, fg='#000000', relief=GROOVE, font=("Helvetica", 13))
        self.forwardButton = Button(self.bottomFrame, text="Következő", command=self.play, font=("Helvetica", 11), relief=GROOVE)
        self.cancelButton = Button(self.bottomFrame, text="Mégse", command=self.cancelAddition, font=("Helvetica", 11), relief=GROOVE)

        self.label.grid(row=0, column=0, padx=(0,5))
        self.entry.grid(row=0, column=1)
        self.cancelButton.grid(row=0, column=1, sticky=E, padx=10)
        self.forwardButton.grid(row=0, column=0, sticky=E)

        self.logObj.simpleLog("Waiting for word addition for language: %s" % self.user.languages[0].language)

        self.root.focus_force()
        self.entry.focus()
        self.root.bind('<Return>', self.play)

        self.root.mainloop()

    def play(self, event=None):
        temp = self.entry.get()
        self.addedWords.append(temp)
        self.logObj.simpleLog("Added \"%s\" for %s" % (temp, self.user.languages[self.counter].language))

        if (self.counter + 1) != len(self.user.languages):
            self.counter += 1
            self.logObj.simpleLog("Waiting for word addition for language: %s" % self.user.languages[self.counter].language)
            self.label['text'] = "%s:" % self.user.languages[self.counter].language
            self.entry.delete(0, END)
            if (self.counter+1) == len(self.user.languages):
                self.forwardButton.config(text="Befejezés")
        else:
            self.logObj.simpleLog("Words gathered.")
            self.pushNewWordsToDatabase()
            self.saveForUser()
            self.user.database.setNextWordID()

            self.logObj.simpleLog("Word addition finished.")
            showinfo("Siker!", "Sikeresen hozzáadva!")

            self.root.destroy()

    def pushNewWordsToDatabase(self):
        self.logObj.simpleLog("Adding words to database...")

        self.user.database.insertIntoTable("WordID", [self.user.username, self.user.database.nextWordID])

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

    def saveForUser(self):
        self.user.wordIDs.append(self.user.database.nextWordID)
        for i in range(len(self.user.languages)):
            self.user.languages[i].addWord(self.user.database.nextWordID, self.addedWords[i])

    def cancelAddition(self):
        if askyesno("Megszakítás", "Biztosan megszakítja a hozzáadást?"):
            self.logObj.simpleLog("Word addition cancelled.")
            self.root.destroy()
        else:
            self.root.focus_force()
            self.logObj.simpleLog("Word addition cancel cancelled.")
