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
            blocks: one dimensional array of blocks for the level,
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
        self.player = Player()
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
        collider = Rectanglef(position = Vector2f())
        self.rb = RigidBody2D()

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
        # Retreiving level data
        level_data = level["data"]
        # Changing data to be formatted in [x][y] instead of [y][x]
        level_data = load_blocks(level_data)
        # Finally, positioning the blocks to their correct locations
        level_data = position_blocks(level_data)
        # Appending to result a new level with
        # level_name and the correct data
        result.append(Level(level_data, name=level_name))

    return result

def position_blocks(block_arr: List):
    """Positions the blocks correctly.

    It will take the blocks position in the array,
    and multiply it by Block.size.

    Args:
        block_arr: a two dimensional list of blocks [x][y]

    Returns:
        A one dimensional array of blocks positioned correctally
    """

    # Initalize the result to an empty list
    result = list()

    # Looping through all of the blocks on the x and y axes
    for x in range(len(block_arr)):
        for y in range(len(block_arr[0])):
            # Making sure that it is not an air block
            if block_arr[x][y] is not None:
                # Setting the block position by multiplying
                # the current x and y positions by the
                # block size.
                block_arr[x][y].x = x*Block.block_size[0]
                block_arr[x][y].y = y*Block.block_size[1]
                # Appending the block with the correct position to result
                result.append(block_arr[x][y])

    return result
# TODO: Take out (x,y) formula and replace with flat array, since that is now what Level.__init__ takes in
def load_blocks(block_data: List):
    """Converts [y][x] blocks to [x][y].

    Also converts block names into their
    respective blocks.

    Args:
        block_data: array of blocks in above format

    Returns:
        2 dimensional array representing blocks arranged in x,y from [0,0]
    """

    # Setting the width and height to the dimensions of the array
    width = len(block_data[0])
    height = len(block_data)

    # Initalizing the 2D result array to the [width][height]
    result = [[None for y in range(height)] for x in range(width)]

    # Looping through the dictionary
    for y in range(len(block_data)):
        for x in range(len(block_data[0])):
            # Setting the current [x][y] value of result to
            # the [y][x] value of block_data
            result[x][y] = block_data[y][x]

    # Looping through all of the data
    # and converting it to blocks
    for x in range(len(result)):
        for y in range(len(result[0])):
            # Making sure that it is not an air block
            if result[x][y] != "None":
                result[x][y] = Block(result[x][y])
            else:
                # Set result (x,y) to python None instead of "None"
                result[x][y] = None

    return result
