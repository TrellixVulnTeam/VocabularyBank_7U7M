from pprint import pprint
from kivy.uix.screenmanager import Screen


import sqlite3



class MenuScreen(Screen):
    data = ""

    #------------------- will edit
    def load_execute_books(self):
        conn = sqlite3.connect("Data/Base/Books.db")
        cursor = conn.cursor()

        data = cursor.execute("SELECT * FROM 'Data_name_of_books'")
        data = data.fetchall()
        pprint(data)
        conn.close()
        self.add_list_elements(data)

    
    def add_list_elements(self,data):
        # im know that its f***ing sh***  x_x
        pass



            #self.ids.list_editor.children[1].add_widget(element)
            #element.write_infor(item)
        