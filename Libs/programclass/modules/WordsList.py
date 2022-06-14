from kivy.uix.gridlayout import GridLayout
from kivy.properties import VariableListProperty
from kivy.uix.boxlayout import BoxLayout


class WordsList(GridLayout):
    WordsInterval = VariableListProperty([30,30])