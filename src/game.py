import sys

from kivy.uix.screenmanager import ScreenManager
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.core.window import Window
from kivy.clock import Clock

from level import Level, load_levels


class Game(ScreenManager):
    """Contains Levels and other gameplay screens."""
    def __init__(self, **kwargs):
        """Initalization method of game class.

        Binds keyboard methods _keyboard_closed, _keyup, and _keydown,
        sets up update function at 60 fps (every 1/60 of a second),
        initalizes a list for keys pressed, and sets up the levels.

        Args:
            **kwargs: anything needed for base class ScreenManager
        """
        # Calling the base class (ScreenManager) __init__ method with **kwargs
        super(Game, self).__init__(**kwargs)

        # Getting all keyboard functions binded
        # _keyboard_closed, _keyup _keydown
        self._keyboard = Window.request_keyboard(self._keyboard_closed, self)
        self._keyboard.bind(on_key_down=self._keydown,
                            on_key_up=self._keyup)

        # Set of currently pressed keys
        self.keys = set()

        # Loading all levels from json file
        self.levels = load_levels()

        # Looping through all of the levels and adding them
        for level in self.levels:
            self.add_widget(level)

        # Setting the current level to the first one
        self.current = self.levels[0].name

        # Scheduling the clock to run 'Update' every 1/60th of a second
        Clock.schedule_interval(self.Update, 1.0 / 60.0)

    def Update(self, dt):
        """Runs all update methods in children through recrusion."""
        # Updating current level
        self.current_screen.Update(dt)

    def _keyboard_closed(self):
        """Closes the keyboard and unbinds it."""
        # Unbinding keyboard
        self._keyboard.unbind(on_key_down=self._keydown,
                            on_key_up=self._keyup)
        # Setting keyboard to None
        self._keyboard = None

    def _keydown(self, keyboard, keycode, text, modifiers):
        """Adds to the key list whenever a key is pressed down."""
        # Only append if it is not already in the list
        if not keycode[1] in self.keys:
            self.keys.add(keycode[1]) # Using keycode[1] since keycode
                                      # looks like this (100, 'd')

    def _keyup(self, keyboard, keycode, *args):
        """Removes from the key list whenever a key is pulled down."""
        # Making sure that the key is in 'keys' so that remove does
        # not through an exception
        if keycode[1] in self.keys:
            self.keys.remove(keycode[1]) # Using keycode[1] since keycode
                                         # looks like this (100, 'd')
