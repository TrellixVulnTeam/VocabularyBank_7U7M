from pprint import pprint

from kivymd.app import MDApp
from kivymd.uix.list import ThreeLineAvatarIconListItem,IconLeftWidget,IconRightWidget

from kivy.lang.builder import Builder

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.uix.screenmanager import Screen, ScreenManager

from kivy.properties import StringProperty
from kivy.properties import NumericProperty

#from Libs.uix.kv import ScreenManagerKV,MenuScreen, EdittingScreen,BooksScreen,StatisticScreen


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
    icon_button_pluss_size = StringProperty("42sp")
    icon_filter_size = StringProperty("30sp")
    icon_search_size = StringProperty("30sp")
    font_size_search_field = StringProperty("26sp")



class EdittingScreen(Screen):
    pass



class Main(MDApp):
    icon_button_top_menu_size = StringProperty("32sp")
    icon_button_bot_menu_size = StringProperty("34sp")
    icon_main_menu_size = StringProperty("42sp")


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
        sm = ScreenManager()

        sm.add_widget(MenuScreen(name="menu"))
        sm.add_widget(StatisticScreen(name="statistic"))
        sm.add_widget(EdittingScreen(name="edit"))
        sm.add_widget(BooksScreen(name="books"))

        return sm



if __name__ == '__main__':
    Main().run()