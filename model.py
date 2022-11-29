import nvdlib
import pandas
import time
from colorama import Fore
from colorama import Style
from strings import (RESULTS_NOT_FOUND,
                     DATABASE_FILE_NAME,
                     NIST_KEY,
                     NIST_KEYWORD_SEARCH,
                     SEVERITY_CRITICAL,
                     SEVERITY_HIGH,
                     SEVERITY_MEDIUM,
                     SEVERITY_LOW)


class Model:
    severity_to_colors_converter = {
            SEVERITY_CRITICAL: Fore.LIGHTRED_EX,
            SEVERITY_HIGH: Fore.RED,
            SEVERITY_MEDIUM: Fore.YELLOW,
            SEVERITY_LOW: Fore.GREEN,
            None: Fore.MAGENTA
        }

    def __init__(self):
        start_time = time.time()

        print(50 * "=")
        database = pandas.read_excel(DATABASE_FILE_NAME, usecols=[0])

        a = nvdlib.searchCVE(keywordSearch=NIST_KEYWORD_SEARCH, key=NIST_KEY)
        counter = 1

        for i in range(len(database)):
            start_time1 = time.time()

            print(f'{counter}. {database.iloc[i, 0]}')

            a = nvdlib.searchCVE(keywordSearch=database.iloc[i, 0], key=NIST_KEY)
            if len(a) == 0:
                print(f'{Fore.RED}{RESULTS_NOT_FOUND}{Style.RESET_ALL}')
            else:
                for j in a:
                    id_s = f'{Fore.BLUE}{j.id}{Style.RESET_ALL}'
                    score_s = f'score={j.score[1]}'
                    severity_color = self.severity_to_colors_converter[j.score[2]]
                    scores_s = f'severity={severity_color}{j.score[2]}{Style.RESET_ALL}'

                    print(f'{id_s} {score_s}\t\t{scores_s}')

            counter += 1
            end_time1 = time.time()

            print("--- %s seconds ---" % round(end_time1 - start_time1, 2))
            print(50 * "=")

        end_time = time.time()
        print("--- %s seconds ---" % (end_time - start_time))
