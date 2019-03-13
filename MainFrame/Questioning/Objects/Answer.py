

class Answer:

    def __init__(self, questionObj, givenAnswer):
        self.wordID =       questionObj.wordID
        self.sourceLang =   questionObj.sLang
        self.answerLang =   questionObj.aLang
        self.label =        questionObj.sWord
        self.answer =       questionObj.aWord
        self.givenAnswer =  givenAnswer
