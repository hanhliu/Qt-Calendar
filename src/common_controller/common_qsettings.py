from PySide6.QtCore import QSettings

from src.grid_custom.item_grid_model import ItemGridModel


class CommonQSettings:
    __instance = None

    def __init__(self):
        self.settings = QSettings("GPS", "Common Settings")

    @staticmethod
    def get_instance():
        if CommonQSettings.__instance is None:
            CommonQSettings.__instance = CommonQSettings()
        return CommonQSettings.__instance

    def save_data_grid(self, data):
        self.settings.setValue("data_grid", data)

    def get_data_grid(self):
        if self.settings.contains("data_grid"):
            list_data_grid = self.settings.value("data_grid")
        else:
            list_data_grid = [
                ItemGridModel(name=f"6 Divisions", data=[{(0, 1), (1, 0), (1, 1), (0, 0)}], row=3, column=3,
                              grid_count=6),
                ItemGridModel(name=f"8 Divisions",
                              data=[{(0, 1), (1, 2), (2, 1), (0, 0), (1, 1), (2, 0), (0, 2), (2, 2), (1, 0)}], row=4,
                              column=4, grid_count=8),
                ItemGridModel(name=f"10 Divisions",
                              data=[{(0, 1), (1, 0), (1, 1), (0, 0)}, {(1, 2), (0, 2), (0, 3), (1, 3)}], row=4,
                              column=4,
                              grid_count=10),
                ItemGridModel(name=f"13 Divisions", data=[{(1, 1), (1, 2), (2, 1), (2, 2)}], row=4, column=4,
                              grid_count=13)
            ]
        return list_data_grid

    def clear_all(self):
        self.settings.clear()
