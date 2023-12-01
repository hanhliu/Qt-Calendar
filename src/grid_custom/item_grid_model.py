from typing import List


class ItemGridModel:
    name: str = None
    data: List = None
    grid_size: int = None

    def __init__(self, name=None, data=None, grid_size=None):
        self.name = name
        self.data = data
        self.grid_size = grid_size

    def update_data(self, name=None, data: List = None, grid_size=None):
        if name:
            self.name = name
        if data:
            self.data = data
        if grid_size:
            self.grid_size = grid_size