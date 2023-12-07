from typing import List, Tuple, Set


class ItemGridModel:
    name: str = None
    data: List[Set[Tuple[int, int]]] = None
    grid_count: int = None
    row: int = None
    column: int = None
    image_url: str = None

    def __init__(self, name=None, data=None, grid_count=None, row=None, column=None, image_url=None):
        self.name = name
        self.data = data
        self.grid_count = grid_count
        self.row = row
        self.column = column
        self.image_url = image_url

    def update_data(self, name=None, data: List = None, grid_count=None, row=None, column=None, image_url=None):
        if name:
            self.name = name
        if data:
            self.data = data
        if grid_count:
            self.grid_count = grid_count
        if row:
            self.row = row
        if column:
            self.column = column
        if image_url:
            self.image_url = image_url
