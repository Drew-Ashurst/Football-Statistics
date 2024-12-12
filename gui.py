from tkinter import *


class GUI:
    def __init__(self):
        # initializes the window
        self.window = Tk()
        self.window.title("Football Stats")
        self.window.geometry("800x800")
        self.window.resizable(True, True)
        # self.window -> 1x1
        self.window.columnconfigure(0, weight=1)
        self.window.rowconfigure(0, weight=1)

        self.home_window()

    def check_button(self):
        print("working")

    def home_window(self):
        # self.main_home_frame -> 2x1
        self.main_home_frame = Frame(self.window, bg="slate gray")
        self.main_home_frame.rowconfigure(0, weight=1)
        self.main_home_frame.rowconfigure(1, weight=4)
        self.main_home_frame.columnconfigure(0, weight=1)

        # self.home_button_frame -> 5x5
        self.home_button_frame = Frame(self.main_home_frame, bg="red")
        self.home_button_frame.rowconfigure((0, 1, 2, 3, 4), weight=1)
        self.home_button_frame.columnconfigure((0, 1, 2, 3, 4), weight=1)

        self.main_home_frame.grid(row=0, column=0, sticky="nesw")
        self.home_button_frame.grid(row=1, column=0, sticky="news")

        self.button1 = Button(
            self.home_button_frame,
            text="PRINT",
            command=self.check_button,
            bg="blue",
            activebackground="dodger blue",
        )
        self.button1.grid(row=0, column=0, sticky="nesw")

        self.title = Label(
            self.main_home_frame,
            bg="slate gray",
            text="NFL Statistics Analyzer",
            font=("Times New Roman", 50, "bold"),
        ).grid(row=0, column=0, sticky="nesw")


g = GUI()
g.window.mainloop()
