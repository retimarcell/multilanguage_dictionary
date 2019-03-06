from Logging import logger
from Windows import LoginWindow as lw
from Windows import MainWindow as mw
from User import User as us
from Database import DatabaseMain as dm

if __name__ == '__main__':
    logObj = logger.Logger()
    try:
        database = dm.Database(logObj)

        loginWindow = lw.LoginWindow(logObj, database)
        user = us.User(logObj, loginWindow.user, database)

        mainWindow = mw.MainWindow(logObj, user, database)
    except Exception as e:
        logObj.errorLog(e)
