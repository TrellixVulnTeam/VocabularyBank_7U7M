from pprint import pprint

from kivy.uix.boxlayout import BoxLayout
from kivy.animation import Animation
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.boxlayout import BoxLayout

from kivy.properties import StringProperty

from kivymd.uix.button import MDFlatButton

import random


class BattonBoxLayout(ButtonBehavior, BoxLayout):
    bg_color = StringProperty("FFFFE4")


class RestartButton(MDFlatButton):
    pass



class SimpleRegime(BoxLayout):
    visited_word_indexs = []
    indexs = []
    is_binded_animation = False

    animations = {
        'win': Animation(
            but_color=(167/255.0,255/255.0,100/255.0,1),
            duration=0.25,
            t='out_back',
        ) + Animation(
            but_color=(255/255.0, 255/255.0, 157/255.0, 1),
            duration=0.1,
        ),

        'lose': Animation(
            but_color=(226/255.0,43/255.0,43/255.0,1),
            duration=0.25,
            t='out_back',
        ) + Animation(
            but_color=(255/255.0, 255/255.0, 157/255.0, 1),
            duration=0.1,
        ),
    }


    def animation_boxbut(self,status,widget):
        if status in self.animations.keys():
            self.animations[status].start(widget)


    def win_event(self,widget):
        pprint(f"{widget.children[0].text} == {widget.data}")
        self.animation_boxbut('win',widget)


    def lose_event(self,widget):
        pprint("lose")
        self.animation_boxbut('lose',widget)


    def go_to_writed(self,*args):
        self.write_random(self.data_base_data,self.data_base_data_max_len,0)


    def chek_valid(self,widget,*data_of_tried):
        if not self.is_binded_animation:
            for item in self.animations.keys():
                self.animations[item].bind(
                    on_complete=self.go_to_writed         
                )
            self.is_binded_animation = True


        if (widget.children[0].text == widget.data[0] or widget.children[0].text == widget.data[1]):
            self.win_event(widget)
        else: 
            self.lose_event(widget)


    def write_random(self,data,lens,status):
        if status == 0:
            print(type(lens))
            print(type(data))

            self.tried_word = random.randint(0,lens-1)
            while self.tried_word in self.visited_word_indexs:
                self.tried_word = random.randint(0,lens-1)
              
            self.visited_word_indexs.append(self.tried_word)
            if len(self.visited_word_indexs) == lens:
                self.visited_word_indexs = []
            self.indexs = [i for i in range(lens) if i != self.tried_word]
            random.shuffle(self.indexs)
            pprint((self.indexs,self.tried_word))

            self.tried_word_data = data[self.tried_word]
            self.add_infor_in_learn_pool(self.tried_word,data)



    def add_infor_in_learn_pool(self,index,data,inverse=False):
        data_pointer = (0,1)
        if inverse == True:
            data_pointer = (1,0)

        # set data arrgs for butbox objs

        setattr(self.ids.top_left, "data", self.tried_word_data)
        setattr(self.ids.top_right, "data", self.tried_word_data)
        setattr(self.ids.bottom_left, "data", self.tried_word_data)
        setattr(self.ids.bottom_right, "data", self.tried_word_data)

        self.ids.word.children[0].text = data[index][data_pointer[0]]

        real_index = random.randint(0,3)
        if real_index != 0:
            self.ids.top_left.children[0].text = data[self.indexs[0]][data_pointer[1]]
        else:
            self.ids.top_left.children[0].text = data[index][data_pointer[1]]
            

        if real_index != 1:
            self.ids.top_right.children[0].text = data[self.indexs[1]][data_pointer[1]]
        else:
            self.ids.top_right.children[0].text = data[index][data_pointer[1]]


        if real_index != 2:
            self.ids.bottom_left.children[0].text = data[self.indexs[2]][data_pointer[1]]
        else:
            self.ids.bottom_left.children[0].text = data[index][data_pointer[1]]


        if real_index != 3:
            self.ids.bottom_right.children[0].text = data[self.indexs[3]][data_pointer[1]]
        else:
            self.ids.bottom_right.children[0].text = data[index][data_pointer[1]]


