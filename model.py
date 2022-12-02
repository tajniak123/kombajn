import pandas
from strings import KEY_VALUES, KEY_TIME
import time
from nvdlib import searchCVE
from strings import DATABASE_FILE_NAME, NIST_KEY


class Model:
    def __init__(self):
        self.__database = pandas.read_excel(DATABASE_FILE_NAME)
        self.__values = {}

    @property
    def database(self):
        return self.__database

    @property
    def values(self):
        return self.__values

    def download_CVE_from_NIST(self, name):
        start_time = time.time()
        answer_from_nist = searchCVE(keywordSearch=name, key=NIST_KEY)
        end_time = time.time()
        return {KEY_TIME: (end_time-start_time),
                KEY_VALUES: answer_from_nist}

    def initialise_downloading_data(self):
        start_time = time.time()
        print(self.__database)
        for i in range(len(self.__database)):
            app_name = self.__database.iloc[i, 0]
            searching_result = self.download_CVE_from_NIST(app_name)
            self.__values[app_name].append(searching_result)

        end_time = time.time()
        print(end_time-start_time)
