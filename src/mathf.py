import math

# Downward acceleration due to gravity
# 9.8 meters per second per second or (m/s)^2
GRAVITY = -9.8

class Vector2f(object):
    """Vector2f: stores two floats, x and y, for easier creation of velocities and positions."""

    @property
    def x(self):
        """The x value of the Vector."""
        return self._x
    @x.setter
    def x(self, value):
        """The x value of the Vector.

        Args:
            value: a float, representing the x value of the vector."""
        self._x = float(value)

    @property
    def y(self):
        """The y value of the Vector."""
        return self._y
    @y.setter
    def y(self, value):
        """The y value of the Vector.

        Args:
            value: a float, representing the y value of the vector."""
        self._y = float(value)

    def __init__(self, convert_from=None, *, x=0, y=0):
        """"Initalizes x and y positions.

        Args:
            convert_from: a tuple, list, or array of length two representing a \
                            vector2.
            x: a float representing the x-coordinate of the vector.
            y: a float representing the y-coordinate of the vector.
        """
        self.x = x
        self.y = y

        # If `convert_from` is None then do nothing with it
        if convert_from is None:
            return
        # Setting the x and y to their positions in the list/tuple/array
        self.x = convert_from[0]
        self.y = convert_from[1]

    ########## OPERATORS ##########
    def __add__(self, other):
        """(+) Adds a vector and vector, or vector and scalar.

        Will add components of vectors, or a scalar to both components of
        the vector.

        Args:
            other: float or Vector2f representing what you want added
        """
        # Result, since __add__ should not change this directly
        result = Vector2f()

        # If it is a float then add it to both
        if type(other) is float or type(other) is int:
            result.x = (other+self.x)
            result.y += (other+self.y)
        elif isinstance(other, Vector2f):
            result.x = (other.x+self.x)
            result.y += (other.y+self.y)

        return result
    def __iadd__(self, other):
        """(+=) Adds a vector and vector, or vector and scalar.

        Will add components of vectors, or a scalar to both components of
        the vector. Then assigns this to the result and returns it.

        Args:
            other: float or Vector2f representing what you want added
        """
        self = self+other
        return self
    def __sub__(self, other):
        """(-) Subtracts a vector and vector, or vector and scalar.

        Will subtact components of vectors, or a scalar to both components of
        the vector.

        Args:
            other: float or Vector2f representing what you want subtracted
        """
        # Result, since __add__ should not change this directly
        result = Vector2f()

        # If it is a float then subtract it from both
        if type(other) is float or type(other) is int:
            result.x = (other-self.x)
            result.y += (other-self.y)
        elif isinstance(other, Vector2f):
            result.x = (other.x-self.x)
            result.y += (other.y-self.y)

        return result
    def __isub__(self, other):
        """(-=) Subtracts a vector and vector, or vector and scalar.

        Will subtract components of vectors, or a scalar to both components of
        the vector. Then assigns this to the result and returns it.

        Args:
            other: float or Vector2f representing what you want subtracted
        """
        self = self-other
        return self
    def __mul__(self, other):
        """(*) Multiplies a vector and vector, or vector and scalar.

        Will multiply components of vectors, or a scalar to both components of
        the vector.

        Args:
            other: float or Vector2f representing what you want multiplied
        """
        # Result, since __add__ should not change this directly
        result = Vector2f()

        # If it is a float then multiply it to both
        if type(other) is float or type(other) is int:
            result.x = (other*self.x)
            result.y += (other*self.y)
        elif isinstance(other, Vector2f):
            result.x = (other.x*self.x)
            result.y += (other.y*self.y)

        return result
    def __imul__(self, other):
        """(*=) Multipies a vector and vector, or vector and scalar.

        Will multiply components of vectors, or a scalar to both components of
        the vector. Then assigns this to the result and returns it.

        Args:
            other: float or Vector2f representing what you want multiplied
        """
        self = self*other
        return self
    def __div__(self, other):
        """(/) Divides a vector and vector, or vector and scalar.

        Will divide components of vectors, or a scalar to both components of
        the vector.

        Args:
            other: float or Vector2f representing what you want divided
        """
        # Result, since __add__ should not change this directly
        result = Vector2f()

        # If it is a float then divide both
        if type(other) is float or type(other) is int:
            result.x = (other/self.x)
            result.y += (other/self.y)
        elif isinstance(other, Vector2f):
            result.x = (other.x/self.x)
            result.y += (other.y/self.y)

        return result
    def __idiv__(self, other):
        """(/=) Divides a vector and vector, or vector and scalar.

        Will divide components of vectors, or a scalar to both components of
        the vector. Then assigns this to the result and returns it.

        Args:
            other: float or Vector2f representing what you want divided
        """
        self = self/other
        return self

    def __iter__(self):
        """Lets Vector2f be converted to a list or tuple."""
        # First element is x, second element is y
        yield self.x
        yield self.y
    def __len__(self):
        """Gets the length of the vector.

        Uses the pythagoream theorm `a^2+b^2=c^2`

        Returns:
            A float, representing the length of the Vector.
        """
        # Solve `a^2+b^2=c^2` to c = sqrt(a^2+b^2)
        return math.sqrt((self.x * self.x) + (self.y * self.y))

