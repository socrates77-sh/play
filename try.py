from tkinter import *

class Test(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        Pack.config(self)
        self.draw = Canvas(self)
        self.draw.pack()
        # self.draw.bind("<MouseWheel>", self.mouseWheel)
        self.bind("<Return>", self.mouseWheel)

    def mouseWheel(self, event):
        self.draw.create_rectangle(50, 50, 100, 100)
        print('wheel')

root = Tk()
test = Test(master=root)
test.mainloop()