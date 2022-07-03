from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.list import OneLineListItem


class CustomMenu(MDDropdownMenu):
    pass


class MenuElement(OneLineListItem):
    def __init__(self, **kwargs):
        super(MenuElement, self).__init__(**kwargs)
        self.ids._lbl_primary.halign = "center"