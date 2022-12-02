import threading
import time
from strings import KEY_VALUES


class Controller:
    def __init__(self, model, view):
        self.__model = model
        self.__view = view
        self.__view.set_download_function(self.download_data)
        self.__view.run_view()

    @property
    def model(self):
        return self.__model

    @property
    def view(self):
        return self.__view

    def download_data(self):
        main_loop = threading.Thread(target=self.initialise_downloading_data)
        main_loop.daemon = True
        main_loop.start()

    def initialise_downloading_data(self):
        start_time = time.time()
        for i in range(len(self.__model.database)):
            app_name = self.__model.database.iloc[i, 0]
            searching_result = self.__model.download_CVE_from_NIST(app_name)
            if self.__model.values.get(app_name) is None:
                self.__model.values[app_name] = []
                self.__model.values[app_name].append(searching_result)
            else:
                self.__model.values[app_name].append(searching_result)

            print(searching_result[KEY_VALUES])

        end_time = time.time()
        print(end_time-start_time)
