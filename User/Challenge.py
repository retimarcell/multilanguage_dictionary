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

    def updateSource(self, sourceL):
        self.sourceLanguage = sourceL
        self.description = "%s: %s" % (self.description, self.sourceLanguage)

    def updateDestination(self, destL):
        self.destinationLanguage = destL
        self.description = "%s: %s" % (self.description, self.destinationLanguage)

    def getHelpAndAmount(self):
        return [self.reward, self.rewardAmount]

    def __eq__(self, other):
        return (self.description == other.description and
                self.sourceLanguage == other.sourceLanguage and
                self.destinationLanguage == other.destinationLanguage and
                self.amount == other.amount and
                self.reward == other.reward and
                self.rewardAmount == other.rewardAmount and
                self.progress == other.progress and
                self.isDone == other.isDone)
