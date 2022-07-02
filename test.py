from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button

from kivy.properties import (
    NumericProperty, ReferenceListProperty, ObjectProperty, StringProperty, ListProperty
)
from kivy.lang import Builder

kv = """
#:import hex kivy.utils.get_color_from_hex

<CustomButton>:
    size_hint_x: 0.8
    size_hint_y: 0.2
    text: root.name
    center_x: root.width / 2
    font_size: 30
    on_release: root.callback(self,self.parent)


<Testwidget>:
    id: object_for_scroll
    size_hint_y: 2
    cols: 1

<Main>:
    canvas:
        Color:
            rgba: hex('#777576')
        Rectangle:
            pos: self.pos
            size: self.size
    size_hint: 1,1
    ScrollView:
        id: buttons_layout
        size_hint_x: 0.9
        size_hint_y: 0.82
        pos_hint: {'center_x': 0.5, 'center_y': 0.5}

"""   
class Main(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.buttons_pool = Testwidget()


        text = "name\n"*20
        # you can go for taple or list its dosnt mater
        for index,but_text in enumerate(text.split("\n")):
            but = CustomButton() # create obj and set his parameters of text ( also you can set any parameter )
            setattr(but, "name", but_text+str(index)) # index is name for example, you can put any one

            # add into the pool
            setattr(self.buttons_pool,"size_hint_y", index//5+1)
            self.buttons_pool.add_widget(but)


        self.ids.buttons_layout.add_widget(self.buttons_pool)


class CustomButton(Button):
    name = StringProperty()
    def callback(self, widget ,pool):
        pool.remove_widget(widget)


class Testwidget(GridLayout):
    pass
 

class GuiApp(App):
    def build(self):
        Builder.load_string(kv)

        return Main()


if __name__ == '__main__':
    GuiApp().run()