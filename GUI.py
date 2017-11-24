from tkinter import *
from PIL import ImageTk, Image
import os

tk = None


def main():
    init_tkinter()  # initial window
    init_ui()  # initial ui(button, text...)
    tk.mainloop()  # open the window


def init_tkinter():
    global tk
    tk = Tk()
    tk.title("OS window")
    tk.state("zoomed")
    tk.protocol("WM_DELETE_WINDOW", quit_program)


def init_ui():
    GUIDemo(master=tk)


class GUIDemo(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.pack(fill=BOTH, expand=1)
        # self.grid()
        self.createWidgets()

    def createWidgets(self):
        _image = ImageTk.PhotoImage(Image.open("src/elevator.png"))
        ui_elevator = Label(self, image=_image)
        ui_elevator.place(x=200, y=20)
        # ui_elevator.grid()
        ui_elevator.image = _image
        pass


def quit_program():
    os._exit(1)


# ----- functions for thread -----

def create_person():  # create a person ui
    # todo
    return 0


def person_entering(person):  # let waiting person walk into elevator
    # todo
    return True


def person_leaving(person):  # let arrived person leave the window
    # todo
    return True
