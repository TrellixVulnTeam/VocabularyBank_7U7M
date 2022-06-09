
from kivymd.app import MDApp
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.lang.builder import Builder
from kivy.uix.button import Button
from kivy.uix.popup import Popup

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
    Button:
        text: "add"
        size_hint_x: 0.2
        size_hint_y: 0.2
        pos_hint: {"top":1}
        on_release: app.on_button_press()

    BoxLayout:
        id: pool
        pos_hint: {"bottom":1}

        size_hint_x: 0.8
        size_hint_y: 0.8

'''

class Screen1(Screen):
    pass

class Screen2(Screen):
    pass




class MainAPP(MDApp):
    def build(self):
        Builder.load_string(kv)
        sm = ScreenManager()
        sm.add_widget(Screen1(name="s1"))
        sm.add_widget(Screen2(name="s2"))
        return sm


    def on_button_press(self, *instance):
        NewDialog = Popup(
            title="",
            size_hint=(None,None),
            size=(220,220),
        )
        NewDialog.open()



if __name__ == "__main__":
    MainAPP().run()