class Shapef(object):
    """Base class for all shapes.

    Members:
        position: (x,y) Vector2f representing the shapes position
    """
    @property
    def position(self):
        """The Vector2f position (x,y) of the shape."""
        return self._position
    @position.setter
    def position(self, value):
        """Sets the shape's position."""
        self._position = value

class Rectanglef(Shapef):
    """Used to represent a 2D rectangle."""

    def __init__(self, **kwargs):
        """Initalizes rectangle position and size.

        Args:
            position: a Vector2f, specifying the x and y of the rectangle,
                        cannot be specified with `x` or `y`
            size: a Vector2f, specifying the width and height of the rectangle,
                    cannot be specified with `width` or `height`
            x: the x position of the rectangle,
                cannot be specified with `position`
            y: the y position of the rectangle,
                cannot be specified with `position`
            width: the width of the rectangle,
                cannot be specified with `size`
            height: the height of the rectangle,
                cannot be specified with `size`
        """
        if ("x" in kwargs.keys() or "y" in kwargs.keys()) and \
            "position" in kwargs.keys():
            # If x/y was specified with position = error
            raise ValueError("Can't specify x/y and position to initalize \
                                Rectangle!")
        if ("width" in kwargs.keys() or "height" in kwargs.keys()) and \
            "size" in kwargs.keys():
            # If width/height was specified with size = error
            raise ValueError("Can't specify width/height and size to initalize \
                                Rectangle!")

        ########## POSITIONING ##########
        if "position" in kwargs.keys():
            self.position = kwargs["position"]
        else:
            if "x" in kwargs.keys():
                self.position.x = kwargs["x"]
            else:
                self.position.x = 0
            if "y" in kwargs.keys():
                self.position.y = kwargs["y"]
            else:
                self.position.y = 0
        ########## /POSITIONING/ ##########
        ########## SIZING ##########
        if "size" in kwargs.keys():
            self.size = kwargs["size"]
        else:
            if "width" in kwargs.keys():
                self.size.width = kwargs["width"]
            else:
                self.size.width = 0
            if "height" in kwargs.keys():
                self.size.height = kwargs["height"]
            else:
                self.size.height = 0
        ########## /SIZING/ ##########

    @property
    def size(self):
        """The size of the rectangle.

        To get the width do `Rectanglef.size.x`
        for height do `Rectanglef.size.y`
        """
        return self._size
    @size.setter
    def size(self, value):
        """The size of the rectangle.

        To get the width do `Rectanglef.size.x`
        for height do `Rectanglef.size.y`

        Args:
            value: a Vector2f representing the size (width/height) of the
                    rectangle.
        """
        self._size = value

class Circlef(Shapef):
    """Used to represent a 2D circle.

    Contains:
        radius: the radius of the circle
    """

    def __init__(self, radius=1.0):
        """Initalizes radius.

        Args:
            radius: positive float/int representing the radius of the circle
        """
        self.radius = radius

    @property
    def radius(self):
        """The radius (half the diameter) of the circle."""
        return self._radius
    @radius.setter
    def radius(self, value):
        """Sets the radius variable, max is 500.

        Args:
            value: positive float/int representing the radius of the circle
        """
        # If 'value' is negative, use its absolute value instead (abs)
        if value < 0:
            value = math.abs(value)
        # Max 'value' out at 500
        if value > 500:
            value = 500
        self._radius = float(value)
    @property
    def diameter(self):
        """The diameter (twice the radius) of the circle."""
        return (self.radius * 2)
    @diameter.setter
    def diameter(self, value):
        """Sets the diameter variable, max is 1000.

        Args:
            value: positive float/int representing the diameter of the circle
        """
        # If 'value' is negative, use its absolute value instead (abs)
        if value < 0:
            value = math.abs(value)
        # Max 'value' out at 500
        if value > 500:
            value = 1000
        self._radius = (float(value)/2.0)

    @property
    def area(self):
        """Returns area of the circle calculated with PI*r^2."""
        return float(math.pi * math.pow(self.radius))
    @property
    def circumference(self):
        """The circumference (area around/perimeter) of the circle.

        Calculated with 2*PI*r."""
        return float(2*math.pi*self.radius)

