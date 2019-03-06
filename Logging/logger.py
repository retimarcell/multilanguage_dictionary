import datetime
import os
import sys

class Logger:

    def __init__(self):
        self.name = datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S") + "log.log"
        self.logPath = os.getcwd() + "//LOGS//" + self.name
        if not os.path.exists(os.getcwd() + "//LOGS"):
            os.makedirs(os.getcwd() + "//LOGS")
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
