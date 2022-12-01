from controller import Controller
from view import View
from model import Model

if __name__ == "__main__":
    model = Model()
    view = View(model)
    controller = Controller(model, view)
