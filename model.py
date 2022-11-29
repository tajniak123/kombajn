import nvdlib
import pandas
import time
from colorama import Fore
from colorama import Style
import os

class Model:
    def __init__(self):


        # os.system('python -m pip install --upgrade pip setuptools virtualenv')
        #os.system('pip install pyqt5')
        #SZABAraaa

        start_time = time.time()

        print(50 * "=")
        plik = pandas.read_excel('Zeszyt1.xlsx', usecols=[0])

        a = nvdlib.searchCVE(keywordSearch='oneconnect', key='2b1f6592-3b28-43f6-819e-8b0281c3dc1c')

        colorDict = {
            "CRITICAL": Fore.LIGHTRED_EX,
            "HIGH": Fore.RED,
            "MEDIUM": Fore.YELLOW,
            "LOW": Fore.GREEN,
            None: Fore.MAGENTA
        }

        c = 1

        for i in range(len(plik)):
            start_time1 = time.time()
            print(f'{c}. {plik.iloc[i, 0]}')
            a = nvdlib.searchCVE(keywordSearch=plik.iloc[i, 0], key='2b1f6592-3b28-43f6-819e-8b0281c3dc1c')
            if len(a) == 0:
                print(f'{Fore.RED}Nie znaleziono wyników{Style.RESET_ALL}')
            else:
                for j in a:
                    print(
                        f'{Fore.BLUE} {j.id} {Style.RESET_ALL} score={j.score[1]} severity={colorDict[j.score[2]]}{j.score[2]} {Style.RESET_ALL}')

            c += 1
            end_time1 = time.time()
            print("--- %s seconds ---" % round(end_time1 - start_time1, 2))
            print(50 * "=")

        end_time = time.time()
        print("--- %s seconds ---" % (end_time - start_time))

        plik = pandas.read_excel('Zeszyt1.xlsx', usecols=[0])