from asyncio import events
from asyncio.windows_events import NULL
from ctypes import sizeof
from posixpath import dirname
import sqlite3
from pprint import pprint
from tkinter.messagebox import NO
from turtle import window_height
import zipfile

from certifi import contents

from kivymd.uix.list import ThreeLineAvatarIconListItem,IconLeftWidget,IconRightWidget,OneLineAvatarIconListItem
from kivymd.uix.button import MDFlatButton,MDRaisedButton
from kivymd.uix.textfield import MDTextField
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.dialog import MDDialog


from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.popup import Popup

from Libs.programclass.modules.CustomList import CustomList
from Libs.programclass.modules.WordsList import WordsList
from Libs.programclass.modules.AddBookDialog import AddBookDialog


from kivy.properties import StringProperty



class BooksScreen(Screen):
    #root variable
    delete_dialog = None
    add_book_dialog_obj = None
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

    #start swap to interanal zone
    def swap_screen(self,name):
        setattr(self.parent,"current" ,'bookInternal')
        self.clear_internal_screen()
        self.load_words(name)


    def clear_internal_screen(self):
        ob = self.parent.get_screen("bookInternal").ids.list_view
        ob.remove_widget(ob.children[0])
        ob.add_widget(WordsList())

    # start algortitm for loading words > build_screen > add_word_into_internal > (get screen with words list)
    def load_words(self, table_name):
        if self.is_table_with_name(table_name):
            self.table_internal_book_name = table_name[0]
            
            self.parent.get_screen("bookInternal").ids.search_field.hint_text = "Search in {}".format(self.table_internal_book_name)
            conn = sqlite3.connect("Data/Base/Books.db")
            cursor = conn.cursor()
            data = cursor.execute("SELECT * FROM " + '\''+table_name[0]+'\'')

            data = data.fetchall()
            conn.close()
            self.build_screen(data,table_name)

    # check data base if exist table
    def is_table_with_name(self,name):
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


    def save_table_name_into_db(self,table_name):
        conn = sqlite3.connect("Data/Base/Books.db")
        cursor = conn.cursor()
        data = cursor.execute("SELECT * FROM last_book_screen_internal")
        data = data.fetchall()
        if len(data) == 0:
            cursor.execute("INSERT INTO last_book_screen_internal VALUE(?,?)",(None,table_name[0]))
        conn.commit()
        conn.close()   



    def build_screen(self,data,table_name):
        pprint(data)
        for word in data:
            self.add_word_into_internal(word)

    # genetate word list for interaln word menu
    def add_word_into_internal(self,word):
        but = CustomList()
        but.Label_menu_texts['word'] = word[0]
        but.Label_menu_texts['translate'] = word[2]

        if word[1] != None and word[1] !='':
            but.Label_menu_texts['transcription'] = word[1]

        but.Label_menu_texts['status'] = str(word[4])

        if word[3] != None and word[1] != '':
            but.Label_menu_texts['asociations'] = word[3]

        self.root.get_screen("bookInternal").ids.list_view.children[0].add_widget(but)


    #end swap to interanal zone

    def into_book_menu(self):
        pass

    def add_book_func(self, book):   
        but = ThreeLineAvatarIconListItem(
            text="{}".format( book[0] ),
            secondary_text="{} words in it".format( book[1] ),
            on_release= lambda x: self.swap_screen(book[0])
        )

        del_item = IconLeftWidget(
            icon="delete",
            on_release= lambda x,z = but: self.del_book_func(z)
            )

        edit_item= IconRightWidget(icon="book-edit")


        but.add_widget(del_item)
        but.add_widget(edit_item)
        self.ids.books_add_list.add_widget(but)





    #delete book form DATA BASE and from screen
    def del_book_func(self,wd_for_del):
        self.wont_to_del_menu(wd_for_del)


    def del_from_data_base(self,wd_for_del):
        conn = sqlite3.connect("Data/Base/Books.db")
        cursor = conn.cursor()
        bookName = wd_for_del.children[2].children[2].text

        cursor.execute("DELETE FROM 'Data_name_of_books' WHERE db_name=?",[bookName])
        cursor.execute("DROP TABLE IF EXISTS '{}'".format(bookName)) 
        conn.commit()
        conn.close()
        self.ids.books_add_list.remove_widget(wd_for_del)


    def wont_to_del_menu(self,ditem):
        but = [
            MDFlatButton(
                text="CANCEL",
                pos_hint={"left":1},
                on_release = lambda x: self.del_menu_dismiss()
            ),
            MDRaisedButton(
                text="DELETE",
                pos_hint={"right":1},
                on_release = lambda x,  z = ditem: self.del_menu_confirm(z)
        )]
        main_lay = BoxLayout(
            orientation= "vertical",
            spacing="12dp",
            size_hint_y= None,
            height= "35dp",
            pos_hint={'top':1},
        )
        bottom_nav_lay = BoxLayout(
            size_hint= (0.8,0.8),
            orientation="horizontal",
            pos_hint={'bottom':1,'center_x':0.5},
        )
        main_lay.add_widget(bottom_nav_lay)

        bottom_nav_lay.add_widget(but[0])
        bottom_nav_lay.add_widget(but[1])



        if not self.delete_dialog:
            self.delete_dialog = MDDialog(
                title="Delete?",
                type="custom",
                content_cls = main_lay,
                radius=[20, 7, 20, 7],
            )
        self.delete_dialog.open()

    
    def del_menu_dismiss(self):
        self.delete_dialog.dismiss()
        self.delete_dialog = None


    def del_menu_confirm(self,ditem):
        self.del_from_data_base(ditem)
        self.delete_dialog.dismiss()
        self.delete_dialog = None


    #--------------------------------------------------------


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

    def create(self, text_field,*arg):
        # see is the text in poput -> textfield no empty
        if text_field.text == "":
            text_field.error = True
        else:
            # zone for check to validation
            name = text_field.text #.replace(" ",'')
            self.create_new_book_by_name(name)

        self.add_book_dialog_obj.dismiss()
        self.add_book_dialog_obj = None


    #create new dialog for add new book into book screen
    def add_book_dialog(self, *instance):


        if not self.add_book_dialog_obj:
            input_book_obj = AddBookDialog()
            but=[
            MDFlatButton(
                text="CANCEL",
                pos_hint={"left":1},
                on_release = lambda x: self.cancel() 
                ),
            MDRaisedButton(
                text="CREATE",
                pos_hint={"right":1},
                on_release = lambda x: self.create(input_book_obj.ids.new_name_of_book)
                ),
            ]
            input_book_obj.ids.bottom_nav.add_widget(but[0])
            input_book_obj.ids.bottom_nav.add_widget(but[1])
            self.add_book_dialog_obj = MDDialog(
                title="Create new",
                type="custom",
                content_cls = input_book_obj,
                radius=[20, 7, 20, 7],
            )
        
        self.add_book_dialog_obj.open()


    def cancel(self, *arg):
        self.add_book_dialog_obj.dismiss()
        self.add_book_dialog_obj = None
        pprint("cancel")