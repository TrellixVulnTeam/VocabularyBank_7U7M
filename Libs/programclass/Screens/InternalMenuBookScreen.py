from pprint import pprint
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
            title_align='center',
            size=(400,310),
            auto_dismiss=False,
            separator_color='#FEF9F5',
        )
        main_box = BoxLayout(
            orientation="vertical",
            size_hint=(0.95,0.95)
        )
        in_main_box_top = BoxLayout(
            orientation="vertical",
            size_hint=(1,0.8)
        )

        word_box = BoxLayout(
            size_hint_x= 0.98,
            size_hint_y= 0.2,
            orientation = 'horizontal'
            )
        translate_box = BoxLayout(
            size_hint_x= 0.98,
            size_hint_y= 0.2,
            orientation = 'horizontal'
            )
        transcription_box = BoxLayout(
            size_hint_x= 0.98,
            size_hint_y= 0.2,
            orientation = 'horizontal'
            )
        asociation_box = BoxLayout(
            size_hint_x= 0.98,
            size_hint_y= 0.2,
            orientation = 'horizontal'
            )



        in_main_box_bottom = BoxLayout(
            orientation="horizontal",
            size_hint=(0.95,0.2)
        )

        self.text_input_word = MDTextField(
            pos_hint={ 'center_x':0.5,'center_y':0.5 },
            size_hint=(0.8,0.8),
            helper_text="Line is necessarily",
            helper_text_mode="on_error",
            hint_text="Necessarily",
            current_hint_text_color='#706B67',
            foreground_color="#FEF9F5",
        )

        self.text_input_translate = MDTextField(
            pos_hint={ 'center_x':0.5,'center_y':0.5 },
            size_hint=(0.8,0.8),
            helper_text="Line is necessarily",
            helper_text_mode="on_error",
            hint_text="Necessarily",
            current_hint_text_color='#706B67',
            foreground_color="#FEF9F5",
        )
        
        self.text_input_transcription = MDTextField(
            pos_hint={ 'center_x':0.5,'center_y':0.5 },
            size_hint=(0.8,0.8),
            hint_text="Not necessarily",
            current_hint_text_color='#706B67',
            foreground_color="#FEF9F5"
        )

        self.text_input_asociation = MDTextField(
            pos_hint={ 'center_x':0.5,'center_y':0.5 },
            size_hint=(0.8,0.8),
            hint_text="Not necessarily",
            current_hint_text_color='#706B67',
            foreground_color="#FEF9F5",
        )

        word_box.add_widget(
            MDLabel(
                theme_text_color="Custom",
                text_color="#FEF9F5",
                pos_hint={ 'center_x':0.5,'center_y':0.5 },
                size_hint=(0.3,0.2),
                text="Word",
                font_name= "Comic"
                )
        )
        translate_box.add_widget(
            MDLabel(
                theme_text_color="Custom",
                text_color="#FEF9F5",
                pos_hint={ 'center_x':0.5,'center_y':0.5 },
                size_hint=(0.3,0.2),
                text="translate",
                font_name= "Comic"
            )
        ) 
        transcription_box.add_widget(
            MDLabel(
                theme_text_color="Custom",
                text_color="#FEF9F5",
                pos_hint={ 'center_x':0.5,'center_y':0.5 },
                size_hint=(0.3,0.2),
                text="transcription",
                font_name= "Comic"
            )
        )
        asociation_box.add_widget(
            MDLabel(
                theme_text_color="Custom",
                text_color="#FEF9F5",
                pos_hint={ 'center_x':0.5,'center_y':0.5 },
                size_hint=(0.3,0.2),
                text="asociation",
                font_name= "Comic"
            )
        )


        word_box.add_widget( self.text_input_word )
        translate_box.add_widget( self.text_input_transcription )
        transcription_box.add_widget( self.text_input_translate )
        asociation_box.add_widget( self.text_input_asociation )


        in_main_box_top.add_widget(word_box)
        in_main_box_top.add_widget(translate_box)
        in_main_box_top.add_widget(transcription_box)
        in_main_box_top.add_widget(asociation_box)

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

        close_but.bind(on_release=self.close)
        ok_but.bind(on_release=self.create)




        in_main_box_bottom.add_widget( close_but )
        in_main_box_bottom.add_widget( ok_but )

        main_box.add_widget( in_main_box_top )
        main_box.add_widget( in_main_box_bottom )

        self.NewDialog.add_widget(main_box)

        self.NewDialog.open()


    def create_new_word(self,data):
        conn = sqlite3.connect("Data/Base/Books.db")
        cursor = conn.cursor()
        #cursor.execute("INSERT INTO")
        conn.close()


    def close(self, *instanse):
        self.NewDialog.dismiss()


    def create(self, *instanse):
        data = []
        data.append(self.text_input_word.text)
        data.append(self.text_input_transcription.text)
        data.append(self.text_input_translate.text)
        data.append(self.text_input_asociation.text)

        if self.check_is_valid(data):
            self.create_new_word(data)

        pprint(data)

        self.NewDialog.dismiss()


    def add_word_func(self):
        self.add_book_dialog()


