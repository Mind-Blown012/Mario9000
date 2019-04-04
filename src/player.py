from kivy.uix.floatlayout import FloatLayout
from kivy.graphics import Rectangle
from kivy.clock import Clock
from kivy.properties import NumericProperty

class Player(FloatLayout):
    """Contains player sprite and movement logic."""

    # The x and y velocities of the player, defaulting to 0
    x_velocity = NumericProperty(0)
    y_velocity = NumericProperty(0)

    def __init__(self, inital_position=(0,0), **kwargs):
        """Initalizes position.

        Args:
            inital_position: two element tuple for the player's inital position
        """
        # Calling the base class (BoxLayout) __init__ method with **kwargs
        super(Player,self).__init__(**kwargs)

        # Disabling size_hint
        self.size_hint_x = None
        self.size_hint_y = None

        # Setting the player's position to the inital position
        self.pos = inital_position
        self.size = (60,60)

        # Setting the player movement speed
        self.speed = 200

    def Update(self, keys):
        """Handles key presses.

        Moves the player with keys A, D,
        and spacebar.

        Args:
            keys: the current keys that are pressed down
        """
        # Checking if A and/or D is pressed
        # if they are, call move.

        # Setting amount to delta-time * speed
        # and making sure that it is an integer
        amount = 0#round(dt*self.speed)

        if 'a' in keys:
            # Calling with -amount since A should move the player backwards
            self.move(-amount)
        if 'd' in keys:
            # Calling with positive amount this time since D should move the
            # player forward.
            self.move(amount)

        if "spacebar" in keys:
            self.jump(dt)

    def PhysicsUpdate(self, dt):
        """Does all of the physics calculations.

        Runs AFTER Update has changed the player's
        properties.

        Args:
            dt: float delta-time, the amount of time that passed between the last frame and this one.
        """


    def move(self, amount):
        """Moves the player a specified distance on the x axis.

        Moves one unit per tick so that collisions will be easy to check,
        since everything (for now) does not have decimal placement.

        Args:
            amount: an integer, representing the amount of distance to move.
        """

        # If amount is positive, then the player goes left, if negative
        # it is going right
        direction = ("right" if (amount > 0) else "left")

        # If there is currently a collision in the direction
        # that the player is going...
        if self.check_collision(direction):
            # Don't move, it should be impossible to
            return
        elif amount is 0:
            # either 0 is passed in, or the loop of movement has ended
            return
        else:
            # This function will keep looping until either:
            #   movement is over
            #   it is collided in the direction it is going
            next_move = amount-(1 if (direction is "right") else -1)
            Clock.schedule_once(lambda dt: self.move(next_move))
            # move 1/-1 per loop interval so it will never collide
            self.x += (1 if (direction is "right") else -1)

    def check_collision(self, direction: str):
        """Checks for collision(s) of block(s) in a certain direction.

        Args:
            direction: a string representing the diretion in which to check for
                       a collision ('right','left','up',or 'down')
        """
        # The set of blocks the player is currently colliding with
        collided_blocks = set()

        ########## Y is bottom, x is left ##########

        # Looping through all of the blocks in the current level:
        for block in self.parent.parent.blocks: # self -> root_wid -> level
            if self.collide_widget(block):
                ########## Taking out all of the diagonal blocks: ##########
                # using 'is' not '>=' since it should be impossible for the player to get inside of the block (right now, without camera)
                if self.right is block.x and self.y is block.top:
                    # diagonal right down
                    continue
                elif self.x is block.right and self.y is block.top:
                    # diagonal left down
                    continue
                elif self.right is block.x and self.top is block.y:
                    # diagonal right up
                    continue
                elif self.x is block.right and self.top is block.y:
                    # diagonal left up
                    continue

                # If it is not diagonal, add it to the set
                collided_blocks.add(block)

        # Looping through collided_blocks
        for block in collided_blocks:
            # Checking if the block is in that direction from the player,
            # if none of the blocks are, then return False
            if direction is "left":
                if self.x is block.right:
                    return True
            elif direction is "right":
                if self.right is block.x:
                    return True
            elif direction is "up":
                if self.top is block.y:
                    return True
            elif direction is "down":
                if self.y is block.top:
                    return True
            return False
