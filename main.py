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
    
    def load_books(self):
        self.create_data_base()



    def create_data_base(self):
        conn = sqlite3.connect("Data/Base/Books.db")
        cursor = conn.cursor()
        cursor.execute(self.table_creator[2])
        conn.close()
    


    def cancel(self, *arg):
        self.NewDialog.dismiss()
        pprint("cancel")

    def create_new_book_by_name(self,name):
        pprint(f"create {name} in database")


    def create(self, *arg):
        # see is the text in poput -> textfield no empty
        if self.text_input.text == "":
            self.text_input.error = True
        else:
            self.create_new_book_by_name(self.text_input.text)
            self.NewDialog.dismiss()
            pprint("create")


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

    icon_button_top_menu_size = StringProperty("32sp")
    icon_button_bot_menu_size = StringProperty("34sp")
    icon_main_menu_size = StringProperty("42sp")

    def load_books(self):
        pprint("loading")


    def add_book_func(self, *arg):   

        but = ThreeLineAvatarIconListItem(
            text="Book Number{}".format( len(self.root.get_screen("books").ids.books_add_list.children)+1 ),
            secondary_text="0 words in it"
        )
        but.add_widget(
            IconLeftWidget(
                icon="delete"
            )
        )
        but.add_widget(
            IconRightWidget(
                icon="book-edit"
            )
        )
        
        self.root.get_screen("books").ids.books_add_list.add_widget(but)
        pprint(self.root.get_screen("books").ids.books_add_list.children)



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