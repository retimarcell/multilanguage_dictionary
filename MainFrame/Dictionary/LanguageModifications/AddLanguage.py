from tkinter import *
from tkinter.messagebox import *
from User import Language


class AddLanguage:

    def __init__(self, logObj, user):
        self.logObj = logObj
        self.logObj.simpleLog("Creating language addition window")
        self.user = user

        self.root = Tk()
        self.root.title("Új nyelv")
        self.root.configure(bg='white')
        ws = self.root.winfo_screenwidth() / 2 - 100
        hs = self.root.winfo_screenheight() / 2 - 300
        self.root.geometry('+%d+%d' % (ws, hs))
        self.root.resizable(width=FALSE, height=FALSE)

        self.label = Label(self.root, text='Az új nyelv:', font=("Helvetica", 13), bg='white')
        self.entry = Entry(self.root, width=25, borderwidth=2, fg='#000000', relief=GROOVE, font=("Helvetica", 13), bg='white')
        self.botFrame = Frame(self.root)
        self.confirmButton = Button(self.botFrame, text="Hozzáadás", font=("Helvetica", 11), command=self.confirm, bg='white', activebackground='white')
        self.cancelButton = Button(self.botFrame, text="Mégse", font=("Helvetica", 11), command=self.cancel, bg='white', activebackground='white')

        self.label.grid(row=0, sticky=E+W, pady=(5,0))
        self.entry.grid(row=1, sticky=E+W, pady=(2,2), padx=(2,2))
        self.botFrame.grid(row=2, sticky=E)
        self.cancelButton.grid(row=0, column=1, sticky=E, padx=10)
        self.confirmButton.grid(row=0, column=0, sticky=E)

        self.entry.focus_force()
        self.root.bind('<Return>', self.confirm)
        self.root.mainloop()

    def confirm(self, event=None):
        newLang = self.entry.get()

        newLang = removeSpecialChars(newLang)

        if newLang == "":
            self.logObj.simpleLog("No language added, resuming")
            showerror("Hiba", "Üres szó van megadva!")
            self.entry.delete(0, END)
        elif self.languageExists(newLang):
            self.logObj.simpleLog("Language already exists")
            showerror("Hiba", "Nyelv már létezik!")
            self.entry.delete(0, END)
        else:
            self.addToUser(newLang)
            self.saveInDatabase(newLang)
            self.root.quit()
            self.root.destroy()

    def languageExists(self, newLang):
        for lang in self.user.languages:
            if lang.language == newLang:
                return True
        return False

    def addToUser(self, newLang):
        self.logObj.simpleLog("Adding language to user: %s" % newLang)

        langObj = Language.Language(newLang, 0)
        for wordID in self.user.wordIDs:
            langObj.wordIDs.append(wordID)
            langObj.words.append("")
            langObj.progresses.append(0)
        self.user.languages.append(langObj)

    def saveInDatabase(self, nL):
        self.logObj.simpleLog("Adding language to database: %s" % nL)

        newLang = "l_%s" % nL

        self.user.database.insertIntoTable("Languages", [newLang[2:], self.user.username, 0])

        if not self.databaseExists(newLang):
            self.logObj.simpleLog("Creating new language database: %s" % newLang)

            values = ["wordID", "word", "progress"]
            types = ["INT", "VARCHAR(120)", "INT"]

            self.user.database.createTable("%s" % newLang, values, types)

        for wordID in self.user.wordIDs:
            self.user.database.insertIntoTable(newLang, [wordID, "", 0])

    def databaseExists(self, newLang):
        if self.user.database.getCount("%s" % newLang, "*") == 0:
            self.logObj.simpleLog("Database does not exist: %s" % newLang)
            return False
        self.logObj.simpleLog("Database exists: %s" % newLang)
        return True

    def cancel(self):
        result = askyesno("Megszakítás", "Biztosan megszakítja a hozzáadást?")
        if result:
            self.logObj.simpleLog("Language addition cancelled.")
            self.root.destroy()
        else:
            self.root.focus_force()
            self.logObj.simpleLog("Language addition cancel cancelled.")


def removeSpecialChars(word):
    reWord = ""

    for letter in word:
        if letter == 'á':
            reWord += "a"
        elif letter == 'é':
            reWord += "e"
        elif letter == "ő" or letter == "ó" or letter == "ö":
            reWord += "o"
        elif letter == "ü" or letter == "ú" or letter == "ű":
            reWord += "u"
        else:
            reWord += letter

    return reWord
