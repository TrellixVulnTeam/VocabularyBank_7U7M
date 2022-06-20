
from msilib.schema import UIText
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import VariableListProperty,ColorProperty,DictProperty,StringProperty
from kivymd.font_definitions import theme_font_styles
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.button import MDFlatButton


from kivy.uix.popup import Popup

from pprint import pprint


class CustomList(BoxLayout):
    WordsInterval = VariableListProperty([20,20])
    text_color_miss = ColorProperty("#000D26")
    
    Label_font_style = StringProperty('Subtitle2')
    Label_font_size = StringProperty("17")

    Label_menu_texts = DictProperty({
            "word": '[miss]',
            "translate": '[miss]',
            "transcription": '[miss]',
            "status": '[miss]',
            "asociations": '[miss]',
        })


    def reset_word_menu(self,*instanse):
        pass

    def reset_transcription_menu(self,*instanse):
        pass

    def reset_asociations_menu(self,*instanse):
        pass

    def reset_status_menu(self,*instanse):
        pass

    def reset_translate_menu(self,*instanse):
        pass

    def rewrite_word(self,word):
        # word.children = ['',
        # "[ref=''][miss][/ref]",
        # "[ref='']0[/ref]",
        # "[ref=''][miss][/ref]",
        # "[ref='']дерево[/ref]",
        # 'new tree']
        print(word.children[-1].text)


    def close(self, *instanse):
        self.reset_menu.dismiss()


    def create(self, *instanse):
        self.reset_menu.dismiss()