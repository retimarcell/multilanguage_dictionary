from tkinter import *
import tkinter.messagebox as mb
import datetime
import re


class LoginWindow:
    def __init__(self, logObj, database):
        self.logObj = logObj
        self.db = database
        self.logObj.simpleLog("Creating login window...")

        self.root = Tk()
        self.root.title("Bejelentkezés")
        self.root.configure(background='white')
        self.ws = self.root.winfo_screenwidth() / 2 - 200
        self.hs = self.root.winfo_screenheight() / 2 - 300
        self.root.geometry('350x95+%d+%d' % (self.ws, self.hs))
        self.root.resizable(width=FALSE, height=FALSE)

        self.frame = Frame(self.root, bg='white')
        self.frame.pack_propagate(0)
        self.frame.pack(fill=BOTH, expand=1)
        self.buttonFrame = Frame(self.frame)
        self.buttonFrame.grid(row=3, column=1, sticky=E, padx=(0,2))
        self.logObj.simpleLog("Frame creation...")

        self.labelUsername = Label(self.frame, text="Felhasználónév: ", font=("Helvetica", 12), bg='white')
        self.labelPassword = Label(self.frame, text="Jelszó: ", font=("Helvetica", 12), bg='white')
        self.entryUsername = Entry(self.frame, borderwidth=2, fg='#000000', relief=GROOVE, font=("Helvetica", 13), width=22)
        self.entryPassword = Entry(self.frame, show="*", borderwidth=2, fg='#000000', relief=GROOVE, font=("Helvetica", 13), width=22)
        self.loginButton = Button(self.buttonFrame, text="Bejelentkezés", command=self.login, font=("Helvetica", 11), bg='white', activebackground='white')
        self.registerButton = Button(self.buttonFrame, text='Regisztráció', command=self.register, font=("Helvetica", 11), bg='white', activebackground='white')

        self.root.bind('<Return>', self.login)

        self.labelUsername.grid(row=0, column=0, padx=(10,0), pady=(5,0))
        self.labelPassword.grid(row=1, column=0, padx=(10,0))
        self.entryUsername.grid(row=0, column=1, padx=(0,2), pady=(5,0))
        self.entryPassword.grid(row=1, column=1, padx=(0,2))
        self.loginButton.grid(row=0, column=0, sticky=E)
        self.registerButton.grid(row=0, column=1, sticky=E, padx=(1,0))
        self.logObj.simpleLog("Frame set.")

        self.entryUsername.focus_force()
        self.root.mainloop()

    def login(self, event=None):
        self.logObj.simpleLog("Attempt to login...")
        self.logObj.simpleLog("Logging in with \"%s\"" % self.entryUsername.get())

        if self.db.checkUsersExists(self.entryUsername.get(), self.entryPassword.get()):
            self.logObj.simpleLog("Login was successful for \"%s\"" % self.entryUsername.get())
            mb.showinfo("Siker!", "Üdvözlöm, %s!" % self.entryUsername.get())
            self.user = self.entryUsername.get()
            self.isFirstTime = self.handleDate()
            self.logObj.simpleLog("Closing the login window...")
            self.root.destroy()
        else:
            self.logObj.simpleLog("Login was NOT successful for \"%s\"" % self.entryUsername.get())
            mb.showerror("Hiba!", "Rossz felhasználónév/jelszó!")

    def handleDate(self):
        lastLogin = self.db.simpleSelectFromTable("Users", ["username"], [self.user])[0][2]
        date = datetime.datetime.now().strftime("%Y-%m-%d")

        self.db.updateLoginTime(self.user, date)
        if str(lastLogin) == str(date):
            return False
        return True

    def register(self):
        self.clearEntries()

        self.labelPasswordConfirm = Label(self.frame, text="Jelszó újra: ", font=("Helvetica", 12), bg='white')
        self.entryPasswordConfirm = Entry(self.frame, show='*', borderwidth=2, fg='#000000', relief=GROOVE, font=("Helvetica", 13), width=22)
        self.labelPasswordConfirm.grid(row=2, column=0, padx=(10,0))
        self.entryPasswordConfirm.grid(row=2, column=1, padx=(0,2), sticky=E)
        self.root.geometry('350x120+%d+%d' % (self.ws, self.hs))
        self.root.title("Regisztráció")
        self.entryUsername.focus_force()

        self.loginButton.configure(text='Regisztráció', command=lambda x='R': self.endRegister(x))
        self.registerButton.configure(text='Mégse', command=lambda x='C': self.endRegister(x))


    def endRegister(self, value):
        if value == 'R':
            entryUN = self.entryUsername.get()
            entryPW = self.entryPassword.get()
            entryPWC = self.entryPasswordConfirm.get()

            if entryUN == "" or entryPW == "":
                self.logObj.simpleLog("Register failed: Missing username/password.")
                mb.showerror("Hiba!", "Hiányzó felhasználónév/jelszó!")
            elif entryPW != entryPWC:
                self.logObj.simpleLog("Register failed: Passwords are not corresponding.")
                mb.showerror("Hiba!", "Nem megegyező a két jelszó!")
            elif re.match("^[a-zA-Z0-9]+$", entryUN) is None:
                self.logObj.simpleLog("Register failed: Not accepted characters in username.")
                mb.showerror("Hiba!", "Felhasználóhoz megengedett karakterek: angol abc kis és nagybetűi, és számok")
            elif re.match("^[a-zA-Z0-9]+$", entryPW) is None:
                self.logObj.simpleLog("Register failed: Not accepted characters in password.")
                mb.showerror("Hiba!", "Jelszóhoz megengedett karakterek: angol abc kis és nagybetűi, és számok")
            else:
                if not self.db.register(entryUN, entryPW):
                    self.logObj.simpleLog("Register failed because of duplicate username.")
                    mb.showerror("Hiba!", "Felhasználónév már létezik!")
                else:
                    self.logObj.simpleLog("Succesful registration for: %s" % entryUN)
                    mb.showinfo("Siker!", "Sikeres regisztráció: %s" % entryUN)
                    value = 'C'

        if value == 'C':
            self.clearEntries()
            self.labelPasswordConfirm.destroy()
            self.entryPasswordConfirm.destroy()
            self.loginButton.configure(text="Bejelentkezés", command=self.login)
            self.registerButton.configure(text='Regisztráció', command=self.register)
            self.root.geometry('350x90+%d+%d' % (self.ws, self.hs))
            self.entryUsername.focus_force()
            self.root.title("Bejelentkezés")


    def clearEntries(self):
        self.logObj.simpleLog("Clearing entries.")
        self.entryUsername.delete(0, END)
        self.entryPassword.delete(0, END)
        self.entryUsername.insert(0, "")
        self.entryPassword.insert(0, "")

