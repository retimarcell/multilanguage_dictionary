class Challenge:

    def __init__(self, d, sL, dL, a, r, rA, p):
        self.description = d
        self.sourceLanguage = sL
        self.destinationLanguage = dL
        self.amount = a
        self.reward = r
        self.rewardAmount = rA
        self.progress = p
        self.noLanguageRestriction = (self.sourceLanguage == "-" and self.destinationLanguage == "-")
        self.isDone = False

    def getHelpAndAmount(self):
        return [self.reward, self.rewardAmount]