class RigidBody2D():
    """Better movement and collision."""

    @property
    def position(self):
        """Returns this rigidbody's collider's position."""
        return self._collider.position
    @property
    def size(self):
        """Returns this rigidbody's collider's size."""
        return self._collider.size

    @property
    def velocity(self):
        return self._velocity
    @velocity.setter
    def velocity(self, value):
        self._velocity = value

    # A set of all registered rigidbodies
    rigidbodies = set()

    def __init__(self, collide_shape):
        """Registers to rigidbodies set. And sets up colliders.

        Args:
            collide_shape: an instance of Shapef or derived. Represents the
                            collision area of the object.
        """

        self._velocity = Vector2f()
        self._collider = collide_shape

        # Adds self to set 'rigidbodies'
        RigidBody2D.rigidbodies.add(self)

    def Update(self, dt: float):
        # Multiplying the velocity by how long it takes to collide
        self.velocity *= collide_swept(self._collider, self.velocity, RigidBody2D.rigidbodies)
        self._collider.position += self.velocity

def collide_shapes(collider_shape, *shapes):
    """Checks if the first shape collides with any others.

    IMPORTANT: does not do collisions between shapes other
    than the first one specified.

    Args:
        collider_shape: a shape that will be tested against the list `shapes`
        *shapes: a list of shape with at least one elements representing the
            shape(s) that should be tested for collision with `collider_shape`
    Returns:
        `None` if no collisions occured or a set of shape(s) that collided
            with `collider_shape`
    """

    # Making sure that at least one shape was passed into `*shapes`
    assert (len(shapes) > 0), "You must pass in at least than one shape for \
                                `*shapes`"

    # Function checking collisions between circles
    def circle_to_circle(circle1, circle2):
        """Checks for collisions between two circles."""
        # Distance between the two circles on the x and y axes, squared
        x_distance = ((circle1.position.x-circle2.position.x)**2)
        y_distance = ((circle1.position.y-circle2.position.y)**2)
        # Sum of the radii of the two circles
        radii_distance = ((circle1.radius+circle2.radius)**2)
        # If the distance between the two centers is less than sum of radii
        # then COLLIDED!
        return (x_distance+y_distance) <= radii_distance
    # Function checking collisions between rectangles
    def rect_to_rect(rect1, rect2):
        """Checks for collisions between two rectangles."""
        # The x-coordinate of the left side of each rectangle
        left1 = (rect1.position.x + rect1.size.x) # Add x and width
        left2 = (rect2.position.x + rect2.size.x)
        # The y-coordinate of the top of each rectangle
        top1 = (rect1.position.y + rect1.size.y) # Add y and height
        top2 = (rect2.position.y + rect2.size.y)
        ########## COLLISIONS ##########
        if rect1.position.y > top2:
            return False # Rect1 above
        if top1 < rect2.position.y:
            return False # Rect1 below
        if rect1.position.x > left2:
            return False # Rect1 to the left of Rect2
        if left1 < rect2.position.x:
            return False # Rect1 to the right of Rect2
        ########## /COLLISIONS/ ##########
        # No collision!
        return True
    # Function checking collisions between rectangles and circles
    def rect_to_circle(rect, circle):
        """Check for collisions between a rectangle and a circle."""
        # Closest point within/outside of the rectangle to the
        # center of the circle.
        closestX = 0.0
        closestY = 0.0

        if circle.position.x < rect.position.x:
            # If the circle is to the left of the rectangle
            # then the closestX is the rectangle's left side
            closestX = rect.position.x
        elif circle.position.x > (rect.position.x + rect.size.x):
            # If the circle is to the right of the rectangle
            # then the closestX is the rectangle's right side
            closestX = (rect.position.x + rect.size.width)
        else:
            # The center of the circle is between the left and right sides
            # of the rectangle, so the closest x is it's own
            closestX = circle.position.x

        # Exact same logic with y values
        if circle.position.y < rect.position.y:
            closestY = rect.position.y
        elif circle.position.y > (rect.position.y + rect.size.y):
            closestY = (rect.position.y + rect.size.width)
        else:
            closestY = circle.position.y

        # Check how far the center of the circle is to the closest x and y
        closeX = math.abs(circle.position.x-closestX) # Don't want it negative
        closeY = math.abs(circle.position.y-closestY)
        # Length of the closest x/y vector is how far it is
        distance = len(Vector2f(closeX, closeY))
        # If the distance is less than the circles radius then it is collided
        return (distance < circle.radius)


    # Looping through `*shapes` and checking for collisions with `collide_shape`
    for shape in shapes:
        pass

