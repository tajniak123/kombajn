import threading


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
        main_loop = threading.Thread(target=self.__model.initialise_downloading_data)
        main_loop.daemon = True
        main_loop.start()
