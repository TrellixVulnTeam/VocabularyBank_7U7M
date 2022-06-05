from kivymd.app import MDApp
from kivy.lang.builder import Builder


kv = '''
<MySwiper@MDSwiperItem>

    FitImage:
        source: "Data/Images/test_swiper.png"
        radius: [6,]

MDScreen:

    BoxLayout:
        id: toolbar
        pos_hint: {"top": 1}
        orientation: 'horizontal'
        size_hint_y: 0.07
        size_hint_x: 1



        MDIconButton:
            id: Settings
            icon: "cog-outline"
            user_font_size: "38sp"

            pos_hint: {"left":1, 'center_x': 0.9}

        MDLabel:
            id: Random_word
            padding: [0,10]
            size_hint: 0.6, 1
            text: "wordaadfafaafsfaafsfafasfsaff"
            font_style: "H4"
                
            pos_hint: {'center_x': 0.5, 'center_y': 0.5}


        MDIconButton:
            id: Localization
            icon: "earth"

            user_font_size: "38sp"
            pos_hint: {"right":1, 'center_x': 0.9}



    MDSwiper:
        pos_hint: {'center_x': 0.5, 'center_y': 0.5}
        size_hint_y: 0.8
        height: root.height - toolbar.height - dp(40)
        y: root.height - self.height - toolbar.height - dp(20)

        MySwiper:

        MySwiper:

    BoxLayout:
        id: toolbar
        pos_hint: {"bottom": 1}
        orientation: 'horizontal'
        size_hint_y: 0.07
        size_hint_x: 1

        MDIconButton:
            id: Statistic
            icon: "chart-areaspline"
            user_font_size: "38sp"

            pos_hint: {"left":1}

        MDIconButton:
            id: Books
            icon: "bookshelf"
            user_font_size: "38sp"

            pos_hint: {'center_y': 0.5, 'center_x': 0.5}

        MDIconButton:
            id: Edit
            icon: "contrast"
            user_font_size: "38sp"

            pos_hint: {"right":1}



'''


class Main(MDApp):
    def build(self):
        return Builder.load_string(kv)

Main().run()