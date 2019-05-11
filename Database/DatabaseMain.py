import datetime
import os
import mysql.connector as mariadb
import configparser


class Database:

    def __init__(self, logObj):
        self.logObj = logObj
        self.logObj.simpleLog('Connecting to database...')
        config = configparser.ConfigParser()
        config.read(os.getcwd() + '\\Database\\config.ini')
        self.dbConnection = mariadb.connect(host=config['CONFIG']['host'],
                                            user=config['CONFIG']['username'],
                                            password=config['CONFIG']['password'],
                                            port=config['CONFIG']['port'],
                                            database=config['CONFIG']['database'])
        self.logObj.simpleLog('Database connection estabilished.')

        self.cursor = self.dbConnection.cursor()
        self.nextWordID = 0
        self.setNextWordID()

    def executeStatement(self, statement):
        self.logObj.statementLog(statement)
        self.cursor.execute(statement)
        self.logObj.statementLog("Statement executed.")

    def setNextWordID(self):
        returnValue = self.simpleSelectFromTable("WordID")
        tempArr = []

        for ele in returnValue:
            tempArr.append(ele[1])

        i = 1
        while True:
            if i not in tempArr:
                self.logObj.simpleLog("Next free Word ID: %i" % i)
                self.nextWordID = i
                break
            i = i + 1

    def checkUsersExists(self, username, password=None):
        self.logObj.simpleLog("Login check on database on Users.")

        if password is None:
            statement = "select * from Users where username=\"%s\"" % username
        else:
            statement = "select * from Users where username=\"%s\" and password=\"%s\"" % (username, password)

        self.executeStatement(statement)
        if len(self.cursor.fetchall()) == 1:
            return True
        return False


    def register(self, username, password):
        self.logObj.simpleLog("Adding new entry to Users.")

        if not self.checkUsersExists(username):
            statement = "insert into Users values (\"%s\", \"%s\", \"%s\", 0)" % (username, password, datetime.datetime.now().strftime("%Y-%m-%d"))

            self.executeStatement(statement)
            self.dbConnection.commit()
            return True

        self.logObj.simpleLog("User already exists")
        return False


    def updateLoginTime(self, username, time):
        self.logObj.simpleLog("Creating update statement for user login")

        statement = "update Users set last_login='%s' where username='%s'" % (time, username)

        self.executeStatement(statement)
        self.dbConnection.commit()


    def simpleSelectFromTable(self, table, where=None, what=None):
        self.logObj.simpleLog("Creating select statement...")
        statement = "select * from %s" % table

        if where is not None:
            statement += " where "
            for i in range(len(where)):
                statement += "%s=\"%s\" and " % (where[i], what[i])
            statement = statement[:-5]

        self.executeStatement(statement)
        return self.cursor.fetchall()


    def insertIntoTable(self, table, values):
        self.logObj.simpleLog("Creating insert statement...")
        statement = "insert into %s values (" % table

        for value in values:
            if type(value) is int:
                statement += "%i," % value
            else:
                statement += "\"%s\"," % value

        statement = statement[:-1] + ")"

        self.executeStatement(statement)
        self.dbConnection.commit()


    def changeWord(self, language, previousValue, newValue, wordID):
        self.logObj.simpleLog("Changing word in \"%s\" language" % language)

        statement = "update l_%s set word='%s', progress=%i where word='%s' and wordID=%i" % (language, newValue, 0, previousValue, wordID)

        self.executeStatement(statement)
        self.dbConnection.commit()


    def deleteRow(self, table, where, what):
        self.logObj.simpleLog("Creating delete statement...")
        statement = "delete from %s where " % table

        for i in range(len(where)):
            statement += "%s=\"%s\" and " % (where[i], str(what[i]))
        statement = statement[:-5]

        self.executeStatement(statement)
        self.dbConnection.commit()


    def updateProgress(self, table, wordID, progress):
        self.logObj.simpleLog("Creating update statement for progress")
        statement = "update l_%s set progress=%i where wordID=%i" % (table, progress, wordID)

        self.executeStatement(statement)
        self.dbConnection.commit()


    def updateHelp(self, newAmount, help, user):
        self.logObj.simpleLog("Creating update statement for help amount")
        statement = "update Helps set amount=%i where help='%s' and username='%s'" % (newAmount, help, user)

        self.executeStatement(statement)
        self.dbConnection.commit()


    def updateChallenge(self, sL, dL, a, r, rA, user, progress):
        self.logObj.simpleLog("Creating update statement for challenge progress")
        statement = "update Challenge_Ongoings set progress=%i where sourceLang='%s' and destinationLang='%s' and amount=%i and reward='%s' and rewardAmount=%i and username='%s'" % (progress, sL, dL, a, r, rA, user)

        self.executeStatement(statement)
        self.dbConnection.commit()


    def updateXp(self, user, newXp):
        self.logObj.simpleLog("Creating update statement for user xp")
        statement = "update Users set xp=%i where username='%s'" % (newXp, user)

        self.executeStatement(statement)
        self.dbConnection.commit()


    def updateLanguageXp(self, lang, user, newXp):
        self.logObj.simpleLog("Creating update statement for language xp")
        statement = "update Languages set xp=%i where username='%s' and language='%s'" % (newXp, user, lang)

        self.executeStatement(statement)
        self.dbConnection.commit()


    def getCount(self, table, countArg, where=None, what=None):
        self.logObj.simpleLog("Creating select count(%s) statement for %s" % (countArg, table))

        statement = "select count(%s) from %s" % (countArg, table)

        if where is not None:
            statement += " where "

            for i in range(len(where)):
                statement += "%s=\"%s\" and " % (where[i], what[i])
            statement = statement[:-5]
        try:
            self.executeStatement(statement)
            return self.cursor.fetchall()[0][0]
        except:
            return 0


    def createTable(self, table, values, types):
        self.logObj.simpleLog("Creating create table statement for: %s" % table)

        statement = "create table if not exists %s (" % table

        for i in range(len(values)):
            statement += "%s %s, " % (values[i], types[i])
        statement = statement[:-2] + ")"

        self.executeStatement(statement)
        self.dbConnection.commit()


    def dropTable(self, table):
        self.logObj.simpleLog("Creating drop table statement for: %s" % table)

        statement = "drop table %s" % table

        self.executeStatement(statement)
        self.dbConnection.commit()
