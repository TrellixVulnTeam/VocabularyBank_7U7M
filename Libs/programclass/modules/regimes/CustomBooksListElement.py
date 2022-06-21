from pprint import pprint
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import VariableListProperty


class CustomBooksListElement(BoxLayout):
    
    WordsInterval = VariableListProperty([20,20])

    def write_infor(self,data):
        self.children[0].children[2].text = data[0]
        self.children[0].children[1].text = str(data[1])
