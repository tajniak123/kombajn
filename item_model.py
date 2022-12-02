class ItemModel:
    def __init__(self, item_id=0, app_name='', item=None):
        self.__item_id = item_id
        self.__app_name = app_name
        self.__item = item

    @property
    def item_id(self):
        return self.__item_id

    @property
    def app_name(self):
        return self.__app_name

    @property
    def item(self):
        return self.__item
