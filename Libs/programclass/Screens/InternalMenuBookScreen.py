from pprint import pprint
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup

from kivy.properties import StringProperty
from kivymd.uix.button import MDFlatButton,MDRaisedButton
from kivymd.uix.dialog import MDDialog

from Libs.programclass.modules.AddWordDialog import AddWordDialog

import sqlite3


class InternalMenuBookScreen(Screen):
    add_word_dialog_obj = None
    icon_button_pluss_size = StringProperty("42sp")
    icon_filter_size = StringProperty("30sp")
    icon_search_size = StringProperty("30sp")
    font_size_search_field = StringProperty("26sp")
    icon_left_menu_botton_size = StringProperty("36sp")
    


    def write_in_data_base(self,table_name, information):
        pass


    def get_text_fields(self,obj):
        return [item.children[1] for item in obj.ids.information_box.children]


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


    def create_new_word(self,data):
        conn = sqlite3.connect("Data/Base/Books.db")
        cursor = conn.cursor()
        #cursor.execute("INSERT INTO")
        conn.close()

    def cancel(self, *arg):
        self.add_word_dialog_obj.dismiss()
        self.add_word_dialog_obj = None
        pprint("cancel")


    def create(self, text_fields,*arg):
        # see is the text in poput -> textfield no empty
        pprint(text_fields)
            # zone for check to validation
            #name = text_field.text #.replace(" ",'')
            #self.create_new_word_by_data(data)

        self.add_word_dialog_obj.dismiss()
        self.add_word_dialog_obj = None


