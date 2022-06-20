from pprint import pprint
from this import d
from kivy.uix.gridlayout import GridLayout
from kivy.properties import VariableListProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.relativelayout import RelativeLayout


class WordsList(GridLayout):
    WordsInterval = VariableListProperty([30,30])
