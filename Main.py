from Logging.logger import Logger
from Windows import LoginWindow as lw
from Windows import MainWindow as mw
from User import User as us
from Database import DatabaseMain as dm
from tkinter import TclError
from tkinter import Tk
from tkinter import messagebox
import sys

if __name__ == '__main__':
    logObj = Logger()

    try:
        database = dm.Database(logObj)
    except:
        root = Tk()
        root.withdraw()
        messagebox.showerror("Hiba", "A rendszer nem tud csatlakozni az adatbázishoz.")
        sys.exit(1)

    loginWindow = lw.LoginWindow(logObj, database)

    try:
        user = us.User(logObj, loginWindow.user, database, loginWindow.isFirstTime)
    except AttributeError:
        sys.exit(0)

    try:
        mainWindow = mw.MainWindow(logObj, user, database)
    except TclError:
        pass

    database.dbConnection.close()
