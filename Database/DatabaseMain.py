import mysql.connector as mariadb

class Database():

    def __init__(self, logObj):
        self.logObj = logObj
        self.logObj.simpleLog('Connecting to database...')
        self.dbConnection = mariadb.connect(host='nemethi.ddns.net', user='marcell_reti', password='password', port=3306, database='multilanguage_dictionary')
        self.logObj.simpleLog('Database connection estabilished.')

        self.cursor = self.dbConnection.cursor()
        self.maxWordID = self.getCount("WordID", "*")


    def executeStatement(self, statement):
        self.logObj.statementLog(statement)
        self.cursor.execute(statement)
        self.logObj.statementLog("Statement executed.")


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
            statement = "insert into Users values (\"%s\", \"%s\")" % (username, password)

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
