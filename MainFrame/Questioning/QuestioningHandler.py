from tkinter import *
from tkinter import ttk
from tkinter.messagebox import *

from MainFrame.Questioning import QuestioningSetup as qs
from MainFrame.Questioning import QuestioningFrame as qf
from MainFrame.Questioning import QuestioningReportFrame as qrf


class QuestioningHandlerFrame(Frame):

    def __init__(self, logobj, root, user):
        self.logObj = logobj
        self.logObj.simpleLog("Creating base frame for questioning...")
        self.user = user

        Frame.__init__(self, master=root, bg='white')
        self.pack_propagate(0)
        self.pack(fill=BOTH, expand=1)


        self.createQuestioningSetupFrame()

    def createQuestioningSetupFrame(self):
        self.showedFrame = qs.QuestioningSetupFrame(self.logObj, self, self.user)

        self.topFrame = Frame(self, bg='white')
        self.topFrame.grid(row=0, sticky=W)
        self.topLabel = Label(self.topFrame, text='Beállítás', bg='white', font=("Helvetica", 38), anchor='w')
        self.topLabel.grid(row=0, sticky=W)
        self.separator = ttk.Separator(self.topFrame, orient=HORIZONTAL)
        self.separator.grid(row=1, column=0, sticky="ew")

        self.helpButton = Button(self.topFrame, text='? ', font=("Helvetica", 11), anchor='e', relief=GROOVE, bg='white', height=1, width=2)
        self.helpButton.bind('<Button-1>', lambda x: 'break')
        self.helpButton.bind('<Button-1>', lambda x: 'break')
        self.helpButton.bind('<Enter>', self.enter1)
        self.helpButton.bind('<Leave>', self.leave)
        self.helpButton.grid(row=0, column=1, pady=(0,16), padx=(957,5), sticky=S)

        self.submitButton = Button(self, text="Indítás", width=10, command=self.startQuestioning, bg='white', activebackground='white', font=('Helvetica', 11))
        self.submitButton.grid(row=3, sticky=E, padx=(0,115), pady=(10,0))

    def enter1(self, event=None):
        self.enterMain(1)
        Label(self.topLevelWidget,
              text="Kategória: Válassza ki a kategóriákat, amiből szeretne kikérdezést indítani (alap helyzetben minden ki van választva)\n"
                   "Nyelv: Válassza ki a nyelveket, amelyeket szeretné, hogy megjelenjenek a kikérdezés során (alap helyzetben minden ki van választva)\n"
                   "Kezdő nyelv: Válassza ki a nyelvet, amiből le akarja fordítani a szavakat\n"
                   "Nehézség:\n - Normál: Maximum 15 kérdés\n - Könnyített: Maximum 10 kérdés\n - Nehezített: Maxmimum 30 kérdés, a kezdő nyelv nincs feltűntetve",
              bg='white', font=("Helvetica", 11), relief=RIDGE, borderwidth=2, anchor='w').pack(fill=BOTH)

    def enter2(self, event=None):
        self.enterMain(2)
        Label(self.topLevelWidget,
              text="Fordítsa le a szöveget, a szó alatt látható nyelvre.\nSegítségei nem töltődnek újra.",
              bg='white', font=("Helvetica", 11), relief=RIDGE, borderwidth=2, anchor='w').pack(fill=BOTH)

    def enterMain(self, enterCount):
        x, y, cx, cy = self.helpButton.bbox("insert")
        if enterCount == 1:
            x += self.helpButton.winfo_rootx() - 830
        else:
            x += self.helpButton.winfo_rootx() - 285
        y += self.helpButton.winfo_rooty() + 20
        self.topLevelWidget = Toplevel(self.helpButton)
        self.topLevelWidget.wm_overrideredirect(True)
        self.topLevelWidget.wm_geometry("+%d+%d" % (x, y))

    def leave(self, event=None):
        self.topLevelWidget.destroy()

    def startQuestioning(self):
        self.setupOptions = self.showedFrame.getSetup()
        self.showedFrame.destroy()
        self.submitButton.destroy()
        self.createQuestioningFrame()

    def createQuestioningFrame(self):
        if len(self.user.languages) < 2 or len(self.user.wordIDs) == 0:
            showerror("Hiba!", "Legalább két nyelvre és egy szóra szükség van a kikérdezéshez!")
            self.showedFrame.destroy()
            self.createQuestioningSetupFrame()
        elif self.setupOptions.source in self.setupOptions.languages and len(self.setupOptions.languages) == 1:
            showerror("Hiba!", "Nem lehet csak egy és ugyanazon nyelv a választottak között ami megegyezik a kezdőnyelvvel!")
            self.showedFrame.destroy()
            self.createQuestioningSetupFrame()
        else:
            self.topLabel.config(text='Kikérdezés')
            self.helpButton.bind('<Enter>', self.enter2)
            self.helpButton.grid(row=0, column=1, pady=(0,16), padx=(901,5), sticky=S)
            self.showedFrame = qf.QuestioningFrame(self.logObj, self, self.setupOptions, self.user)

    def finishQuestioning(self):
        self.showedFrame.fullDestroy()
        self.topLabel.destroy()
        self.separator.destroy()
        self.topFrame.destroy()
        self.showedFrame = qrf.ReportFrame(self.logObj, self, self.user)
