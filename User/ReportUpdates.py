

class ReportUpdates:

    def __init__(self, xp):
        self.startingXp = xp
        self.finishXp = 0
        self.amountOfLevelUps = 0
        self.languageLevelUps = []
        self.rewards = []

    def calculateFinishXp(self, xp):
        self.finishXp = xp - self.startingXp
