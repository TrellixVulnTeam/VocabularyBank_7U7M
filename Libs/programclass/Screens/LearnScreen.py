from pprint import pprint


from kivy.utils import get_color_from_hex


from Libs.programclass.modules.Menu import CustomMenu

from kivy.animation import Animation
from kivy.metrics import sp
from kivy.uix.screenmanager import Screen

from Libs.programclass.modules.regimes.SimpleRegime import SimpleRegime,RestartButton
from Libs.programclass.modules.regimes.RundomRegime import RundomRegime


from kivy.properties import StringProperty

import sqlite3
import time
import random


class LearnScreen(Screen):
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
    back_button_size = StringProperty("46sp")
    regime_name = ""
    get_out = True



    def clear_learn_pool(self):
        if hasattr(self,'add_element'):
            self.ids.learn_pool.remove_widget(self.add_element)
        self.ids.menu.text = "Select book"
        self.get_out = True


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
                "text": f"{item[0]}",
                "viewclass": "MenuElement",
                "on_release": lambda x=f"{item[0]}": self.menu_callback(x),
                "width": sp(95)
            } for item in book_items
            ]
        self.menu = CustomMenu(
            background_color=get_color_from_hex(self.bg_screens_whitly_color),
            caller=self.ids.menu,
            items=menu_items,
            width_mult=3,
            radius=[6, 6, 6, 6],
        )

        self.menu.open()
    

    def get_infor(self,table):
        start = time.time()
        conn = sqlite3.connect("Data/Base/Books.db")
        cursor = conn.cursor()
        data = cursor.execute("SELECT * FROM '"+table+"'")
        data = data.fetchall()
        conn.close()
        print(f"[Log   ] geted infor from \'{table}\' {time.time()-start}")
        return data


    def menu_callback(self, book_name):
        self.ids.menu.text = book_name
        self.menu.dismiss()

    
    def write_random(self,data,lens,status):
        if status == 0:


            self.tried_word = random.randint(0,lens-1)

            while self.tried_word in self.add_element.visited_word_indexs:
                if len(self.add_element.visited_word_indexs) == lens:
                    self.add_element.visited_word_indexs = []
                self.tried_word = random.randint(0,lens-1)
              
            self.add_element.visited_word_indexs.append(self.tried_word)

            self.add_element.indexs = [i for i in range(lens) if i != self.tried_word]
            random.shuffle(self.add_element.indexs)
            pprint((self.add_element.indexs,self.tried_word))

            self.tried_word_data = data[self.tried_word]
            self.add_infor_in_learn_pool(self.tried_word,data)


    def add_infor_in_learn_pool(self,index,data,inverse=False):
        data_pointer = (0,1)
        if inverse == True:
            data_pointer = (1,0)

        # set data arrgs for butbox objs

        setattr(self.add_element.ids.top_left, "data", self.tried_word_data)
        setattr(self.add_element.ids.top_right, "data", self.tried_word_data)
        setattr(self.add_element.ids.bottom_left, "data", self.tried_word_data)
        setattr(self.add_element.ids.bottom_right, "data", self.tried_word_data)

        self.add_element.ids.word.children[0].text = data[index][data_pointer[0]]

        real_index = random.randint(0,3)
        if real_index != 0:
            self.add_element.ids.top_left.children[0].text = data[self.add_element.indexs[0]][data_pointer[1]]
        else:
            self.add_element.ids.top_left.children[0].text = data[index][data_pointer[1]]
            

        if real_index != 1:
            self.add_element.ids.top_right.children[0].text = data[self.add_element.indexs[1]][data_pointer[1]]
        else:
            self.add_element.ids.top_right.children[0].text = data[index][data_pointer[1]]


        if real_index != 2:
            self.add_element.ids.bottom_left.children[0].text = data[self.add_element.indexs[2]][data_pointer[1]]
        else:
            self.add_element.ids.bottom_left.children[0].text = data[index][data_pointer[1]]


        if real_index != 3:
            self.add_element.ids.bottom_right.children[0].text = data[self.add_element.indexs[3]][data_pointer[1]]
        else:
            self.add_element.ids.bottom_right.children[0].text = data[index][data_pointer[1]]


    # after start events
    def disbale_buttons(self,disable_status=True,opacity_status=0):
        self.ids.start_but.disabled = disable_status
        self.ids.start_but.opacity = opacity_status
        self.ids.menu.disabled = disable_status
        self.ids.menu.opacity = opacity_status


    def add_restart_button(self):
        self.resturt_button_obj = RestartButton()
        self.ids.beginning_end_lay.add_widget(self.resturt_button_obj)


    def remuve_restart_button(self):
        self.ids.beginning_end_lay.remove_widget(self.resturt_button_obj)


    def redisable_all(self):
        if hasattr(self,"resturt_button_obj"):
            self.disbale_buttons(False,1)
            self.remuve_restart_button()


    def load_learning_pool(self):
        if self.regime_name == "Standart":
            if self.ids.menu.text != "Select book":
                if self.get_out:
                    self.data = self.get_infor(self.ids.menu.text)
                    pprint('data geted')
                    
                    self.max_len = len(self.data)
                    if self.max_len != 0:
                        pprint("len geted")

                        self.add_element = SimpleRegime()
                        self.add_element.book_name = self.ids.menu.text

                        pprint("element created")

                        self.ids.learn_pool.add_widget(self.add_element)

                        pprint("element added into pool")


                        setattr(self.add_element,'data_base_data',self.data)
                        setattr(self.add_element, "data_base_data_max_len",self.max_len)

                        pprint("set args")
                        self.write_random(self.data,self.max_len,0)

                        pprint("write complite")

                        self.disbale_buttons()
                        self.add_restart_button()
                        pprint("reset buttons was made")
                        self.get_out = False


                else:
                    pass



            else:
                pass


        elif self.regime_name == "Rundom":
            self.add_element = RundomRegime()
            self.ids.learn_pool.add_widget(self.add_element)
