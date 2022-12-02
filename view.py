from strings import (RESULTS_NOT_FOUND,
                     START_DOWNLOADING,
                     STOP_DOWNLOADING,
                     DESCRIPTIONS,
                     SEVERITY_CRITICAL,
                     SEVERITY_HIGH,
                     SEVERITY_MEDIUM,
                     SEVERITY_LOW,
                     SECONDS,
                     SEVERITY,
                     SCORE
                     )
from colorama import Fore
from tkinter import (
        Tk,
        Listbox,
        Label,
        BOTH,
        LEFT,
        RIGHT,
        BOTTOM,
        Y, W, N, S, E,
        LabelFrame,
        Button,
        ttk,
        HORIZONTAL,
        Frame
        )
from values import DEFAULT_APP_HEIGHT, DEFAULT_APP_WIDTH


class View:
    def __init__(self, model):
        self.__is_downloading_in_progress = False
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

        self.__top_frame = Frame(self.__root)
        self.__download_button = Button(
                self.__top_frame,
                text=START_DOWNLOADING
                )
        self.__stop_dowload_button = Button(
                self.__top_frame,
                text=STOP_DOWNLOADING
                )

        self.__download_frame = Frame(self.__top_frame)
        self.__current_app_downloading_label = Label(self.__download_frame)
        self.__position_downloading_label = Label(self.__download_frame)
        self.__downloading_pb = ttk.Progressbar(
                self.__download_frame,
                orient=HORIZONTAL,
                length=DEFAULT_APP_WIDTH-2, mode='determinate',
                )

        self.__left_frame = Frame(self.__root)
        self.__listbox = Listbox(self.__left_frame, activestyle='dotbox')
        self.__listbox.bind("<<ListboxSelect>>", self.on_click_listbox_item)

        self.__details_frame = LabelFrame(self.__root, text="CVE")
        self.__severity_frame = Frame(self.__details_frame)
        self.__severity_lab = Label(self.__severity_frame, text=SEVERITY)
        self.__severity_value_lab = Label(self.__severity_frame, text="Value of Severity")
        self.__score_frame = Frame(self.__details_frame)
        self.__score_lab = Label(self.__score_frame, text=SCORE)
        self.__score_value_lab = Label(self.__score_frame, text="Value of Score")

        self.__description_frame = Frame(self.__details_frame)
        self.__description_lab = Label(self.__description_frame, text=DESCRIPTIONS)
        self.__description_value_lab = Label(self.__description_frame, text="Value of Descriptions")
        self.__description_value_lab.bind('<Configure>',
                lambda e: self.__description_value_lab.config(wraplength=self.__description_value_lab.winfo_width()))

        self.__pack_items()

    def __pack_items(self):
        self.__top_frame.pack(anchor=N)
        self.__download_button.pack()

        self.__left_frame.pack(fill=Y, expand=True, side=LEFT, anchor=W)
        self.__listbox.pack(fill=Y, expand=True)

        self.__details_frame.pack(fill=BOTH, expand=True, side=RIGHT)
        self.__description_frame.pack(side=BOTTOM, ipadx=4, ipady=4)
        self.__description_lab.pack()
        self.__description_value_lab.pack()
        self.__severity_frame.pack(side=RIGHT, ipadx=4, ipady=4)
        self.__severity_lab.pack()
        self.__severity_value_lab.pack()
        self.__score_frame.pack(side=LEFT, expand=True)
        self.__score_lab.pack()
        self.__score_value_lab.pack()

    def switch_progressbar_visibility(self, visible):
        if visible:
            self.__download_frame.pack()
            self.__current_app_downloading_label.pack(side=LEFT, anchor=W, ipadx=4)
            self.__position_downloading_label.pack(side=RIGHT, anchor=E, ipadx=4)
            self.__downloading_pb.pack()
            self.__stop_dowload_button.pack()
            self.__download_button.forget()
        else:
            self.__download_frame.forget()
            self.__stop_dowload_button.forget()
            self.__download_button.pack()

    def on_click_listbox_item(self, event):
        selection = event.widget.curselection()
        if selection:
            self.update_values(selection[0])

    def add_item_to_list(self, CVE_name):
        self.__listbox.insert(self.__listbox.size(), CVE_name)

    def set_stop_downloading_function(self, function):
        self.__stop_dowload_button.config(command=function)

    def set_stop_button_enabled(self):
        self.__stop_dowload_button['state'] = "disabled"

    def set_stop_button_normal(self):
        self.__stop_dowload_button['state'] = "normal"

    def set_download_function(self, function):
        self.__downloading_pb.pack()
        self.__download_button.config(command=function)

    def update_download_notifications(self, app_name='', position=''):
        self.__current_app_downloading_label.config(text=app_name)
        self.__position_downloading_label.config(text=position)

    def update_progressbar(self):
        self.__downloading_pb['value'] += 100/len(self.__model.database)

    def reset_progressbar(self):
        self.__downloading_pb['value'] = 0

    def update_values(self, index):
        item = self.__model.values[index]
        self.__details_frame.configure(text=item.app_name)
        self.__score_value_lab.configure(text=item.item.score[1])
        self.__severity_value_lab.configure(text=item.item.score[2])
        self.__description_value_lab.configure(text=item.item.descriptions[0].value)

    def run_view(self):
        self.__root.mainloop()
