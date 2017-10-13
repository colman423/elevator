import tkinter as TK


def main():
    tk = init_tkinter()  # initial window
    init_ui(tk)  # initial ui(button, text...)
    # tk.mainloop()  # open the window


def init_tkinter():
    tk = TK.Tk()
    tk.title("OS window")
    tk.state("zoomed")
    return tk


def init_ui(tk):
    label = TK.Label(tk, text="Hello World!")
    label.pack()


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
