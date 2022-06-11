from kivy.uix.screenmanager import Screen
from kivy.properties import StringProperty


class InternalMenuBookScreen(Screen):
    icon_button_pluss_size = StringProperty("42sp")
    icon_filter_size = StringProperty("30sp")
    icon_search_size = StringProperty("30sp")
    font_size_search_field = StringProperty("26sp")