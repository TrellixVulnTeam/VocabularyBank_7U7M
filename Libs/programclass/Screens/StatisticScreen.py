from kivy.uix.screenmanager import Screen



from kivy.metrics import sp
from kivy.utils import get_color_from_hex
from kivy.uix.dropdown import DropDown


from Libs.programclass.modules.Menu import CustomMenu

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.behaviors.button import ButtonBehavior

import time
from datetime import date
import sqlite3
from pprint import pprint


class Statistic:
    information = []
    def week(self):
        n_day = 0
        now_date = date.today()
        now_time = now_date.strftime("""%d %m %Y""") # 'xx yy zz'
        now_time_cut = now_time.split()
        week_days = []

        if int(now_time.split()[0]) >= 7:
            for day in range(7):
                numday = str(int(now_time_cut[0])-day)
                week_days.append( numday + " " + now_time_cut[1] + " " + now_time_cut[2] )

        else:
            for day in range(int(now_time.split()[0])):
                numday = str(int(now_time_cut[0])-day) if len(str(int(now_time_cut[0])-day)) == 2 else "0" + str(int(now_time_cut[0])-day) 

                week_days.append( numday + " " + now_time_cut[1] + " " + now_time_cut[2] )
            if now_time_cut[1] != '01':
                for day in range(7-int(now_time.split()[0])):
                    if now_date.month % 2 == 1:
                        n_day = 31
                    elif now_date.month == 2:
                        if now_date.year % 4 == 0:
                            n_day = 29
                        else:
                            n_day = 28
                    else:
                        n_day = 30

                    numday =   str(int(n_day)-day) if len(str(int(n_day)-day)) == 2 else "0" + str(int(n_day)-day) 
                    nummunth = str(int(now_time_cut[1])-1) if len(str(int(now_time_cut[1])-1)) == 2 else  "0" + str(int(now_time_cut[1])-1)

                    week_days.append( numday + " " + nummunth + " " + now_time_cut[2] )

            else:
                for day in range(7-int(now_time.split()[0])):
                    if now_date.month % 2 == 1:
                        n_day = 31
                    elif now_date.month == 2:
                        if now_date.year % 4 == 0:
                            n_day = 29
                        else:
                            n_day = 28
                    else:
                        n_day = 30

                    numday =   str(int(n_day)-day) if len(str(int(n_day)-day)) == 2 else "0" + str(int(n_day)-day) 
                    nummunth = str(12) if len(str(12)) == 2 else  "0" + str(12)
                    numyear =  str(int(now_time_cut[2])-1)

                    week_days.append( numday + " " + nummunth + " " + numyear)

        week_stats_information = {}
        for day in week_days:
            if day in self.information.keys():
                week_stats_information.update({ day:self.information[day] })
            else:
                week_stats_information.update({ day:[0,0] })

            

        return week_stats_information


    

    def today(self):
        now_time = date.today()
        now_time = now_time.strftime("""%d %m %Y""")
        if now_time in self.information.keys():
            if len(self.information)>0: 
                return [self.information[now_time],True]

        else:
            if len(self.information)>0: 
                return [self.information[now_time],True]


    def get_first_book(self):
        start = time.time()
        conn = sqlite3.connect("Data/Base/Books.db")
        get_book_execute = "SELECT db_name,size FROM \"Data_name_of_books\""

        cursor = conn.cursor()
        data = cursor.execute(get_book_execute)      
        data = data.fetchall()
        point = [0,0] 
        for index,i in enumerate(data):
            if i[1] > point[0]:
                point[0] = i[1]
                point[1] = index
        
        conn.close()
        print(f"[Log   ] geted infor from \'{'Data_name_of_book'}\' {time.time()-start}")

        return data[point[1]]


    def get_data(self):

        now_time = date.today()
        now_time = now_time.strftime("""%d %m %Y""")

    
        name  = self.get_first_book()
        self.name_db = name
        start = time.time()
        get_stats_execute = "SELECT * FROM \"" + name[0] + "\""

        conn = sqlite3.connect("Data/Base/Statistic.db")
        cursor = conn.cursor()
        data = cursor.execute(get_stats_execute)
        self.information = data.fetchall()
        self.information = { self.information[i][0] : [self.information[i][1], self.information[i][2]] for i in range(len(self.information))}
        conn.close()
        print(f"[Log   ] geted infor from \'{name[0]}\' {time.time()-start}")


class StatisticScreen(Screen):
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
                "width": sp(95),
            } for item in book_items
            ]
        self.menu = CustomMenu(
            background_color=get_color_from_hex(self.bg_screens_whitly_color),
            width_mult=3,
            radius=[6, 6, 6, 6],
            caller=self.ids.menu,
            items=menu_items,
        )

        self.menu.open()


    def change_diagram(self, element, types):
        if types == "book":
            self.new_diagram_with_book(element)
        elif types == "regimes":
            self.new_diagram_with_regimes()
        else:
            pass




    def menu_callback(self, book_name):
        if self.ids.menu.text != book_name:
            self.ids.menu.text = book_name
            self.change_diagram(book_name,"book")

        self.menu.dismiss()


    def menu_regime_callback(self,regimes):
        if self.ids.regimes.text != regimes:
            self.ids.regimes.text = regimes
            self.change_diagram(regimes,"regime")


        self.menu_regime.dismiss()


    def menu_regime_start(self):
        book_items = ['simple','rundom']
        menu_items = [
            {
                "text": f"{item}",
                "viewclass": "MenuElement",
                "on_release": lambda x=f"{item}": self.menu_regime_callback(x),
                "width": sp(95)
            } for item in book_items
            ]
        self.menu_regime = CustomMenu(
            background_color=get_color_from_hex(self.bg_screens_whitly_color),
            width_mult=3,
            radius=[6, 6, 6, 6],
            caller=self.ids.regimes,
            items=menu_items,
        )


        self.menu_regime.open()




class StatisticSelectDropDown(DropDown):
    pass


class StatisticSelectDropDownElement(BoxLayout, ButtonBehavior):

    def pe(self):
        pprint(self)