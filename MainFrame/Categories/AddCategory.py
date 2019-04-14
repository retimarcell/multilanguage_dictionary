from tkinter import *
from tkinter.messagebox import *
from User import Category


class AddCategory:

    def __init__(self, logObj, user):
        self.logObj = logObj
        self.logObj.simpleLog("Creating category addition window")
        self.user = user

        self.root = Tk()
        self.root.resizable(width=FALSE, height=FALSE)

        self.label = Label(self.root, text='Kategória neve:', font=("Helvetica", 13))
        self.entry = Entry(self.root, width=25, borderwidth=2, fg='#000000', relief=GROOVE, font=("Helvetica", 13))
        self.botFrame = Frame(self.root)
        self.forwardButton = Button(self.botFrame, text="OK", font=("Helvetica", 11), command=self.play, relief=GROOVE)
        self.cancelButton = Button(self.botFrame, text="Mégse", font=("Helvetica", 11), command=self.cancelAddition, relief=GROOVE)

        self.label.grid(row=0, sticky=E+W, pady=(5,0))
        self.entry.grid(row=1, sticky=E+W, pady=(2,2))
        self.botFrame.grid(row=2, sticky=E)
        self.cancelButton.grid(row=0, column=1, sticky=E, padx=10)
        self.forwardButton.grid(row=0, column=0, sticky=E)

        self.root.focus_force()
        self.entry.focus()
        self.root.bind('<Return>', self.play)

        self.root.mainloop()

    def play(self):
        entry = self.entry.get()

        if entry != "":
            self.user.categories.append(Category.Category(entry))
            self.user.database.insertIntoTable("Categories", [entry, self.user.username, -1])
            self.root.destroy()
        else:
            showerror("Hiba", "Kategória üresen hagyva!")

    def cancelAddition(self):
        result = askyesno("Megszakítás", "Biztosan megszakítja a hozzáadást?")
        if result:
            self.logObj.simpleLog("Category addition cancelled.")
            self.root.destroy()
        else:
            self.root.focus_force()
            self.logObj.simpleLog("Category addition cancel cancelled.")
