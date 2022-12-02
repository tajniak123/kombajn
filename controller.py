import threading
import time
from strings import KEY_VALUES
from item_model import ItemModel


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
        self.__view.set_visible_downloading_details(True)
        start_time = time.time()
        for i in range(len(self.__model.database)):
            app_name = self.__model.database.iloc[i, 0]
            self.__view.update_download_notifications(app_name, f'{i}/{len(self.__model.database)}')
            searching_result = self.__model.download_CVE_from_NIST(app_name)

            for cve in searching_result[KEY_VALUES]:
                item = ItemModel(item_id=len(self.__model.values), app_name=app_name, item=cve)
                self.__model.values.append(item)
                self.__view.add_item_to_list(item.item.id)

            self.__view.update_progressbar()

        end_time = time.time()
        self.__view.set_visible_downloading_details(False)
        print(end_time-start_time)
