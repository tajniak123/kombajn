import threading
import time
from strings import KEY_VALUES
from item_model import ItemModel


class Controller:
    def __init__(self, model, view):
        self.__is_downloading_in_progress = False
        self.__model = model
        self.__view = view
        self.__view.set_download_function(self.download_data)
        self.__view.set_stop_downloading_function(self.stop_downloading)
        self.__view.run_view()
        self.__downloading_loop = None

    @property
    def model(self):
        return self.__model

    @property
    def view(self):
        return self.__view

    def download_data(self):
        self.__downloading_loop = threading.Thread(
                target=self.initialise_downloading_data)
        self.__downloading_loop.daemon = True
        self.__downloading_loop.start()

    def stop_downloading(self):
        self.__is_downloading_in_progress = False
        self.__view.set_stop_button_enabled()

    def initialise_downloading_data(self):
        self.__is_downloading_in_progress = True
        self.__view.switch_progressbar_visibility(True)
        start_time = time.time()

        if self.__model.database is None:
            self.__view.error_message_box()
        else:
            for i in range(len(self.__model.database)):
                if self.__is_downloading_in_progress:
                    app_name = self.__model.database.iloc[i, 0]
                    self.__view.update_download_notifications(
                            app_name, f'{i}/{len(self.__model.database)}')
                    searching_result = self.__model.download_CVE_from_NIST(app_name)

                    for cve in searching_result[KEY_VALUES]:
                        item = ItemModel(
                                item_id=len(self.__model.values),
                                app_name=app_name,
                                item=cve
                                )
                        self.__model.values.append(item)
                        self.__view.add_item_to_list(item.item.id)

                    self.__view.update_progressbar()
                else:
                    break

        end_time = time.time()
        self.__view.switch_progressbar_visibility(False)
        print(end_time-start_time)
        self.__view.set_stop_button_normal()
        self.__view.reset_progressbar()
