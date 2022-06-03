from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.relativelayout import RelativeLayout

from kivy.config import Config


class MainInterface(App):
    def build(self):
        button_names = [
        ] 

        main_layout = RelativeLayout(size =(800, 600))

        buttons = [
            "Setings",
            "Add Words",
            "Edit Words",
            "Shafle Learn",
            "Timer Learn"
        ]
        h_layout = BoxLayout()



        main_layout.add_widget(h_layout)
        return main_layout


    def on_button_press(self, instance):
        print(instance.text)


if __name__ == "__main__":
    MainInterface().run()