import time
import threading
from strings import KEY_VALUES, KEY_TIME


class Controller:
    def __init__(self, model, view):
        self.__model = model
        self.__view = view

        main_loop = threading.Thread(target=self.initialise_downloading_data)
        main_loop.daemon = True
        main_loop.start()

        self.__view.run_view()

    @property
    def model(self):
        return self.__model

    @property
    def view(self):
        return self.__view

    def initialise_downloading_data(self):
        self.__view.print_line()
        database = self.__model.database
        start_time = time.time()

        for i in range(len(database)):
            app_name = database.iloc[i, 0]
            self.__view.print_title(i+1, app_name)

            searching_result = self.__model.download_CVE_from_NIST(app_name)
            self.__view.print_CVE(searching_result.get(KEY_VALUES), searching_result.get(KEY_TIME))

        end_time = time.time()
        self.__view.print_seconds(end_time-start_time)
