from strings import (RESULTS_NOT_FOUND,
                     SEVERITY_CRITICAL,
                     SEVERITY_HIGH,
                     SEVERITY_MEDIUM,
                     SEVERITY_LOW,
                     SECONDS,
                     SEVERITY,
                     SCORE
                     )

from colorama import Fore
from colorama import Style
from tkinter import Tk, Listbox, Label, BOTH, LEFT, RIGHT, Y, W, LabelFrame, Button
from values import DEFAULT_APP_HEIGHT, DEFAULT_APP_WIDTH


class View:
    def __init__(self, model):
        self.__model = model
        self.__download_function = None
        self.__window_width = DEFAULT_APP_WIDTH
        self.__window_height = DEFAULT_APP_HEIGHT
        self.__window_size = f'{self.__window_width}x{self.__window_height}'
        self.__values = []
        self.__severity_to_colors_converter = {
            SEVERITY_CRITICAL: Fore.LIGHTRED_EX,
            SEVERITY_HIGH: Fore.RED,
            SEVERITY_MEDIUM: Fore.YELLOW,
            SEVERITY_LOW: Fore.GREEN,
            None: Fore.MAGENTA
        }
        self.__root = Tk()
        self.__root.geometry(self.__window_size)
        self.__download_button = Button(self.__root,
                                        text="Pobierz")

        #self.__update_values_button = Button(self.__root,
        #                                    text="Wyswietl",
        #                                    command=self.__show_values)

        self.__listbox = Listbox(self.__root,
                           height = 25,
                           width = 15,
                           activestyle = 'dotbox')
        self.__listbox.bind("<<ListboxSelect>>", self.callback)

        self.__frame = LabelFrame(self.__root, text="CVE")

        self.__severity_lab = Label(self.__frame, text="Severity")
        self.__score_lab = Label(self.__frame, text="Score")
        self.__description_lab = Label(self.__frame, text="Descriptions")

        self.__severity_value_lab = Label(self.__frame, text="Value of Severity")
        self.__score_value_lab = Label(self.__frame, text="Value of Score")
        self.__description_value_lab = Label(self.__frame, text="Value of Descriptions")

        self.__download_button.pack()
       # self.__update_values_button.pack()

        self.__listbox.pack(fill=Y, expand=True, side=LEFT, anchor=W)
        self.__frame.pack(fill=BOTH, expand=True, side=RIGHT)

        self.__severity_lab.pack(fill=BOTH, expand=True)
        self.__score_lab.pack(fill=BOTH, expand=True)
        self.__description_lab.pack(fill=BOTH, expand=True)

        self.__severity_value_lab.pack(fill=BOTH, expand=True)
        self.__score_value_lab.pack(fill=BOTH, expand=True)
        self.__description_value_lab.pack(fill=BOTH, expand=True)

    def callback(self, event):
        selection = event.widget.curselection()
        if selection:
            index = selection[0]
            self.update_values(index)

    def add_item_to_list(self, CVE_name):
        self.__listbox.insert(self.__listbox.size(), CVE_name)

    def set_download_function(self, function):
        self.__download_button.config(command=function)

    def update_values(self, index):
        item = self.__model.values[index]
        self.__score_value_lab.configure(text=item.item.score[1])
        self.__severity_value_lab.configure(text=item.item.score[2])
        self.__description_value_lab.configure(text=item.item.descriptions[0].value)

    def run_view(self):
        self.__root.mainloop()
