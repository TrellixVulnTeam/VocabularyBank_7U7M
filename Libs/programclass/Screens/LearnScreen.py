from kivymd.uix.menu import MDDropdownMenu

from kivy.uix.screenmanager import Screen

from kivy.properties import StringProperty

import sqlite3


class LearnScreen(Screen):
    back_button_size = StringProperty("36sp")
    ragime_name = ""



    def get_book_from_db(self):
        get_execute = "SELECT * FROM 'Data_name_of_books'"
        conn = sqlite3.connect("Data/Base/Books.db")
        cursor = conn.cursor()
        data_db = cursor.execute(get_execute)
        return data_db.fetchall()


    def menu_start(self):
        book_items = self.get_book_from_db()
        menu_items = [
            {
                "text": f"\"{item[0]}\"  words number {item[1]} ",
                "viewclass": "OneLineListItem",
                "on_release": lambda x=f"{item[0]}": self.menu_callback(x),
            } for item in book_items
            ]
        self.menu = MDDropdownMenu(
            caller=self.ids.menu,
            items=menu_items,
            width_mult=4,
            radius=[6, 6, 6, 6],
            position="bottom",
            ver_growth="up",
            hor_growth="right"
        )

        self.menu.open()
    

    def menu_callback(self, book_name):
        self.ids.menu.text = book_name
        self.menu.dismiss()