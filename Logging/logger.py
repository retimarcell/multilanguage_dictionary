import datetime
import os
import sys


class Logger:

    def __init__(self):
        self.name = datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S") + "log.log"
        self.currDir = os.getcwd()
        self.logPath = self.currDir + "//LOGS//" + self.name
        self.reportPath = self.currDir + "//Reports//"

        if not os.path.exists(self.currDir + "//LOGS"):
            os.makedirs(self.currDir + "//LOGS")

        if not os.path.exists(self.currDir + "//Reports"):
            os.makedirs(self.currDir + "//Reports")

        self.logFile = open(self.logPath, 'w')
        self.simpleLog("Logger initialized")

    def simpleLog(self, message):
        self.logFile.write(datetime.datetime.now().strftime("%Y_%m_%d_%H:%M:%S ") + message + "\n")

    def printAndLog(self, message):
        print(datetime.datetime.now().strftime("%Y_%m_%d_%I:%M:%S ") + message)
        self.logFile.write(datetime.datetime.now().strftime("%Y_%m_%d_%H:%M:%S ") + message + "\n")

    def errorLog(self, e):
        exc_type, exc_obj, tb = sys.exc_info()
        f = tb.tb_frame
        lineno = tb.tb_lineno
        filename = f.f_code.co_filename
        self.logFile.write("{0}: ERROR {1} | Line {2} in {3}".format(datetime.datetime.now().strftime("%Y_%m_%d_%I:%M:%S "), str(e), lineno, filename))
        print("ERROR {0} | Line {1} in {2}".format(str(e), lineno, filename))

    def statementLog(self, message):
        msg = ""
        for ele in message.split():
            if "password=" in ele:
                msg += "password=***** "
            else:
                msg += ele + " "
        self.logFile.write(datetime.datetime.now().strftime("%Y_%m_%d_%H:%M:%S [DB STATEMENT] ") + msg + "\n")

    def arrayItemsLog(self, message, arr):
        msg = message
        if len(arr) > 0:
            msg += " {"
            for ele in arr:
                msg += "%s, " % str(ele)
            msg = msg[:-2] + "}"
        else:
            msg += " {EMPTY}"
        self.logFile.write(datetime.datetime.now().strftime("%Y_%m_%d_%H:%M:%S ") + msg + "\n")

    def setupLog(self, lang, cat, source, mode):
        self.logFile.write(datetime.datetime.now().strftime("%Y_%m_%d_%H:%M:%S Options: \n"))
        printDivider(self.logFile)
        self.arrayItemsLog("Languages: ", lang)
        self.arrayItemsLog("Categories: ", cat)
        self.logFile.write("Source language: %s\n" % source)
        self.logFile.write("Mode: %s\n" % mode)
        printDivider(self.logFile)

    def questionLog(self, wordID, sLang, aLang, sWord, aWord):
        self.logFile.write(datetime.datetime.now().strftime("%Y_%m_%d_%H:%M:%S Question object: \n"))
        printDivider(self.logFile)
        self.logFile.write("WordID:\t%s\n" % wordID)
        self.logFile.write("Source language:\t%s\n" % sLang)
        self.logFile.write("Answer language:\t%s\n" % aLang)
        self.logFile.write("Source word:\t%s\n" % sWord)
        self.logFile.write("Answer word:\t%s\n" % aWord)
        printDivider(self.logFile)

    def createQuestioningReport(self, answerArr):
        temp = self.reportPath + datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S") + ".txt"
        reportFile = open(temp, 'w')

        for i in range(len(answerArr)):
            isLast = i + 1 == len(answerArr)

            attachAnswer(reportFile, answerArr[i], i, isLast)


def attachAnswer(reportFile, answer, index, isLast):
    i = index + 1
    if answer.progress != -1:
        reportFile.write("%i. szó [Helyes]\n" % i)
    else:
        reportFile.write("%i. szó [Rossz]\n" % i)
    reportFile.write("Kérdezett szó: %s (%s)\n" % (answer.label, answer.sourceLang))
    reportFile.write("Várt szó: %s (%s)\n" % (answer.answer, answer.answerLang))
    reportFile.write("Beadott szó: %s\n" % answer.givenAnswer)

    if not isLast:
        printDivider(reportFile)


def printDivider(logf):
    logf.write("\n")
    logf.write("=============================================\n")
    logf.write("\n")
