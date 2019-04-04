import sys

from kivy.app import App
from kivy.core.window import Window
from kivy.uix.button import Button

from game import Game

class Application(App):
    def build(self):
        self.title = "Mario 9000"
        self.game = Game()
        return self.game

if __name__ == "__main__":
    Application().run()

# TODO: Level parser
