from tkinter import *
import tkinter.messagebox as mb
import datetime


class LoginWindow:
    def __init__(self, logObj, database):
        self.logObj = logObj
        self.db = database
        self.logObj.simpleLog("Creating login window...")

        self.root = Tk()
        self.frame = Frame(self.root)
        self.frame.pack()
        self.buttonFrame = Frame(self.frame)
        self.buttonFrame.grid(row=3, column=1)
        self.logObj.simpleLog("Frame creation...")

        self.labelUsername = Label(self.frame, text="Username: ")
        self.labelPassword = Label(self.frame, text="Password: ")
        self.entryUsername = Entry(self.frame)
        self.entryPassword = Entry(self.frame, show="*")
        self.loginButton = Button(self.buttonFrame, text="Login", command=self.login)
        self.registerButton = Button(self.buttonFrame, text='Register', command=self.register)

        self.root.bind('<Return>', self.login)

        self.labelUsername.grid(row=0, column=0)
        self.labelPassword.grid(row=1, column=0)
        self.entryUsername.grid(row=0, column=1)
        self.entryPassword.grid(row=1, column=1)
        self.loginButton.grid(row=0, column=0)
        self.registerButton.grid(row=0, column=1)
        self.logObj.simpleLog("Frame set.")

        self.root.focus_force()
        self.entryUsername.focus()
        self.root.mainloop()

    def login(self, event=None):
        self.logObj.simpleLog("Attempt to login...")
        self.logObj.simpleLog("Logging in with \"%s\"" % self.entryUsername.get())

        if self.db.checkUsersExists(self.entryUsername.get(), self.entryPassword.get()):
            self.logObj.simpleLog("Login was successful for \"%s\"" % self.entryUsername.get())
            mb.showinfo("Success!", "Welcome %s" % self.entryUsername.get())
            self.user = self.entryUsername.get()
            self.isFirstTime = self.handleDate()
            self.logObj.simpleLog("Closing the login window...")
            self.root.destroy()
        else:
            self.logObj.simpleLog("Login was NOT successful for \"%s\"" % self.entryUsername.get())
            mb.showerror("Failure!", "Incorrect login credentials!")

    def handleDate(self):
        lastLogin = self.db.simpleSelectFromTable("Users", ["username"], [self.user])[0][2]
        date = datetime.datetime.now().strftime("%Y-%m-%d")

        self.db.updateLoginTime(self.user, date)
        if lastLogin == date:
            return False
        return True

    def register(self):
        self.clearEntries()

        self.labelPasswordConfirm = Label(self.frame, text="Password Again: ")
        self.entryPasswordConfirm = Entry(self.frame, show='*')
        self.labelPasswordConfirm.grid(row=2, column=0)
        self.entryPasswordConfirm.grid(row=2, column=1)

        self.loginButton.configure(text='Register', command=lambda x='R': self.endRegister(x))
        self.registerButton.configure(text='Cancel', command=lambda x='C': self.endRegister(x))


    def endRegister(self, value):
        # TODO create helps in database
        if value == 'R':
            if self.entryUsername.get() == "" or self.entryPassword.get() == "" or self.entryPasswordConfirm.get() == "":
                self.logObj.simpleLog("Register failed: Missing username/password.")
                mb.showerror("Failure!", "Missing username/password!")
            elif self.entryPassword.get() != self.entryPasswordConfirm.get():
                self.logObj.simpleLog("Register failed: Passwords are not corresponding.")
                mb.showerror("Failure!", "Passwords are not corresponding!")
            else:
                if not self.db.register(self.entryUsername.get(), self.entryPassword.get()):
                    self.logObj.simpleLog("Register failed because of duplicate username.")
                    mb.showerror("Failure!", "Username already exists!")
                else:
                    self.logObj.simpleLog("Succesful registration for: %s" % self.entryUsername.get())
                    mb.showinfo("Success!", "Succesful registration with username: %s" % self.entryUsername.get())
                    value = 'C'

        if value == 'C':
            self.clearEntries()
            self.labelPasswordConfirm.destroy()
            self.entryPasswordConfirm.destroy()
            self.loginButton.configure(text="Login", command=self.login)
            self.registerButton.configure(text='Register', command=self.register)


    def clearEntries(self):
        self.logObj.simpleLog("Clearing entries.")
        self.entryUsername.delete(0, END)
        self.entryPassword.delete(0, END)
        self.entryUsername.insert(0, "")
        self.entryPassword.insert(0, "")
