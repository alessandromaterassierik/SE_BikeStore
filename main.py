import flet as ft

from model.model import Model
from UI.view import View
from UI.controller import Controller
from UI.alert import AlertManager

def main(page: ft.Page):
    my_model = Model()
    my_view = View(page)
    my_alert = AlertManager(page)
    my_controller = Controller(my_view, my_model, my_alert)
    my_view.set_controller(my_controller)
    my_view.load_interface()


ft.app(target=main)
