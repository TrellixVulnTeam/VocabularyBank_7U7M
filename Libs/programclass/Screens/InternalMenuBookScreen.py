from pprint import pprint
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup

from kivy.properties import StringProperty
from kivymd.uix.button import MDFlatButton,MDRaisedButton
from kivymd.uix.dialog import MDDialog

from Libs.programclass.modules.AddWordDialog import AddWordDialog
from Libs.programclass.modules.CustomList import CustomList

import sqlite3


class InternalMenuBookScreen(Screen):
    self_name_in_db = ''
    add_word_dialog_obj = None
    icon_button_pluss_size = StringProperty("42sp")
    icon_filter_size = StringProperty("30sp")
    icon_search_size = StringProperty("30sp")
    font_size_search_field = StringProperty("26sp")
    icon_left_menu_botton_size = StringProperty("36sp")
    

    def get_now_scroll_size(self):
        return self.ids.list_view.children[0].size_hint_y


    def rewrite_word(self,parent_widget):
        pass


    def get_text_fields(self,obj):
        '''Convert list of TextField -> list of string'''
        return [item.children[0] for item in obj.ids.information_box.children]


    def add_word_dialog(self, *instance):
        if not self.add_word_dialog_obj:
            input_word_obj = AddWordDialog()

            fields = self.get_text_fields(input_word_obj)

            but=[
            MDFlatButton(
                text="CANCEL",

                on_release = lambda x: self.cancel() 
                ),
            MDRaisedButton(
                text="CREATE",

                on_release = lambda x: self.create(fields)
                ),
            ]
            input_word_obj.ids.bottom_nav.add_widget(but[0])
            input_word_obj.ids.bottom_nav.add_widget(but[1])
            self.add_word_dialog_obj = MDDialog(
                title="Create new",
                type="custom",
                content_cls = input_word_obj,
                radius=[20, 7, 20, 7],
            )
        
        self.add_word_dialog_obj.open()


    def update_on_scroll_size(self, size):
        '''func resize scroll view obj when add new Obj'''
        self.ids.list_view.children[0].size_hint_y = self.ids.list_view.children[0].size_hint_y + 0.2


    def update_on_book_screen(self, size):
        '''func resize size of book into book screen'''
        for book in self.parent.get_screen("books").ids.books_add_list.children:
            if book.text == self.self_name_in_db:
                setattr(book,'hint_text',str(size)+" word in it ")


    def update_on_internal_screen(self,data):
        '''add new CastomList() with atributes in trasfered list
            
            get list [ word, translate, transcription, asociation]
        '''
        but = CustomList()
        but.Label_menu_texts['word'] = data[0]
        but.Label_menu_texts['translate'] = data[1]

        if data[1] != None and data[1] !='':
            but.Label_menu_texts['transcription'] = data[2]

        but.Label_menu_texts['status'] = "0"

        if data[3] != None and data[1] != '':
            but.Label_menu_texts['asociations'] = data[3]
        self.ids.list_view.children[0].add_widget(but)


    def update_information_on_screens(self,data,size):
        ''' func sturn all other func hous update somthing'''
        self.update_on_book_screen(size)
        self.update_on_internal_screen(data) 
        self.update_on_scroll_size(data)


    def update_db_infor(self,data):
        '''ubdatate infor about book in DB and on Mainloop'''
        get_execute = "SELECT size FROM 'Data_name_of_books' WHERE db_name = '"+self.self_name_in_db+"'"
        set_execute = "UPDATE 'Data_name_of_books' SET size = ? WHERE db_name = '"+self.self_name_in_db+"'"

        conn = sqlite3.connect("Data/Base/Books.db")
        cursor = conn.cursor()
        data_db = cursor.execute(get_execute)
        size = data_db.fetchall()[0][0] + 1
        cursor.execute(set_execute,[size])
        conn.commit()
        conn.close()

        self.update_information_on_screens(data,size)


    def write_data_in_db(self,data):
        '''ubdatate infor about book in DB by name'''
        text = self.ids.search_field.hint_text.split()[-1]
        self.self_name_in_db = text

        write_execute = "INSERT INTO '"+self.self_name_in_db+"' VALUES(?,?,?,?,?,?)"
        conn = sqlite3.connect("Data/Base/Books.db")
        cursor = conn.cursor()
        cursor.execute(write_execute,[data[0],data[1],data[2],data[3],0,None])
        conn.commit()
        conn.close()
        self.update_db_infor(data)


    def validation(self,data):
        '''func see is new word no empty'''
        data = data[::-1]
        if data[0] == "" or data[1] == "":
            print("Has no valid")
        else:
            self.write_data_in_db(data)
            self.add_word_dialog_obj.dismiss()
            self.add_word_dialog_obj = None


    def create_new_word(self,data):
        '''create new word event'''
        text = self.ids.search_field.hint_text.split()[-1]
        self.self_name_in_db = text

        text_data = [i.text for i in data]
        self.validation(text_data)


    def cancel(self, *arg):
        self.add_word_dialog_obj.dismiss()
        self.add_word_dialog_obj = None
        pprint("cancel")


    def create(self, text_fields,*arg):
        # see is the text in poput -> textfield no empty
        self.create_new_word(text_fields)
        

            # zone for check to validation
            #name = text_field.text #.replace(" ",'')
            #self.create_new_word_by_data(data)

