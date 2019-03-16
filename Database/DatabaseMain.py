import mysql.connector as mariadb

class Database():

    def __init__(self, logObj):
        self.logObj = logObj
        self.logObj.simpleLog('Connecting to database...')
        self.dbConnection = mariadb.connect(host='nemethi.ddns.net', user='marcell_reti', password='password', port=3306, database='multilanguage_dictionary')
        self.logObj.simpleLog('Database connection estabilished.')

        self.cursor = self.dbConnection.cursor()


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


    def changeWord(self, language, previousValue, newValue):
        self.logObj.simpleLog("Changing word in \"%s\" language" % language)

        statement = "update l_%s set word='%s', progress=%i where word='%s'" % (language, newValue, 0, previousValue)

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
