from typing import Any
from discord.ui import View
from discord.ui.item import Item

class View(View):
    def __init__(self):
        super().__init__()
    
    def add_items(self, *items: Item[Any]):
        for item in items:
            super().add_item(item)
        return self