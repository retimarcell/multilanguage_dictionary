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
        self.root.title("Szó hozzáadás")

        self.frame = Frame(self.root, bg='white')
        self.frame.pack()
        self.topFrame = Frame(self.frame, bg='white')
        self.bottomFrame = Frame(self.frame, bg='white')
        self.topFrame.grid(row=0, sticky=E+W, pady=(10,0))
        self.bottomFrame.grid(row=1, sticky=E)
        self.additionFrames = []

        for i in range(len(self.user.languages)):
            self.additionFrames.append(AdditionFrame(self.topFrame, self.user.languages[i].language, i))

        self.forwardButton = Button(self.bottomFrame, text="Hozzáadás", command=self.play, font=("Helvetica", 11), bg='white', activebackground='white')
        self.cancelButton = Button(self.bottomFrame, text="Mégse", command=self.cancelAddition, font=("Helvetica", 11), bg='white', activebackground='white')

        self.cancelButton.grid(row=0, column=1, sticky=E, padx=10)
        self.forwardButton.grid(row=0, column=0, sticky=E)

        self.logObj.simpleLog("Waiting for word addition for language: %s" % self.user.languages[0].language)

        ws = self.root.winfo_screenwidth() / 2 - 200
        hs = self.root.winfo_screenheight() / 2 - 300
        self.root.geometry('+%d+%d' % (ws, hs))
        self.root.resizable(width=FALSE, height=FALSE)
        self.root.configure(bg='white')

        self.additionFrames[0].entry.focus_force()
        self.root.bind('<Return>', self.play)

        self.root.mainloop()

    def play(self, event=None):
        entries = []
        isAllNone = True
        for frame in self.additionFrames:
            t = frame.entry.get()
            if t != "":
                isAllNone = False
                entries.append(t)

        if isAllNone:
            showerror("Hiba!", "Legalább egy szónak adjon meg egy bemenetet!")
        else:
            for entry in entries:
                self.logObj.simpleLog("Added word: %s")
                self.addedWords.append(entry)

            self.logObj.simpleLog("Words gathered.")
            self.pushNewWordsToDatabase()
            self.saveForUser()
            self.user.database.setNextWordID()

            self.logObj.simpleLog("Word addition finished.")
            showinfo("Siker!", "Sikeresen hozzáadva!")
            self.root.quit()
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
        values.append(self.user.database.nextWordID)
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


class AdditionFrame(Frame):

    def __init__(self, root, label, rowN):
        Frame.__init__(self, master=root, bg='white')
        self.grid(row=rowN, sticky=E)

        self.label = Label(self, text="%s:" % label.capitalize(), font=("Helvetica", 15), bg='white')
        self.entry = Entry(self, width=30, borderwidth=2, fg='#000000', relief=GROOVE, font=("Helvetica", 13), bg='white')
        self.label.grid(row=0, column=0, padx=(4,10), sticky=E)
        self.entry.grid(row=0, column=1, padx=(0,4), sticky=E)
