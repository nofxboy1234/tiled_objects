from tiled_object import Tiled_Object

# Delegation example

class Door(object):
    colour = 'brown'

    def __init__(self, number, status):
        self.number = number
        self.status = status

    @classmethod
    def knock(cls):
        print "Knock!"

    def open(self):
        self.status = 'open'

    def close(self):
        self.status = 'closed'

""" Inheritance: An object IS another object. Implicit delegation. """
class SecurityDoor(Door):
    colour = 'gray'
    locked = True

    def open(self):
        if self.locked:
            return
        super(SecurityDoor, self).open()

""" Composition: An object KNOWS another object. Explicit delegation """
class SecurityDoor(object):
    locked = True

    def __init__(self, number, status):
        self.door = Door(number, status)

    def open(self):
        if self.locked:
            return
        self.door.open()

    def __getattr__(self, attr):
        """ Called whenever a requested attribute or method is not
            found in the object.
        """
        return getattr(self.door, attr)

# sdoor1 = SecurityDoor(1, 'closed')
# sdoor1.locked = False
# sdoor1.open()
# print(sdoor1.status)
# print(sdoor1.colour)

to = Tiled_Object('enemies', 01, 19, 19, 32, 32,
                    object_name="enemy01")
print("group_name: %s" % to.group_name)
print("sprite: %s" % to.sprite)
print("id: %s" % to.id)
print("x: %s" % to.x)
print("y: %s" % to.y)
print("width: %s" % to.width)
print("height: %s" % to.height)
print("object_name: %s" % to.object_name)
print("type: %s" % to.type)
