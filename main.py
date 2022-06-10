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

#from Libs.uix.kv import ScreenManagerKV,MenuScreen, EdittingScreen,BooksScreen,StatisticScreen

class Dialog_book_add(Widget):
    pass


class MainAPP(Screen):
    def add(self):
        self.new_button = Button(text=str(1))
        self.ids.books_add_list.add_widget(self.new_button)
        pprint(self.children[1].children[1].children)
        pprint( self.ids.books_add_list.children)


class MenuScreen(Screen):

    pass


class StatisticScreen(Screen):
    pass


class Book(Widget):
    name = StringProperty("kill me pls")


class BooksScreen(Screen):
    #root variable
    icon_button_pluss_size = StringProperty("42sp")
    icon_filter_size = StringProperty("30sp")
    icon_search_size = StringProperty("30sp")
    font_size_search_field = StringProperty("26sp")
    table_creator = [
            """CREATE TABLE IF NOT EXISTS '' (
                "word"	TEXT NOT NULL UNIQUE,
                "transcription"	TEXT,
                "translate" TEXT NOT NULL UNIQUE,
                "association" TEXT,
                "status" INTEGER NOT NULL,
                "index"	INTEGER NOT NULL UNIQUE,
                PRIMARY KEY("index" AUTOINCREMENT)
            );""",
            """INSERT INTO 'Data_name_of_books' VALUES (?,?)"""
            ]

    def cancel(self, *arg):
        self.NewDialog.dismiss()
        pprint("cancel")

    def into_book_menu(self):
        pass

    def add_book_func(self, book):   
        but = ThreeLineAvatarIconListItem(
            text="{}".format( book[0] ),
            secondary_text="{} words in it".format( book[1] )
        )

        del_item = IconLeftWidget(
            icon="delete",
            on_release= lambda x,y = book[0],z = but: self.del_book_func(y,z)
            )

        edit_item= IconRightWidget(icon="book-edit")


        but.add_widget(del_item)
        but.add_widget(edit_item)
        self.ids.books_add_list.add_widget(but)


    def del_book_func(self,bookName,wd_for_del):
        conn = sqlite3.connect("Data/Base/Books.db")
        cursor = conn.cursor()
        cursor.execute("DELETE FROM 'Data_name_of_books' WHERE db_name=?",[bookName])
        cursor.execute("DROP TABLE IF EXISTS {}".format(bookName)) 
        conn.commit()
        conn.close()
        self.remove_widget(wd_for_del)



    def create_new_book_by_name(self,name):
        create_execute = self.table_creator[0][:28] + name + self.table_creator[0][28:]
        conn = sqlite3.connect("Data/Base/Books.db")
        cursor = conn.cursor()
        book = [name,0]

        cursor.execute(create_execute)
        cursor.execute(self.table_creator[1],(book[0],book[1]))
        conn.commit()
        self.add_book_func(book)
        conn.close()

    def create(self, *arg):
        # see is the text in poput -> textfield no empty
        if self.text_input.text == "":
            self.text_input.error = True
        else:
            self.create_new_book_by_name(self.text_input.text)
            self.NewDialog.dismiss()


    def add_book_dialog(self, *instance):
        self.NewDialog = Popup(
            title="Input a name of new dict",
            size_hint=(None,None),
            size=(400,300),
            auto_dismiss=False
        )
        main_box = BoxLayout(
            orientation="vertical",
            size_hint=(0.95,0.95)
        )
        in_main_box = BoxLayout(
            orientation="horizontal",
            size_hint=(0.9,0.4)
        )
        self.text_input = MDTextField(
            size_hint=(0.9,0.6),
            helper_text="Name is empty, please input or close",
            helper_text_mode="on_error",
        )

        close_but = MDFlatButton(
            size_hint=(0.4,0.45),
            text="CLOSE"
        )
        ok_but = MDFlatButton(
            size_hint=(0.4,0.45),
            text="OK"
        )
        close_but.bind(on_release=self.cancel)
        ok_but.bind(on_release=self.create)
        in_main_box.add_widget(ok_but)
        in_main_box.add_widget(close_but)
        main_box.add_widget(self.text_input)
        main_box.add_widget(in_main_box)

        self.NewDialog.add_widget(main_box)

        self.NewDialog.open()


class EdittingScreen(Screen):
    pass



class Main(MDApp):
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

    def del_book_func(self,bookName,wd_for_del):
        conn = sqlite3.connect("Data/Base/Books.db")
        cursor = conn.cursor()
        cursor.execute("DELETE FROM 'Data_name_of_books' WHERE db_name=?",[bookName])
        cursor.execute("DROP TABLE IF EXISTS {}".format(bookName)) 
        conn.commit()
        conn.close()
        self.root.get_screen("books").remove_widget(wd_for_del)

    def load_books(self):
        self.new_book_word_number = 0
        self.new_book_name = ''
        self.create_data_base()
        data = self.get_infor_from_db()
        for book in data:
            self.new_book_name = book[0]
            self.new_book_word_number = book[1]
            self.add_book_func()
        pprint(data)


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


    def add_book_func(self, *arg):   

        but = ThreeLineAvatarIconListItem(
            text="{}".format( self.new_book_name ),
            secondary_text="{} words in it".format( self.new_book_word_number )
        )
        del_item = IconLeftWidget(
            icon="delete",
            on_release= lambda x,y = self.new_book_name,z = but: self.del_book_func(y,z)
            )

        edit_item= IconRightWidget(icon="book-edit")


        but.add_widget(del_item)
        but.add_widget(edit_item)
        self.root.get_screen("books").ids.books_add_list.add_widget(but)


    def build(self):
        Builder.load_file("Libs//uix//kv//ScreenManagerKV.kv")
        Builder.load_file("Libs//uix//kv//MenuScreen.kv")
        Builder.load_file("Libs//uix//kv//StatisticScreen.kv")
        Builder.load_file("Libs//uix//kv//BooksScreen.kv")
        Builder.load_file("Libs//uix//kv//EdittingScreen.kv")
        Builder.load_file("Libs//uix//kv//Book.kv")
        Builder.load_file("Libs//uix//kv//book_add_dialog.kv")
        sm = ScreenManager()

        sm.add_widget(MenuScreen(name="menu"))
        sm.add_widget(StatisticScreen(name="statistic"))
        sm.add_widget(EdittingScreen(name="edit"))
        sm.add_widget(BooksScreen(name="books"))

        return sm


if __name__ == '__main__':
    Main().run()