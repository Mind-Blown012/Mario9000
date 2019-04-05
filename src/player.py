from kivy.uix.floatlayout import FloatLayout
from kivy.graphics import Rectangle
from kivy.clock import Clock
from kivy.properties import NumericProperty

from mathf import RigidBody2D, Rectanglef, Vector2f

class Player(FloatLayout):
    """Contains player sprite and movement logic."""

    def __init__(self, inital_position=(0,0), **kwargs):
        """Initalizes position.

        Args:
            inital_position: two element tuple for the player's inital position
        """
        # Calling the base class (BoxLayout) __init__ method with **kwargs
        super(Player,self).__init__(**kwargs)

        # Initalizing the player's rigidbody with a rectangle (AABB) collider
        collider = Rectanglef(position=Vector2f(inital_position), size=\
                                Vector2f((60,60)))
        self.rb = RigidBody2D(collider)

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
        amount = 4

        if 'a' in keys:
            # Calling with -amount since A should move the player backwards
            self.rb.velocity.x = -amount
        if 'd' in keys:
            # Calling with positive amount this time since D should move the
            # player forward.
            self.rb.velocity.x = amount

    def PhysicsUpdate(self, dt):
        """Does all of the physics calculations.

        Runs AFTER Update has changed the player's
        properties.

        Args:
            dt: float delta-time, the amount of time that passed between the last frame and this one.
        """
        self.rb.Update(dt)
        self.pos = tuple(self.rb.position)
