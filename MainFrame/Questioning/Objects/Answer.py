

class Answer:

    def __init__(self, logObj, questionObj, givenAnswer):
        self.logObj =       logObj
        self.wordID =       questionObj.wordID
        self.sourceLang =   questionObj.sourceLang
        self.answerLang =   questionObj.answerLang
        self.label =        questionObj.label
        self.answer =       questionObj.answer.lower()
        self.givenAnswer =  givenAnswer.lower()

        self.analyze()

    def analyze(self):

        self.progress = 0
        if self.answer == self.givenAnswer:
            self.progress = 1
        else:
            self.progress = -1
