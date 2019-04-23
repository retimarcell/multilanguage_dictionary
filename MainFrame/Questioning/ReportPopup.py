from tkinter import *
from tkinter import ttk


class ReportWindow:

    def __init__(self, logObj, answers):
        self.logObj = logObj
        self.logObj.simpleLog("Creating report window")

        self.root = Tk()
        self.root.title("Kiértékelés")
        self.root.configure(bg='white')
        x = self.root.winfo_screenwidth() / 2 - 250
        y = self.root.winfo_screenheight() / 2 - 200
        self.root.geometry("500x400+%d+%d" % (x, y))
        self.root.resizable(height=FALSE)

        self.mainFrame = Frame(self.root, bg="white")
        self.mainFrame.pack(fill=BOTH, expand=True)

        self.canvas = Canvas(self.mainFrame, bg='white')
        self.canvas.grid(row=0, column=0, sticky='news')

        self.scrollbar = Scrollbar(self.mainFrame, orient="vertical", command=self.canvas.yview)
        self.scrollbar.grid(row=0, column=1, sticky='ns')

        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.innerFrame = Frame(self.canvas, bg='white')
        self.window = self.canvas.create_window((0,0), window=self.innerFrame, anchor='nw')

        self.mainFrame.columnconfigure(0, weight=1)
        self.mainFrame.rowconfigure(0, weight=1)

        self.innerFrame.bind("<Configure>", self.resize)
        self.canvas.bind("<Configure>", self.frameWidth)

        for i in range(len(answers)):
            Label(self.innerFrame, text=answers[i].sourceLang, font=("Helvetica", 9), bg='white').grid(row=3*i, column=0, sticky=W, padx=(2,0), pady=(1,1))
            Label(self.innerFrame, text=answers[i].answerLang, font=("Helvetica", 9), bg='white').grid(row=3*i, column=2, sticky=W, padx=(2,0), pady=(1,1))
            Label(self.innerFrame, text=answers[i].label.capitalize(), font=("Helvetica", 14), bg='white').grid(row=3*i+1, column=0, sticky=W, padx=(2,0), pady=(1,1))
            Label(self.innerFrame, text=" --> ", font=("Helvetica", 11), bg='white').grid(row=3*i+1, column=1, pady=(1,1))
            givenLabel = Label(self.innerFrame, text="\"%s\"" % answers[i].givenAnswer.capitalize(), font=("Helvetica", 14), bg='white')
            givenLabel.grid(row=3*i+1, column=2, pady=(1,1), sticky=W)
            Label(self.innerFrame, text="(%s)" % answers[i].answer.capitalize(), font=("Helvetica", 11), bg='white').grid(row=3*i+1, column=3, padx=(0,2), pady=(1,1), sticky=W)
            sepFrame = Frame(self.innerFrame, bg='black', width=300, height=1, bd=1, relief='sunken')
            sepFrame.grid(row=3*i+2, columnspan=5, sticky="ew")

            if answers[i].progress == 1:
                givenLabel.configure(fg="green")
            else:
                givenLabel.configure(fg="red")

    def resize(self, event=None):
        self.canvas.configure(scrollregion=self.canvas.bbox('all'))

    def frameWidth(self, event):
        canvasWidth = event.width
        self.canvas.itemconfig(self.window, width=canvasWidth)
