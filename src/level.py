from typing import List
import json

from kivy.uix.screenmanager import Screen
from kivy.uix.floatlayout import FloatLayout
from kivy.properties import StringProperty
from kivy.properties import ListProperty

from mathf import RigidBody2D, Rectanglef, Vector2f
from player import Player

class Level(Screen):
    """Contains all blocks in current level and player."""
    # Using a list property so that the player can access them for collision
    # through self.parent
    blocks = ListProperty()

    def __init__(self, blocks, **kwargs):
        """Adds all blocks to the level.

        Sets up Camera. (not yet!)

        Args:
            blocks: set of blocks for the level,
                    all positioned correctly
            **kwargs: anything that needs to be passed into
                      base class Screen
        """
        # Calling the base class (Screen) __init__ method with **kwargs
        super(Level,self).__init__(**kwargs)

        # Setting root widget since a screen can't
        # have multiple widgets
        root_wid = FloatLayout()

        # Looping through all of the blocks...
        for block in blocks:
            # Making sure that it is not an air block
            if block is not None:
                # ...and adding them to root_wid
                root_wid.add_widget(block)
                # Appending all of the blocks to the ListProperty blocks
                self.blocks.append(block)

        # Creating a player and adding it to root_wid
        self.player = Player((0,120)) # HACK: Testing player's position at 61
        root_wid.add_widget(self.player)

        self.add_widget(root_wid)

    def Update(self, dt):
        """Calls Player.Update(). And then Player.PhysicsUpdate()

        Args:
            dt: delta-time, (1/60)-(amount of time that actually passed)
        """
        # Calling player.Update with currently pressed keys
        self.player.Update(self.parent.keys)
        self.player.PhysicsUpdate(dt)

class Block(FloatLayout):
    """Contains sprite for block."""
    file_name = StringProperty("./res/blocks/invalid.png")
    # The size of every block
    block_size = [30,30]

    def __init__(self, name: str, **kwargs):
        """Sets up block to use file image passed in with name.

        IMPORTANT: must pass in size to **kwargs, can't change it later.

        Args:
            name: string, name of the block representing the end of the filename
                  (ex. file is 'block_dirt.png' name is 'dirt') also supports
                  passing in full filename.
            **kwargs: any arguments that need to be passed into base class
                      BoxLayout
        """
        self.hi = "hi"
        # Calling the base class (FloatLayout) __init__ method with **kwargs
        # not using super so that it will not interfere with RigidBody2D
        super().__init__(**kwargs)

        # Creating a collider and RigidBody2D for each block
        collider = Rectanglef(position = Vector2f(self.pos), size = \
                                Vector2f(self.size))
        self.rb = RigidBody2D(collider)

        # Disabling size hint
        self.size_hint_x = None
        self.size_hint_y = None

        # Setting size to block size
        self.size = Block.block_size

        # Check to see how the user passed in name, and format it correctly
        # depending on that
        if ".png" in name:
            self.file_name = "./res/blocks/"+name
        else:
            # TODO: Support passing in full filepath
            self.file_name = "./res/blocks/"+name+".png"

def load_levels():
    """Loads levels found in file 'levels.json'

    Takes the name and data from the level in the
    json file and then parses it.

    Returns:
        An array of levels in the seqental order of how they are found in the
        json file

    Raises:
        ioerror: could not find 'levels.json' or error reading it.
    """
    # TODO: load levels through images and implement level editor

    # The resullt is a list of levels
    result = list()

    data = None

    # Opening the 'levels.json' file in read mode
    # and converting it to a python dict
    with open("./res/levels.json", "r") as file:
        data = json.load(file)

    for level in data:
        # Retreiving the level name
        level_name = level["name"]
        # Retreiving temporary level data
        _level_data = level["data"]
        # Converting the format of the block array into a flat array, and
        # positioning each block into the correct location.
        level_data = load_blocks(_level_data)
        # Appending to result a new level with
        # level_name and the correct data
        result.append(Level(level_data, name=level_name))

    return result

def load_blocks(block_data: List):
    """Converts [y][x] blocks to [x][y].

    Also converts block names into their
    respective blocks.

    Args:
        block_data: array of blocks in above format

    Returns:
        2 dimensional array representing blocks arranged in x,y from [0,0]
    """
    def position_block(x_pos, y_pos):
        """Positions a block according to it's x and y positions in the array.

        Returns:
            A tuple representing the blocks (x,y) position.
        """
        # Multiply the x/y positions by the width/height of a block
        x_pos = x_pos*Block.block_size[0]
        y_pos = y_pos*Block.block_size[1]
        return x_pos, y_pos
    # First, reverse the list since it comes in the incorrect order.
    # (only the first dimension)
    block_data = list(reversed(block_data))

    # Initalizing the one dimensional array (set)
    result = set()

    # Loop through the 2D list:
    for y in range(len(block_data)):
        for x in range(len(block_data[0])):
            # Four steps:
            #   1. Get text at current position in list
            #   2. Get correct position, in kivy coordinates.
            #   3. Create a `Block` with the correct position
            #   4. Add the block to result.
            text = block_data[y][x]
            # If "None", don't put a block there! (skip)
            if text == "None":
                continue
            # Get the block position
            block_pos = position_block(x, y)
            block = Block(text, pos=block_pos)
            result.add(block)
    return result
