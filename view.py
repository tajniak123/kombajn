import tkinter

from strings import (
                     FILE_NOT_FOUND,
                     DATABASE_FILE_NAME,
                     START_DOWNLOADING,
                     STOP_DOWNLOADING,
                     DESCRIPTIONS,
                     SEVERITY_CRITICAL,
                     SEVERITY_HIGH,
                     SEVERITY_MEDIUM,
                     SEVERITY_LOW,
                     SEVERITY,
                     SCORE
                     )
from colorama import Fore
from tkinter import (
        Tk,
        Text,
        Label,
        BOTH,
        LEFT,
        RIGHT,
        Y, W, N, E, S,
        LabelFrame,
        Button,
        ttk,
        HORIZONTAL,
        Frame,
        messagebox
        )
from values import (
        DEFAULT_APP_HEIGHT,
        DEFAULT_APP_WIDTH,
        DETAIL_FRAME_HEIGHT,
        DETAIL_FRAME_WIDTH,
        )

from colors import (
        BLACK_BG,
        RED_BG,
        ORANGE_BG,
        YELLOW_BG,
        WHITE_FG,
        BLACK_FG,
        )


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
            SEVERITY_LOW: Fore.YELLOW,
            None: Fore.MAGENTA
        }
        self.__root = Tk()
        self.__root.geometry(self.__window_size)
        self.__root.resizable(False, False)

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
                length=DEFAULT_APP_WIDTH,
                mode='determinate',
                )

        self.__left_frame = Frame(self.__root)
        self.__treeview = ttk.Treeview(self.__left_frame)
        self.__treeview.heading('#0', text='Aplikacje', anchor=W)
        self.__treeview.bind("<Double-1>", self.on_click_listbox_item)

        self.__details_frame = LabelFrame(
                self.__root,
                width=DETAIL_FRAME_WIDTH,
                height=DETAIL_FRAME_HEIGHT,
                )

        self.__severity_frame = Frame(self.__details_frame)
        self.__severity_lab = Label(self.__severity_frame, text=SEVERITY)
        self.__severity_value_lab = Label(self.__severity_frame)
        self.__score_frame = Frame(self.__details_frame)
        self.__score_lab = Label(self.__score_frame, text=SCORE)
        self.__score_value_lab = Label(self.__score_frame)

        self.__description_frame = Frame(self.__details_frame)
        self.__description_lab = Label(
                self.__description_frame,
                text=DESCRIPTIONS
                )
        self.__description_value_lab = Label(
                self.__description_frame,
                width=DETAIL_FRAME_WIDTH,
                wraplength=DETAIL_FRAME_WIDTH,
                )

        self.__pack_items()

    def __pack_items(self):
        self.__top_frame.pack(anchor=N)
        self.__download_button.pack()

        self.__left_frame.pack(fill=Y, expand=True, side=LEFT, anchor=W)
        self.__treeview.pack(fill=Y, expand=True)

        self.__details_frame.pack(fill=BOTH, side=RIGHT)
        self.__description_frame.pack(ipadx=4, ipady=4)
        self.__description_lab.pack()
        self.__description_value_lab.pack()
        self.__severity_frame.pack(side=RIGHT, anchor=S, ipadx=4, ipady=4)
        self.__severity_lab.pack()
        self.__severity_value_lab.pack()
        self.__score_frame.pack(side=LEFT, anchor=S, ipadx=4, ipady=4)
        self.__score_lab.pack()
        self.__score_value_lab.pack()

    def switch_progressbar_visibility(self, is_visible):
        if is_visible:
            self.__download_frame.pack()
            self.__current_app_downloading_label.pack(
                    side=LEFT,
                    anchor=W,
                    ipadx=4,
                    )
            self.__position_downloading_label.pack(
                    side=RIGHT,
                    anchor=E,
                    ipadx=4
                    )
            self.__downloading_pb.pack()
            self.__stop_dowload_button.pack()
            self.__download_button.forget()
        else:
            self.__download_frame.forget()
            self.__stop_dowload_button.forget()
            self.__download_button.pack()

    def error_message_box(self):
        messagebox.showerror(
                title=FILE_NOT_FOUND,
                message=f'{FILE_NOT_FOUND} {DATABASE_FILE_NAME}'
                )

    def on_click_listbox_item(self, event):
        item = self.__treeview.identify('item', event.x, event.y)
        if item:
            self.update_values(int(item))

    def update_values(self, index):
        item = self.__model.values[index]
        self.__details_frame.configure(text=item.app_name)
        if item.item.score[1] >= 9:
            self.__score_value_lab.configure(text=item.item.score[1], bg=BLACK_BG, fg=WHITE_FG)
            self.__severity_value_lab.configure(text=item.item.score[2], bg=BLACK_BG, fg=WHITE_FG)
        elif item.item.score[1] >= 7 and item.item.score[1] < 9:
            self.__score_value_lab.configure(text=item.item.score[1], bg=RED_BG, fg=WHITE_FG)
            self.__severity_value_lab.configure(text=item.item.score[2], bg=RED_BG, fg=WHITE_FG)
        elif item.item.score[1] >= 4 and item.item.score[1] < 7:
            self.__score_value_lab.configure(text=item.item.score[1], bg=ORANGE_BG, fg=BLACK_FG)
            self.__severity_value_lab.configure(text=item.item.score[2], bg=ORANGE_BG, fg=BLACK_FG)
        elif item.item.score[1] > 0 and item.item.score[1] < 4:
            self.__score_value_lab.configure(text=item.item.score[1], bg=YELLOW_BG, fg=BLACK_FG)
            self.__severity_value_lab.configure(text=item.item.score[2], bg=YELLOW_BG, fg=BLACK_FG)
        self.__description_value_lab.configure(
                text=item.item.descriptions[0].value, justify='center')

    def add_item_to_list(self, APP_name, id):
        self.__treeview.insert('', 'end', text=APP_name, iid=id, open=False)

    def move(self, idITEM, idAPP, idCVE):
        self.__treeview.move(idITEM, idAPP, idCVE)

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

    def run_view(self):
        self.__root.mainloop()
