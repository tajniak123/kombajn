import pandas
import time
from nvdlib import searchCVE
from strings import DATABASE_FILE_NAME, NIST_KEY, KEY_VALUES, KEY_TIME


class Model:
    def __init__(self):
        self.__database = self.get_database()

    @property
    def database(self):
        return self.__database

    def get_database(self):
        return pandas.read_excel(DATABASE_FILE_NAME, usecols=[0])

    def download_CVE_from_NIST(self, name):
        start_time = time.time()
        answer_from_nist = searchCVE(keywordSearch=name, key=NIST_KEY)
        end_time = time.time()
        return {KEY_TIME: (end_time-start_time),
                KEY_VALUES: answer_from_nist}
