import sqlite3
from pprint import pprint

from kivymd.uix.list import ThreeLineAvatarIconListItem,IconLeftWidget,IconRightWidget
from kivymd.uix.button import MDFlatButton
from kivymd.uix.textfield import MDTextField

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.popup import Popup

from kivy.properties import StringProperty



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
        self.ids.books_add_list.remove_widget(wd_for_del)



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
