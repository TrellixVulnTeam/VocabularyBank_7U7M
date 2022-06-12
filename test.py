
from kivymd.app import MDApp
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.lang.builder import Builder
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout

kv = '''
ScreenManager:
    Screen1:
    Screen2:


<Screen1>:
    name: 's1'
    Button:
        text: "swap"
        size_hint_x: 0.2
        size_hint_y: 0.2
        pos_hint: {"top":1}
        on_release: root.manager.current = 's2'


<Screen2>:
    name: 's2'
    BoxLayout:
        orientation: 'vertical'
        MDFlatButton:
            text: "add"
            size_hint_x: 0.2
            size_hint_y: 0.18
            pos_hint: {"top":1}
            on_release: app.add_button_press()

        ScrollView:
            size_hint_x: 0.9
            size_hint_y: 0.82
            MDList:





<add_list_element>:
    size_hint_y: 0.09
    size_hint_x: 0.9
    pos_hint: {"top":1}
    orientation: 'horizontal'
    Button:
        text: '1'
    Button:
        text: '2'
    Button:
        text: '3'

    

'''

class add_list_element(BoxLayout):
    pass


class Screen1(Screen):
    pass

class Screen2(Screen):
    pass




class MainAPP(MDApp):
    list_buttons = []

    def build(self):
        Builder.load_string(kv)
        sm = ScreenManager()
        sm.add_widget(Screen1(name="s1"))
        sm.add_widget(Screen2(name="s2"))
        return sm

    def del_button_press(self, *instance):
        for but in self.list_buttons:
            self.root.get_screen("s2").ids.pool.remove_widget(but)

    def add_button_press(self, *instance):
        print("a")
        but = add_list_element()
        #self.list_buttons.append(but)
        #self.root.get_screen("s2").ids.pool.add_widget(but)



if __name__ == "__main__":
    MainAPP().run()