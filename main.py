from distutils.command.build import build
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
from kivy.uix.gridlayout import GridLayout

from kivy.properties import StringProperty
from kivy.properties import NumericProperty
from kivy.properties import ColorProperty

#include programclasses

from Libs.programclass.Screens.BookScreen import BooksScreen
from Libs.programclass.Screens.EdittingScreen import EdittingScreen
from Libs.programclass.Screens.InternalMenuBookScreen import InternalMenuBookScreen
from Libs.programclass.Screens.MenuScreen import MenuScreen
from Libs.programclass.Screens.StatisticScreen import StatisticScreen
from Libs.programclass.modules.CustomBottomNavigation import CustomBottomNavigation
from Libs.programclass.modules.CustomList import CustomList
from Libs.programclass.modules.WordsList import WordsList

#from Libs.uix.kv import ScreenManagerKV,MenuScreen, EdittingScreen,BooksScreen,StatisticScreen




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




    def build(self):
        Builder.load_file("Libs//uix//kv//ScreenManagerKV.kv")
        Builder.load_file("Libs//uix//kv//MenuScreen.kv")
        Builder.load_file("Libs//uix//kv//StatisticScreen.kv")
        Builder.load_file("Libs//uix//kv//BooksScreen.kv")
        Builder.load_file("Libs//uix//kv//EdittingScreen.kv")
        Builder.load_file("Libs//uix//kv//InternalMenuBookScreen.kv")
        sm = ScreenManager()

        Builder.load_file("Libs//uix//kv//modules//CustomBottomNavigation.kv")
        Builder.load_file("Libs//uix//kv//modules//CustomList.kv")
        Builder.load_file("Libs//uix//kv//modules//WordsList.kv")
        self.screens = ['menu','statistic','books','edit','bookInternal']

        sm.add_widget(MenuScreen(name="menu"))
        sm.add_widget(StatisticScreen(name="statistic"))
        sm.add_widget(EdittingScreen(name="edit"))
        sm.add_widget(BooksScreen(name="books"))
        sm.add_widget(InternalMenuBookScreen(name="bookInternal"))
        return sm  


    #START FOR zone with swap and bind internal book screen
    def swap_screen(self,screen_name_index,*name_book):
        screen_name = self.screens
        setattr(self.root,"current" ,screen_name[int(screen_name_index[0])-1])
        if screen_name_index[0] == '5':
            self.clear_internal_screen()
            self.load_words(name_book)

        pprint("[Log   ]"f"@{self.screen_is_displayed}"+" >> "+f"@{screen_name[int(screen_name_index[0])-1]}")
        self.screen_is_displayed = screen_name[int(screen_name_index[0])-1]


    def clear_internal_screen(self):
        ob = self.root.get_screen("bookInternal").ids.list_view
        ob.remove_widget(ob.children[0])
        ob.add_widget(WordsList())


    def add_word_into_internal(self,word):

        but = CustomList()
        but.Label_menu_texts['word'] = word[0]
        but.Label_menu_texts['translate'] = word[2]
        swap_color = ColorProperty("lightslategrey")


        if word[1] != None and word[1] !='':
            but.Label_menu_texts['transcription'] = word[1]

        but.Label_menu_texts['status'] = str(word[4])

        if word[3] != None and word[1] != '':
            but.Label_menu_texts['asociations'] = word[3]

        self.root.get_screen("bookInternal").ids.list_view.children[0].add_widget(but)

    # check data base if exist table also like into Book screen funck
    def is_tabele_with_name(self,name):
        conn = sqlite3.connect("Data/Base/Books.db")
        cursor = conn.cursor()
        for item in cursor.execute("SELECT db_name FROM Data_name_of_books").fetchall():
            if name == item:
                conn.close()
                return True
            else:
                continue

        conn.close()
        return False


    def build_screen(self,data):
        for word in data:
            self.add_word_into_internal(word)

    # start algortitm for loading words > build_screen > add_word_into_internal > (get screen with words list)
    def load_words(self, table_name):
        if self.is_tabele_with_name(table_name):
            conn = sqlite3.connect("Data/Base/Books.db")
            cursor = conn.cursor()
            print(table_name[0])
            data = cursor.execute("SELECT * FROM " + '\''+table_name[0]+'\'')
            data = data.fetchall()
            conn.close()
            self.build_screen(data)
    #END FOR  zone with swap and bind internal book screen

    #START FOR zone where loading new book
    def del_book_func(self,bookName,wd_for_del):
        conn = sqlite3.connect("Data/Base/Books.db")
        cursor = conn.cursor()
        cursor.execute("DELETE FROM 'Data_name_of_books' WHERE db_name=?",[bookName])
        cursor.execute("DROP TABLE IF EXISTS '{}'".format(bookName)) 
        conn.commit()
        conn.close()
        self.root.get_screen("books").ids.books_add_list.remove_widget(wd_for_del)


    def load_books(self):
        if self.load_books_triger == False:
            new_book_word_number = 0
            new_book_name = ''
            self.create_data_base()
            data = self.get_infor_from_db()
            for book in data:
                new_book_name = book[0]
                new_book_word_number = book[1]
                self.add_book_func(new_book_name,new_book_word_number)
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


    def add_book_func(self, new_book_name,new_book_word_number):   
        but = ThreeLineAvatarIconListItem(
            text="{}".format( new_book_name ),
            secondary_text="{} words in it".format( new_book_word_number ),
            on_release= lambda x: self.swap_screen(('5'),new_book_name)
        )
        del_item = IconLeftWidget(
            icon="delete",
            on_release= lambda x,y = new_book_name,z = but: self.del_book_func(y,z)
        )
        edit_item= IconRightWidget(
            icon="book-edit",
            on_release= lambda x: self.edit_menu
        )
        but.add_widget(del_item)
        but.add_widget(edit_item)
        self.root.get_screen("books").ids.books_add_list.add_widget(but)

    #END FOR zone where loading new book

if __name__ == '__main__':
    Main().run()