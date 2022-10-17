import time
from datetime import date
import sqlite3

from pprint import pprint
from Libs.programclass.Screens.LearnScreen import LearnScreen
from kivymd.app import MDApp
from kivymd.uix.list import ThreeLineAvatarIconListItem,IconLeftWidget,IconRightWidget

from kivymd.uix.button import MDFlatButton,MDRaisedButton
from kivymd.uix.textfield import MDTextField
from kivymd.uix.dialog import MDDialog
from kivymd.uix.label import MDLabel

from kivy.lang.builder import Builder
from kivy.clock import Clock
Clock.max_iteration = 30


from kivy.uix.boxlayout import BoxLayout
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.popup import Popup
from kivy.uix.gridlayout import GridLayout
from kivy.core.window import Window
from kivy.utils import get_color_from_hex

from kivy.properties import StringProperty
from kivy.properties import NumericProperty
from kivy.properties import ColorProperty


from kivy.garden.matplotlib import FigureCanvasKivyAgg
import matplotlib.pyplot as plt

#include programclasses

from Libs.programclass.Screens.BookScreen import BooksScreen
from Libs.programclass.Screens.EdittingScreen import EdittingScreen
from Libs.programclass.Screens.InternalMenuBookScreen import InternalMenuBookScreen
from Libs.programclass.Screens.MenuScreen import MenuScreen
from Libs.programclass.Screens.StatisticScreen import StatisticScreen,Statistic
from Libs.programclass.modules.CustomBottomNavigation import CustomBottomNavigation
from Libs.programclass.modules.CustomList import CustomList
from Libs.programclass.modules.WordsList import WordsList

#from Libs.uix.kv import ScreenManagerKV,MenuScreen, EdittingScreen,BooksScreen,StatisticScreen


Window.size = 500,800
Window.top = 30
Window.left = 500


