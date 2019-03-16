class SetupOptions:

    def __init__(self, logObj, l, c, s, m):
        self.languages = l
        self.categories = c
        self.source = s
        self.mode = m

        logObj.setupLog(self.languages, self.categories, self.source, self.mode)
