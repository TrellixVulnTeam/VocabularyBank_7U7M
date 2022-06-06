from multiprocessing.dummy import active_children
from unicodedata import name

import kivy
from kivymd.app import MDApp
from kivy.lang.builder import Builder
from kivy.uix.screenmanager import Screen, ScreenManager


kv = '''
#:import get_color_from_hex kivy.utils.get_color_from_hex
#:import GridLayout kivy.uix.gridlayout

ScreenManager:
    MenuScreen:
    StatisticScreen:
    BooksScreen:
    EdittingScreen:
 
<MySwiper@MDSwiperItem>
    BoxLayout:
        Button:
            text: "hi"


<BooksScreen>:
    name: 'books'

    BoxLayout:
        id: toolbar
        pos_hint: {"top": 1}
        orientation: 'horizontal'
        size_hint_y: 0.08
        size_hint_x: 1
        
        BoxLayout:
            pos_hint: {"bottom": 1}
            size_hint_y: 0.9
            size_hint_x: 0.96
 
            MDIconButton:
                id: Settings
                icon: "cog-outline"
                user_font_size: "32sp"

                pos_hint: {"left":1, 'center_x': 0.9,'center_y': 0.5}

            MDLabel:
                id: Random_word
                size_hint: 0.6, 1
                text: "This is a BooksScreen"
                font_style: "H5"
                    
                pos_hint: {'center_x': 0.5, 'center_y': 0.5}


            MDIconButton:
                id: Localization
                icon: "earth"

                user_font_size: "32sp"
                pos_hint: {"right":1, 'center_x': 0.9,'center_y': 0.5}
    BoxLayout:
        id: bottom_navigation
        size_hint_y: 0.08
        size_hint_x: 1
        
        #panel_color: get_color_from_hex("#eeeaea")
        #selected_color_background: get_color_from_hex("#97ecf8")
        #text_color_activate: 0, 0, 0, 1
        BoxLayout:
            size_hint_x: 0.35
            pos_hint: {'center_x': 0.5, 'center_y': 0.5}
            MDIconButton: 
                id: Start
                icon: "menu"
                user_font_size: '42sp'
                on_release: 
                    root.manager.current = 'menu'

        BoxLayout
            canvas:
                Color:
                    rgba: 151, 236, 248, 1
                Rectangle:
                    pos: self.pos
                    size: self.size



            BoxLayout
            
                pos_hint: {'center_x': 0.5, 'center_y': 0.5}
                MDIconButton:
                    id: Statistic
                    icon: "chart-areaspline"
                    user_font_size: '34sp'
                    on_release: 
                        root.manager.current = 'statistic'

            BoxLayout:

                pos_hint: {'center_x': 0.5, 'center_y': 0.5}
                MDIconButton:
                    id: Books
                    icon: "bookshelf"
                    user_font_size: '34sp'
                    on_release: 
                        root.manager.current = 'books'

            BoxLayout:

                pos_hint: {'center_x': 0.5, 'center_y': 0.5}
                MDIconButton:
                    id: Edit      
                    icon: "contrast"
                    user_font_size: '34sp'
                    on_release:
                        root.manager.current = 'edit'



<EdittingScreen>:
    name: 'edit'

    BoxLayout:
        id: toolbar
        pos_hint: {"top": 1}
        orientation: 'horizontal'
        size_hint_y: 0.08
        size_hint_x: 1
        
        BoxLayout:
            pos_hint: {"bottom": 1}
            size_hint_y: 0.9
            size_hint_x: 0.96
 
            MDIconButton:
                id: Settings
                icon: "cog-outline"
                user_font_size: "32sp"

                pos_hint: {"left":1, 'center_x': 0.9,'center_y': 0.5}

            MDLabel:
                id: Random_word
                size_hint: 0.6, 1
                text: "This is a EdittingScreen"
                font_style: "H5"
                    
                pos_hint: {'center_x': 0.5, 'center_y': 0.5}


            MDIconButton:
                id: Localization
                icon: "earth"

                user_font_size: "32sp"
                pos_hint: {"right":1, 'center_x': 0.9,'center_y': 0.5}
    BoxLayout:
        id: bottom_navigation
        size_hint_y: 0.08
        size_hint_x: 1
        
        #panel_color: get_color_from_hex("#eeeaea")
        #selected_color_background: get_color_from_hex("#97ecf8")
        #text_color_activate: 0, 0, 0, 1
        BoxLayout:
            size_hint_x: 0.35
            pos_hint: {'center_x': 0.5, 'center_y': 0.5}
            MDIconButton: 
                id: Start
                icon: "menu"
                user_font_size: '42sp'
                on_release: 
                    root.manager.current = 'menu'

        BoxLayout
            canvas:
                Color:
                    rgba: 151, 236, 248, 1
                Rectangle:
                    pos: self.pos
                    size: self.size



            BoxLayout
            
                pos_hint: {'center_x': 0.5, 'center_y': 0.5}
                MDIconButton:
                    id: Statistic
                    icon: "chart-areaspline"
                    user_font_size: '34sp'
                    on_release: 
                        root.manager.current = 'statistic'

            BoxLayout:

                pos_hint: {'center_x': 0.5, 'center_y': 0.5}
                MDIconButton:
                    id: Books
                    icon: "bookshelf"
                    user_font_size: '34sp'
                    on_release: 
                        root.manager.current = 'books'

            BoxLayout:

                pos_hint: {'center_x': 0.5, 'center_y': 0.5}
                MDIconButton:
                    id: Edit      
                    icon: "contrast"
                    user_font_size: '34sp'
                    on_release:
                        root.manager.current = 'edit'



<StatisticScreen>:
    name: 'statistic'

    BoxLayout:
        id: toolbar
        pos_hint: {"top": 1}
        orientation: 'horizontal'
        size_hint_y: 0.08
        size_hint_x: 1
        
        BoxLayout:
            pos_hint: {"bottom": 1}
            size_hint_y: 0.9
            size_hint_x: 0.96
 
            MDIconButton:
                id: Settings
                icon: "cog-outline"
                user_font_size: "32sp"

                pos_hint: {"left":1, 'center_x': 0.9,'center_y': 0.5}

            MDLabel:
                id: Random_word
                size_hint: 0.6, 1
                text: "This is a StatisticScreen"
                font_style: "H5"
                    
                pos_hint: {'center_x': 0.5, 'center_y': 0.5}


            MDIconButton:
                id: Localization
                icon: "earth"

                user_font_size: "32sp"
                pos_hint: {"right":1, 'center_x': 0.9,'center_y': 0.5}
    BoxLayout:
        id: bottom_navigation
        size_hint_y: 0.08
        size_hint_x: 1
        
        #panel_color: get_color_from_hex("#eeeaea")
        #selected_color_background: get_color_from_hex("#97ecf8")
        #text_color_activate: 0, 0, 0, 1
        BoxLayout:
            size_hint_x: 0.35
            pos_hint: {'center_x': 0.5, 'center_y': 0.5}
            MDIconButton: 
                id: Start
                icon: "menu"
                user_font_size: '42sp'
                on_release: 
                    root.manager.current = 'menu'

        BoxLayout
            canvas:
                Color:
                    rgba: 151, 236, 248, 1
                Rectangle:
                    pos: self.pos
                    size: self.size



            BoxLayout
            
                pos_hint: {'center_x': 0.5, 'center_y': 0.5}
                MDIconButton:
                    id: Statistic
                    icon: "chart-areaspline"
                    user_font_size: '34sp'
                    on_release: 
                        root.manager.current = 'statistic'

            BoxLayout:

                pos_hint: {'center_x': 0.5, 'center_y': 0.5}
                MDIconButton:
                    id: Books
                    icon: "bookshelf"
                    user_font_size: '34sp'
                    on_release: 
                        root.manager.current = 'books'

            BoxLayout:

                pos_hint: {'center_x': 0.5, 'center_y': 0.5}
                MDIconButton:
                    id: Edit      
                    icon: "contrast"
                    user_font_size: '34sp'
                    on_release:
                        root.manager.current = 'edit'


<MenuScreen>:
    name: 'menu'

    BoxLayout:
        id: toolbar
        pos_hint: {"top": 1}
        orientation: 'horizontal'
        size_hint_y: 0.08
        size_hint_x: 1
        
        BoxLayout:
            pos_hint: {"bottom": 1}
            size_hint_y: 0.9
            size_hint_x: 0.96
 
            MDIconButton:
                id: Settings
                icon: "cog-outline"
                user_font_size: "32sp"

                pos_hint: {"left":1, 'center_x': 0.9,'center_y': 0.5}

            MDLabel:
                id: Random_word
                size_hint: 0.6, 1
                text: "This is a plays for rand word"
                font_style: "H5"
                    
                pos_hint: {'center_x': 0.5, 'center_y': 0.5}


            MDIconButton:
                id: Localization
                icon: "earth"

                user_font_size: "32sp"
                pos_hint: {"right":1, 'center_x': 0.9,'center_y': 0.5}

    
    MDSwiper:
        pos_hint: {'center_x': 0.5, 'center_y': 0.5}
        size_hint_y: 0.82
        height: root.height - toolbar.height - dp(40)
        y: root.height - self.height - toolbar.height - dp(20)

        MySwiper:

        MySwiper:

    BoxLayout:
        id: bottom_navigation
        size_hint_y: 0.08
        size_hint_x: 1
        
        #panel_color: get_color_from_hex("#eeeaea")
        #selected_color_background: get_color_from_hex("#97ecf8")
        #text_color_activate: 0, 0, 0, 1
        BoxLayout:
            size_hint_x: 0.35
            pos_hint: {'center_x': 0.5, 'center_y': 0.5}
            MDIconButton: 
                id: Start
                icon: "menu"
                user_font_size: '42sp'
                on_release: 
                    root.manager.current = 'menu'

        BoxLayout
            canvas:
                Color:
                    rgba: 151, 236, 248, 1
                Rectangle:
                    pos: self.pos
                    size: self.size



            BoxLayout
            
                pos_hint: {'center_x': 0.5, 'center_y': 0.5}
                MDIconButton:
                    id: Statistic
                    icon: "chart-areaspline"
                    user_font_size: '34sp'
                    on_release: 
                        root.manager.current = 'statistic'

            BoxLayout:

                pos_hint: {'center_x': 0.5, 'center_y': 0.5}
                MDIconButton:
                    id: Books
                    icon: "bookshelf"
                    user_font_size: '34sp'
                    on_release: 
                        root.manager.current = 'books'

            BoxLayout:

                pos_hint: {'center_x': 0.5, 'center_y': 0.5}
                MDIconButton:
                    id: Edit      
                    icon: "contrast"
                    user_font_size: '34sp'

                    theme_text_color: 'Custom'
                    #text_color: 1,0,0,1

                    on_release:
                        root.manager.current = 'edit'

'''
#user_font_size: "38sp"


active_navigete_name = 'menu'

class MenuScreen(Screen):
    pass

class StatisticScreen(Screen):
    pass

class BooksScreen(Screen):
    pass

class EdittingScreen(Screen):
    pass




sm = ScreenManager()

sm.add_widget(MenuScreen(name="menu"))
sm.add_widget(StatisticScreen(name="statistic"))
sm.add_widget(EdittingScreen(name="edit"))
sm.add_widget(BooksScreen(name="books"))

class Main(MDApp):
    def build(self):
        return Builder.load_string(kv)

Main().run()