class Main(MDApp):
    bg_screens_border_color = "313131"
    bg_screens_color = "#141414"
    bg_screens_whitly_color = "212121"
    icon_but_colors = "#F6F6C4"
    icon_but_colors_hint = "#8B8B6F"
    label_text_colors = "#F6F6C4"
    label_text_colors_hint = "#8B8B6F"
    label_text_colors_hint_hint = "#77775F"
    text_file_colors_hint = "#8B8B6F"
    text_file_colors = "#F6F6C4"



    data = ''
    load_books_triger = False
    load_stats_triger = False
    delete_dialog = None
    screen_is_displayed = "menu"
    sql_executes = ["""
            CREATE TABLE IF NOT EXISTS 'Data_name_of_books' (
                "db_name"	TEXT NOT NULL UNIQUE,
                "size"	INTEGER NOT NULL );""",
            """
            SELECT db_name,size FROM Data_name_of_books
            """,
            ["""CREATE TABLE IF NOT EXISTS '""","""' (
                "time"	TEXT NOT NULL UNIQUE,
                "win"	INTEGER NOT NULL,
                "lose"	INTEGER NOT NULL );"""]
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
        Builder.load_file("Libs//uix//kv//LearnScreen.kv")
        sm = ScreenManager()

        Builder.load_file("Libs//uix//kv//modules//CustomBottomNavigation.kv")
        Builder.load_file("Libs//uix//kv//modules//CustomList.kv")
        Builder.load_file("Libs//uix//kv//modules//WordsList.kv")
        Builder.load_file("Libs//uix//kv//modules//AddBookDialog.kv")
        Builder.load_file("Libs//uix//kv//modules//AddWordDialog.kv")
        Builder.load_file("Libs//uix//kv//modules//SimpleRegime.kv")
        Builder.load_file("Libs//uix//kv//modules//RundomRegime.kv")
        Builder.load_file("Libs//uix//kv//modules//CustomBooksListElement.kv")
        Builder.load_file("Libs//uix//kv//modules//CustomBooksList.kv")


        self.screens = ['menu','statistic','books','edit','bookInternal','learn']
        self.screens_obj = [
            MenuScreen(name="menu"),
            StatisticScreen(name="statistic"),
            EdittingScreen(name="edit"),
            BooksScreen(name="books"),
            InternalMenuBookScreen(name="bookInternal"),
            LearnScreen(name="learn"),
        ] 
       # self.screens_obj[0].load_execute_books() # book screen pre load
        

        for element_screen in self.screens_obj:
            sm.add_widget(element_screen)

        return sm  


    def get_tried_word(self):
        return self.root.get_screen("menu").data


    
    def add_statistic(self, status, book,*args):
        pprint((book,status))
        
        inf_status = [1,0] if status == "win" else [0,1]

        table_creator = self.sql_executes[2][0]+book+self.sql_executes[2][1]
        now_time = date.today()
        now_time = now_time.strftime("""%d %m %Y""")
        conn = sqlite3.connect("Data/Base/Statistic.db")
        cursor = conn.cursor()
        cursor.execute(table_creator)

        input_execute = """INSERT OR IGNORE INTO '"""+ book +"""'"""+"""VALUES(?,?,?)"""
        if inf_status[0]:
            update_execute = """UPDATE \"""" + book + """\" SET \"win\"=\"win\"+1 WHERE \"time\"=?"""
        else:
            update_execute = """UPDATE \"""" + book + """\" SET \"lose\"=\"lose\"+1 WHERE \"time\"=?"""

        start = time.time()

    
        cursor.execute(input_execute,(now_time,0,0))
        conn.commit()
        conn.close()

        conn = sqlite3.connect("Data/Base/Statistic.db")
        cursor = conn.cursor()
        cursor.execute(update_execute,[now_time])
        conn.commit()

        
        print(f"[Log   ] inputed into \'{book}\' {time.time()-start}")
        pprint((now_time,inf_status[0],inf_status[1]))
        conn.close()



    #zone to load learn screen (random or simple or.... )
    def load_learning(self,regime,*arg):
        self.screens_obj[5].regime_name = regime
        self.swap_screen(('6'))


    #end zone
    def get_size_into_internal(self,book,size_load):
        '''funk return new size scroll view obj when swipe into internal screen'''
        if size_load == None:
            get_execute = "SELECT size FROM 'Data_name_of_books' WHERE db_name = '"+book+"'"

            conn = sqlite3.connect("Data/Base/Books.db")
            cursor = conn.cursor()
            data_db = cursor.execute(get_execute)
            size = data_db.fetchall()[0][0]
            conn.close()
            return size // 7 + 1


    def add_statistic(self):
        plt.figure(figsize=(9,3))
        weekdata = self.statistic.week() # [dict(date : [win, lose]) , bool]
        height = []
        tick_label = list(weekdata.keys())
        for i in tick_label:
            height.append(weekdata[i][0])

        left = [i+1 for i in range(len(tick_label))]
        tick_label = [ i[:2]+"-"+i[3:5] for i in list(weekdata.keys())]
        pprint(height)
        pprint(tick_label)
        plt.bar(left, height, tick_label = tick_label,
        width = 0.8, color = ['green'])
        
        # naming the x-axis
        plt.xlabel('Days')
        # naming the y-axis
        plt.ylabel('Wins')
        # plot title
        plt.title(f'Simple regime of {self.statistic.name_db[0]}')
        self.root.get_screen("statistic").ids.graf_widget.add_widget(FigureCanvasKivyAgg(plt.gcf()))

        self.load_stats_triger = True


    #START FOR zone with swap and bind internal book screen
    def swap_screen(self,screen_name_index,*name_book):
        '''func get ( index of screen in self.screens like ('3') ) numeration of screen going with 1

            if index of screen = ('5') need get book name'''
        screen_name = self.screens
        setattr(self.root,"current" ,screen_name[int(screen_name_index[0])-1])

        if screen_name_index[0] == '2':
            self.statistic = Statistic()
            self.statistic.get_data()
            if not self.load_stats_triger:
                self.add_statistic()


        if screen_name_index[0] == '5':
            self.clear_internal_screen()
            self.root.get_screen("bookInternal").ids.search_field.hint_text = f"Search in {name_book[0]}"
            
            self.root.get_screen("bookInternal").ids.list_view.children[0].size_hint_y = self.get_size_into_internal(name_book[0],None)
            self.load_words(name_book) 

        pprint("[Log   ]"f"@{self.screen_is_displayed}"+" >> "+f"@{screen_name[int(screen_name_index[0])-1]}")
        self.screen_is_displayed = screen_name[int(screen_name_index[0])-1]


    def clear_internal_screen(self):
        '''clear word from screen when go out of internal screen'''
        ob = self.root.get_screen("bookInternal").ids.list_view
        ob.remove_widget(ob.children[0])
        ob.add_widget(WordsList())


    def add_word_into_internal(self,word):
        '''write word in list inside the bookInternal for view 
        
          get element of table with : [ word, transcription, translate, asociations, status ]

          create CastomList() and with parametrs in transferred list
          add him into ("bookInternal").ids.list_view.children[0]
        '''
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
        '''func check is table by name of not

            (return: bool) (get str: name)
        '''
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
        '''func start cycle passes on each element of the table which has been transferred

            going to ---> add_word_into_internal(*element of table)
        '''
        start = time.time()
        for word in data:
            self.add_word_into_internal(word)
        print(f"[Log   ] writed words {time.time()-start}")

    # start algortitm for loading words > build_screen > add_word_into_internal > (get screen with words list)
    def load_words(self, table_name):
        ''' funk preload word from DataBase by str: table_name

            going to ---> is_tabele_with_name(*table name) if return true 
                going to ---> build_screen(*data of table)
            
            data is table of infor from Data/Base/Books.db - with name of table = table_name
        '''
        if self.is_tabele_with_name(table_name):
            start = time.time()
            conn = sqlite3.connect("Data/Base/Books.db")
            cursor = conn.cursor()
            print(table_name[0])
            data = cursor.execute("SELECT * FROM " + '\''+table_name[0]+'\'')
            data = data.fetchall()
            conn.close()
            print(f"[Log   ] geted infor from \'{table_name}\' {time.time()-start}")
            self.build_screen(data)


    #END FOR  zone with swap and bind internal book screen

    #START FOR zone where delete  book
    def del_from_data_base(self,wd_for_del):
        '''delete information(table) from database by name'''
        conn = sqlite3.connect("Data/Base/Books.db")
        cursor = conn.cursor()
        bookName = wd_for_del.children[2].children[2].text

        cursor.execute("DELETE FROM 'Data_name_of_books' WHERE db_name=?",[bookName])
        cursor.execute("DROP TABLE IF EXISTS '{}'".format(bookName)) 
        conn.commit()
        conn.close()
        self.root.get_screen("books").ids.books_add_list.remove_widget(wd_for_del)


    def wont_to_del_menu(self,ditem):
        ''' fuck create dialog with 2 buttons ok or close 
        
            get widget that you want to delete
        '''
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
        '''funck if dont wont to delete book'''
        self.delete_dialog.dismiss()
        self.delete_dialog = None


    def del_menu_confirm(self,ditem):
        '''funck if wont to delete book'''
        self.del_from_data_base(ditem)
        self.delete_dialog.dismiss()
        self.delete_dialog = None

    #-----------------------------------------------
    
    #START FOR zone where loading new book
    def load_books(self): 
        ''' funk load book from data base and write created widget of book in list'''
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
        ''' return table from db with list [(book_name1,size),(book_name2,size),....]'''
        conn = sqlite3.connect("Data/Base/Books.db")
        cursor = conn.cursor()
        data = cursor.execute(self.sql_executes[1]).fetchall()
        conn.close()
        return data


    def create_data_base(self):
        '''create table with simple parametrs of book if no exist'''
        conn = sqlite3.connect("Data/Base/Books.db")
        cursor = conn.cursor()
        cursor.execute(self.sql_executes[0])
        conn.close()


    def edit_menu(self):
        pass


    def add_book_func(self, new_book_name,new_book_word_number):
        '''func write all book that has in DataBase on book screen'''
        but = ThreeLineAvatarIconListItem(
            text="{}".format( new_book_name ),
            secondary_text="{} words in it".format( new_book_word_number ),
            secondary_theme_text_color="Custom",
            secondary_text_color=get_color_from_hex(self.label_text_colors_hint),
            on_release= lambda x: self.swap_screen(('5'),new_book_name),
            theme_text_color="Custom",
            text_color=get_color_from_hex(self.label_text_colors),
        )
        del_item = IconLeftWidget(
            icon="delete",
            on_release= lambda y,z = but: self.wont_to_del_menu(z),
            text_color=get_color_from_hex(self.icon_but_colors),
            theme_text_color="Custom"
        )
        edit_item= IconRightWidget(
            icon="book-edit",
            on_release= lambda x: self.edit_menu(),
            text_color=get_color_from_hex(self.icon_but_colors),
            theme_text_color="Custom"
        )
        but.add_widget(del_item)
        but.add_widget(edit_item)
        self.root.get_screen("books").ids.books_add_list.add_widget(but)

    #END FOR zone where loading new book

if __name__ == '__main__':
    Main().run()