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


class View:
    def __init__(self):
        self.__severity_to_colors_converter = {
            SEVERITY_CRITICAL: Fore.LIGHTRED_EX,
            SEVERITY_HIGH: Fore.RED,
            SEVERITY_MEDIUM: Fore.YELLOW,
            SEVERITY_LOW: Fore.GREEN,
            None: Fore.MAGENTA
        }

    def print_title(self, item_id, name):
        print(f'{item_id}. {name}')

    def print_line(self):
        print(50 * "=")

    def print_seconds(self, time):
        print(f'--- %s {SECONDS} ---' % round(time, 2))

    def print_CVE(self, cve_list, downloading_time):
        if len(cve_list) == 0:
            print(f'{Fore.RED}{RESULTS_NOT_FOUND}{Style.RESET_ALL}')
        else:
            for cve in cve_list:
                id_s = f'{Fore.BLUE}{cve.id}{Style.RESET_ALL}'
                score = cve.score[1]
                vernulability_lvl = cve.score[2]
                score_s = f'{SCORE} = {score}'
                severity_color = self.__severity_to_colors_converter[vernulability_lvl]
                scores_s = f'{SEVERITY} = {severity_color}{vernulability_lvl}{Style.RESET_ALL}'

                print(f'{id_s} {score_s}\t\t{scores_s}')

        self.print_seconds(downloading_time)
        self.print_line()
