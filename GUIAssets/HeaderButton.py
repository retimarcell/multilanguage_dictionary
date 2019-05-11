from tkinter import *


class HeaderButton(Button):

    def __init__(self, logObj, root, title, pos):
        self.logObj = logObj
        self.position = pos
        self.title = title
        self.onDisplay = False
        self.logObj.simpleLog("Creating header button with title \"%s\"" % self.title)

        Button.__init__(self, master=root, text=self.title, bg='white', activebackground='silver', font=('Helvetica', '15'), width=27)
        self.grid(column=self.position, row=0, sticky=W)

        self.bind("<Enter>", self.on_hover)
        self.bind("<Leave>", self.off_hover)


    def on_hover(self, e):
        self.logObj.simpleLog("Hovering on \"%s\"" % self.title)
        self.configure(bg='lightgrey')


    def off_hover(self, e):
        self.logObj.simpleLog("Hovering stopped on \"%s\"" % self.title)
        self.configure(bg='white')