def collide_swept(collider_shape, collider_velocity, shapes):
    """Calculates sweeping collisions for the given object(s) and velocity.

    Takes in the current velocity of the collide shape and checks if it will
    'go through' any of the shapes this current frame.

    Args:
        collider_shape: an instance of a class derived from `Shapef`\
                    representing the shape that you want collisions checked for.
        collider_velocity: a Vector2f representing the current velocity of\
                            `collider_shape`.
        *shapes: a list of shapes that you want to check for collisions with
                    `collider_shape`
    Returns:
        A floating point number between 0 and 1, representing the fraction of
        the current velocity that the `collider_shape` should move this frame
        so that it will not collide with any `*shapes`.
    """
    # TODO: Implement swept circle colliders, currently only have AABB

    def get_time(shape):
        """Gets the entry and exit time for `collider_shape` colliding with\
        shape.

        Returns:
            A tuple of length two, with the entry time as element one, and the
            exit time as element two.
        """
        # Getting the distance between `collider_shape` and shape
        entry_distance = Vector2f()
        exit_distance = Vector2f()
        ### X ###
        if collider_velocity.x > 0:
            # If `collider_shape` is traveling forward on the x-axis
            entry_distance.x = shape.position.x - (collider_shape.position.x + \
                                                    collider_shape.size.x)
            exit_distance.x = (shape.position.x + shape.size.x) - \
                                collider_shape.position.x
        else:
            # If `collider_shape` is traveling backwards on the x-axis,
            # do the opposite.
            entry_distance.x = (shape.position.x + shape.size.x) - \
                                collider_shape.position.x
            exit_distance.x = shape.position.x - (collider_shape.position.x + \
                                                    collider_shape.size.x)
        ### /X/ ###
        ### Y ###
        # Same as x
        if collider_velocity.y > 0:
            # If `collider_shape` is traveling forward on the y-ayis
            entry_distance.y = shape.position.y - (collider_shape.position.y + \
                                                    collider_shape.size.y)
            exit_distance.y = (shape.position.y + shape.size.y) - \
                                collider_shape.position.y
        else:
            # If `collider_shape` is traveling backwards on the y-ayis,
            # do the opposite.
            entry_distance.y = (shape.position.y + shape.size.y) - \
                                collider_shape.position.y
            exit_distance.y = shape.position.y - (collider_shape.position.y + \
                                                    collider_shape.size.y)
        ### /Y/ ###
        # The actual entry and exit times, the x and y a floating point number 0
        # to 1 relative to how much of the velocity can be traveled.

        # Initalize as negative and positive infinity
        entry = Vector2f(x=float("-inf"), y=float("-inf"))
        exit = Vector2f(x=float("inf"), y=float("inf"))

        # No dividing by zero!
        if collider_velocity.x != 0:
            # Divide distance by speed to get decimal representing how much
            # of velocity should be travled.
            entry.x = entry_distance.x / collider_velocity.x
            exit.x = exit_distance.x / collider_velocity.x
        if collider_velocity.y != 0:
            # Divide distance by speed to get decimal representing how much
            # of velocity should be travled.
            entry.y = entry_distance.y / collider_velocity.y
            exit.y = exit_distance.y / collider_velocity.y

        # Time (0 to 1) will always be greatest x or y value
        entryTime = max(entry.x, entry.y)
        exitTime = min(exit.x, exit.y)

        # No Collision!
        # Conditions for collision to happen:
        #   1. Entry must come before exit
        #   2. Entry-time and exit-time must be between 1 and 0
        if (entryTime > exitTime) or (entry.x < 0 and entry.y < 0) or \
            (entry.x > 1) or (entry.y > 1):
            # `return 1`: full velocity can be made without colliding into
            # anything.
            return 1
        else:
            print("Distance: "+str([tuple(entry_distance),tuple(exit_distance)]))
            print("Entries/Exits: "+str([tuple(entry),tuple(exit)]))
            print("Times: "+str([entryTime, exitTime]))
            print("Velocity: "+str(tuple(collider_velocity)))
            print("Shapes:\n\tCollider:\n\t\tPosition: "+str(tuple(collider_shape.position))+
                    "\n\t\tSize: "+str(tuple(collider_shape.size))+"\n\tBlock: "+
                    "\n\t\tPosition: "+str(tuple(shape.position))+"\n\t\tSize: "+
                    str(tuple(shape.size)))
            # `return entryTime`: number between one and 0 times velocity is how
            # far `shape` can travel this frame
            return entryTime

    # Want the earliest point that `collider_shape` collides with any one
    # of `*shapes`. One means that the shape `collider_shape` should travel
    # it's full velocity `collider_velocity`, and zero means that
    # `collider_shape` should not move at all.
    minimum_collision_time = float(1.0)

    # Loop through the list of shapes
    for shape in shapes:
        collideTime = get_time(shape)
        # Only set `minimum_collision_time` if this is the smallest time so far
        if collideTime == 0.0:
            print(collideTime)
            print(tuple(shape.position))
        if collideTime < minimum_collision_time:
            minimum_collision_time = collideTime

    return minimum_collision_time

# TODO: Make it so that this is more friendly with the kivy enviornment.
# TODO: Type checking with properties
