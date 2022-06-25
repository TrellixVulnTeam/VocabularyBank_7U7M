
from kivymd.app import MDApp
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.lang.builder import Builder
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout

kv = '''
#:import hex kivy.utils.get_color_from_hex

BoxLayout:
    spacing: 30
    orientation: 'vertical'
    size_hint_x: 0.82
    size_hint_y: 0.8
    pos_hint: {"center_x":0.5,"center_y":0.5}
    BoxLayout:
        canvas:
            Color:
                rgba: hex("#F6F6C4")
            Rectangle:
                pos: self.pos
                size: self.size
        size_hint_x: 1
        size_hint_y: 0.2
        pos_hint: {'top':1}
        MDLabel:

    BoxLayout:
        spacing: 20
        pos_hint: {'bottom':1}
        size_hint_x: 1
        size_hint_y: 0.76
        orientation: "vertical"
        BoxLayout:
            spacing: 20

            pos_hint: {"center_y": 0.25}
            size_hint_y: 0.46
            size_hint_x: 1
            orientation: 'horizontal'
            BoxLayout:
                canvas:
                    Color:
                        rgba: hex("#F6F6C4")
                    Rectangle:
                        pos: self.pos
                        size: self.size
                id: top_left

            BoxLayout:
                canvas:
                    Color:
                        rgba: hex("#F6F6C4")
                    Rectangle:
                        pos: self.pos
                        size: self.size
                id: top_right


        BoxLayout:
            spacing: 20

            pos_hint: {"center_y": 0.75}
            size_hint_y: 0.46
            size_hint_x: 1
            orientation: "horizontal"
            BoxLayout:
                canvas:
                    Color:
                        rgba: hex("#F6F6C4")
                    Rectangle:
                        pos: self.pos
                        size: self.size
                id: bottom_left

            BoxLayout:
                canvas:
                    Color:
                        rgba: hex("#F6F6C4")
                    Rectangle:
                        pos: self.pos
                        size: self.size
                id: bottom_right

    

'''






class MainAPP(MDApp):
    list_buttons = []

    def build(self):
        return Builder.load_string(kv)




if __name__ == "__main__":
    MainAPP().run()