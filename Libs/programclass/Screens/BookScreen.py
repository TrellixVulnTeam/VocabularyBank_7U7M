import sqlite3
from pprint import pprint

from kivymd.uix.list import ThreeLineAvatarIconListItem,IconLeftWidget,IconRightWidget
from kivymd.uix.button import MDFlatButton
from kivymd.uix.textfield import MDTextField

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.popup import Popup

from Libs.programclass.modules.CustomList import CustomList
from Libs.programclass.modules.WordsList import WordsList


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
        if self.is_tabele_with_name(table_name):
            conn = sqlite3.connect("Data/Base/Books.db")
            cursor = conn.cursor()
            print(table_name[0])
            data = cursor.execute("SELECT * FROM " + '\''+table_name[0]+'\'')
            data = data.fetchall()
            conn.close()
            self.build_screen(data)

    # check data base if exist table
    def is_tabele_with_name(self,name):
        conn = sqlite3.connect("Data/Base/Books.db")
        cursor = conn.cursor()
        for item in cursor.execute("SELECT db_name FROM Data_name_of_books").fetchall():
            if name == item:
                conn.close()
                return True
            else:
                continue


    def build_screen(self,data):
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

    def cancel(self, *arg):
        self.NewDialog.dismiss()
        pprint("cancel")

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
            on_release= lambda x,y = book[0],z = but: self.del_book_func(y,z)
            )

        edit_item= IconRightWidget(icon="book-edit")


        but.add_widget(del_item)
        but.add_widget(edit_item)
        self.ids.books_add_list.add_widget(but)

    #delete book form DATA BASE and from screen
    def del_book_func(self,bookName,wd_for_del):
        conn = sqlite3.connect("Data/Base/Books.db")
        cursor = conn.cursor()
        cursor.execute("DELETE FROM 'Data_name_of_books' WHERE db_name=?",[bookName])
        cursor.execute("DROP TABLE IF EXISTS '{}'".format(bookName)) 
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

            # zone for check to validation
            name = self.text_input.text #.replace(" ",'')
            self.create_new_book_by_name(name)
            self.NewDialog.dismiss()

    #create new dialog for add new book into book screen
    def add_book_dialog(self, *instance):
        self.NewDialog = Popup(
            title="Input a new book",
            size_hint=(None,None),
            title_align='center',
            size=(200,150),
            auto_dismiss=False,
            separator_color='#FEF9F5'
        )
        main_box = BoxLayout(
            orientation="vertical",
            size_hint=(0.95,0.95)
        )
        in_main_box = BoxLayout(
            size_hint=(0.9,0.65)
        )
        self.text_input = MDTextField(
            helper_text="Name is empty, please input or close",
            helper_text_mode="on_error",
            hint_text="write a book",
            current_hint_text_color='#706B67',
            foreground_color="#FEF9F5"
        )

        close_but = MDFlatButton(
            pos_hint={ 'center_x':0.5,'center_y':0.5 },
            text_color="#FEF9F5",
            text="CLOSE"
        )
        ok_but = MDFlatButton(
            pos_hint={ 'center_x':0.5,'center_y':0.5 },
            text_color="#FEF9F5",
            text="OK"
        )
        close_but.bind(on_release=self.cancel)
        ok_but.bind(on_release=self.create)


        bot_lay = BoxLayout(orientation='horizontal',pos_hint={'bottom':1},size_hint=(0.9,0.35))

        bot_lay.add_widget(ok_but)
        bot_lay.add_widget(close_but)
        in_main_box.add_widget(self.text_input)
        main_box.add_widget(in_main_box)
        main_box.add_widget(bot_lay)

        self.NewDialog.add_widget(main_box)

        self.NewDialog.open()
