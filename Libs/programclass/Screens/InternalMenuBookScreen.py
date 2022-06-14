from cgitb import text
from hashlib import md5
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup

from kivy.properties import StringProperty
from kivymd.uix.textfield import MDTextField
from kivymd.uix.button import MDFlatButton
from kivymd.uix.label import MDLabel

import sqlite3


class InternalMenuBookScreen(Screen):
    icon_button_pluss_size = StringProperty("42sp")
    icon_filter_size = StringProperty("30sp")
    icon_search_size = StringProperty("30sp")
    font_size_search_field = StringProperty("26sp")
    icon_left_menu_botton_size = StringProperty("36sp")



    def write_in_data_base(self,table_name, information):
        pass

    def add_book_dialog(self, *instance):
        self.NewDialog = Popup(
            title="Input a new Word",
            size_hint=(None,None),
            size=(600,430),
            auto_dismiss=False
        )
        main_box = BoxLayout(
            orientation="vertical",
            size_hint=(0.95,0.95)
        )
        in_main_box_top = BoxLayout(
            orientation="vertical",
            size_hint=(0.9,0.7)
        )

        word_box = BoxLayout(
            orientation = 'horizontal'
            )
        translate_box = BoxLayout(
            orientation = 'horizontal'
            )
        transcription_box = BoxLayout(
            orientation = 'horizontal'
            )


        in_main_box_bottom = BoxLayout(
            orientation="horizontal",
            size_hint=(0.95,0.3)
        )

        self.text_input_word = MDTextField(
            size_hint=(0.8,0.6),
            helper_text="Line is empty, please input or close",
            helper_text_mode="on_error",
        )
        self.text_input_translate = MDTextField(
            size_hint=(0.8,0.6),
            helper_text="Line is empty, please input or close",
            helper_text_mode="on_error",
        )
        
        self.text_input_transcription = MDTextField(
            size_hint=(0.8,0.6),
            helper_text="Line is empty, please input or close",
            helper_text_mode="on_error",
        )

        word_box.add_widget(
            MDLabel(
                text="Word"
                )
        )
        translate_box.add_widget(
            MDLabel(
                text="translate"
            )
        ) 
        transcription_box.add_widget(
            MDLabel(
                text="transcription"
            )
        )

        word_box.add_widget( self.text_input_word )
        translate_box.add_widget( self.text_input_transcription )
        transcription_box.add_widget( self.text_input_translate )

        in_main_box_top.add_widget(word_box)
        in_main_box_top.add_widget(translate_box)
        in_main_box_top.add_widget(transcription_box)

        close_but = MDFlatButton(
            size_hint=(0.4,0.45),
            text="CLOSE"
        )
        ok_but = MDFlatButton(
            size_hint=(0.4,0.45),
            text="OK"
        )

        close_but.bind(on_release=self.close)
        ok_but.bind(on_release=self.create)


        in_main_box_bottom.add_widget( close_but )
        in_main_box_bottom.add_widget( ok_but )

        main_box.add_widget( in_main_box_top )
        main_box.add_widget( in_main_box_bottom )

        self.NewDialog.add_widget(main_box)

        self.NewDialog.open()


    def close(self, *instanse):
        self.NewDialog.dismiss()


    def create(self, *instanse):
        self.NewDialog.dismiss()


    def add_word_func(self):
        self.add_book_dialog()

