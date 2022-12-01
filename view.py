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
from tkinter import Tk, Listbox, Label, BOTH, LEFT, RIGHT, Y, W, LabelFrame
from values import DEFAULT_APP_HEIGHT, DEFAULT_APP_WIDTH


class View:
    def __init__(self):
        self.__window_width = DEFAULT_APP_WIDTH
        self.__window_height = DEFAULT_APP_HEIGHT
        self.__window_size = f'{self.__window_width}x{self.__window_height}'
        self.__values = {}
        self.__severity_to_colors_converter = {
            SEVERITY_CRITICAL: Fore.LIGHTRED_EX,
            SEVERITY_HIGH: Fore.RED,
            SEVERITY_MEDIUM: Fore.YELLOW,
            SEVERITY_LOW: Fore.GREEN,
            None: Fore.MAGENTA
        }
        self.__root = Tk()
        self.__root.geometry(self.__window_size)

        self.__listbox = Listbox(self.__root,
                           height = 25,
                           width = 15,
                           activestyle = 'dotbox')

        self.__frame = LabelFrame(self.__root, text="dane")

        self.__label = Label(self.__frame, text="Elo")

        self.__listbox.pack(fill=Y, expand=True, side=LEFT, anchor=W)
        self.__frame.pack(fill=BOTH, expand=True, side=RIGHT)
        self.__label.pack(fill=BOTH, expand=True)

    def run_view(self):
        self.__root.mainloop()

    def print_title(self, item_id, name):
        print(f'{item_id}. {name}')

    def print_line(self):
        print(50 * "=")

    def print_seconds(self, time):
        print(f'--- %s {SECONDS} ---' % round(time, 2))

    def print_CVE(self, cve_list, downloading_time, app_name):
        if len(cve_list) == 0:
            print(f'{Fore.RED}{RESULTS_NOT_FOUND}{Style.RESET_ALL}')
        else:
            i = 1
            for cve in cve_list:
                print(cve)
                #tu na razie ten dzial dodawacz, ale trzeba zrobic tego z dolu
                self.__listbox.insert(i, cve.id)
                id_s = f'{Fore.BLUE}{cve.id}{Style.RESET_ALL}'
                score = cve.score[1]
                vernulability_lvl = cve.score[2]
                score_s = f'{SCORE} = {score}'
                severity_color = self.__severity_to_colors_converter[vernulability_lvl]
                scores_s = f'{SEVERITY} = {severity_color}{vernulability_lvl}{Style.RESET_ALL}'
                i += 1
                print(f'{id_s} {score_s}\t\t{scores_s}')
                print(f'{(cve.descriptions[0].value)}')

        self.print_seconds(downloading_time)
        self.print_line()

    def add_cves(self, app_name, cve_list):
        if len(cve_list) > 0:
            i = 1
            for cve in cve_list:
                self.__listbox.insert(i, cve.id)
                values[app_name] = {
                        cve.id:
                        {
                            "score": cve.score[1],
                            "severity" = cve.score[2],
                            "descriptions" = cve.descriptions[0].value,
                        }
                    }


                i += 1
