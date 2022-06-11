from logging import root
from re import X
import sqlite3

from pprint import pprint
from tkinter.messagebox import NO
from kivymd.app import MDApp
from kivymd.uix.list import ThreeLineAvatarIconListItem,IconLeftWidget,IconRightWidget
from kivy.lang.builder import Builder
from kivymd.uix.button import MDFlatButton
from kivymd.uix.textfield import MDTextField

from kivy.clock import Clock
Clock.max_iteration = 30


from kivy.uix.boxlayout import BoxLayout
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.popup import Popup

from kivy.properties import StringProperty
from kivy.properties import NumericProperty

#include programclasses

from Libs.programclass.Screens.BookScreen import BooksScreen
from Libs.programclass.Screens.EdittingScreen import EdittingScreen
from Libs.programclass.Screens.InternalMenuBookScreen import InternalMenuBookScreen
from Libs.programclass.Screens.MenuScreen import MenuScreen
from Libs.programclass.Screens.StatisticScreen import StatisticScreen
from Libs.programclass.modules.custom_bottom_navigation import custom_bottom_navigation

#from Libs.uix.kv import ScreenManagerKV,MenuScreen, EdittingScreen,BooksScreen,StatisticScreen

class Dialog_book_add(Widget):
    pass


class Main(MDApp):
    load_books_triger = False
    screen_is_displayed = "menu"
    sql_executes = ["""
            CREATE TABLE IF NOT EXISTS 'Data_name_of_books' (
                "db_name"	TEXT NOT NULL UNIQUE,
                "size"	INTEGER NOT NULL );""",
            """
            SELECT db_name,size FROM Data_name_of_books
            """
            ]

    icon_button_top_menu_size = StringProperty("32sp")
    icon_button_bot_menu_size = StringProperty("34sp")
    icon_main_menu_size = StringProperty("42sp")

    

    def swap_screen(self,*screen_name_index):
        screen_name = ['menu','statistic','books','edit'] 
        setattr(self.root,"current" ,screen_name[int(screen_name_index[0])-1])
        pprint("[Log   ]"f"@{self.screen_is_displayed}"+" >> "+f"@{screen_name[int(screen_name_index[0])-1]}")
        self.screen_is_displayed = screen_name[int(screen_name_index[0])-1]

    def del_book_func(self,bookName,wd_for_del):
        conn = sqlite3.connect("Data/Base/Books.db")
        cursor = conn.cursor()
        cursor.execute("DELETE FROM 'Data_name_of_books' WHERE db_name=?",[bookName])
        cursor.execute("DROP TABLE IF EXISTS {}".format(bookName)) 
        conn.commit()
        conn.close()
        self.root.get_screen("books").ids.books_add_list.remove_widget(wd_for_del)


    def load_books(self):
        if self.load_books_triger == False:
            self.new_book_word_number = 0
            self.new_book_name = ''
            self.create_data_base()
            data = self.get_infor_from_db()
            for book in data:
                self.new_book_name = book[0]
                self.new_book_word_number = book[1]
                self.add_book_func()
            pprint(data)
            self.load_books_triger = True
        else:
            pass


    def get_infor_from_db(self):
        conn = sqlite3.connect("Data/Base/Books.db")
        cursor = conn.cursor()
        data = cursor.execute(self.sql_executes[1]).fetchall()
        conn.close()
        return data


    def create_data_base(self):
        conn = sqlite3.connect("Data/Base/Books.db")
        cursor = conn.cursor()
        cursor.execute(self.sql_executes[0])
        conn.close()


    def edit_menu(self):
        pass


    def add_book_func(self, *arg):   

        but = ThreeLineAvatarIconListItem(
            text="{}".format( self.new_book_name ),
            secondary_text="{} words in it".format( self.new_book_word_number ),
            on_release= lambda x: self.swap_to_internal_book_screen()
        )

        del_item = IconLeftWidget(
            icon="delete",
            on_release= lambda x,y = self.new_book_name,z = but: self.del_book_func(y,z)
        )
        
        edit_item= IconRightWidget(
            icon="book-edit",
            on_release= lambda x: self.edit_menu
        )

        but.add_widget(del_item)
        but.add_widget(edit_item)
        self.root.get_screen("books").ids.books_add_list.add_widget(but)


    def build(self):
        Builder.load_file("Libs//uix//kv//ScreenManagerKV.kv")
        Builder.load_file("Libs//uix//kv//MenuScreen.kv")
        Builder.load_file("Libs//uix//kv//StatisticScreen.kv")
        Builder.load_file("Libs//uix//kv//BooksScreen.kv")
        Builder.load_file("Libs//uix//kv//EdittingScreen.kv")
        sm = ScreenManager()

        Builder.load_file("Libs//uix//kv//modules//custom_bottom_navigation.kv")

        sm.add_widget(MenuScreen(name="menu"))
        sm.add_widget(StatisticScreen(name="statistic"))
        sm.add_widget(EdittingScreen(name="edit"))
        sm.add_widget(BooksScreen(name="books"))

        return sm


if __name__ == '__main__':
    Main().run()