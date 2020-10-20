import glfw
import sys

from modelos import *

# A class to store the application control
class Controller():
    model: 'System'

    def __init__(self):
        self.model = None

    def set_model(self, new_model):
        self.model = new_model

    def get_model(self):
        return self.model

    def on_key(self, window, key, scancode, action, mods):
        if action != glfw.PRESS:
            return
        # Declares that we are going to use the global object controller inside this function.
        global controller

        if key == glfw.KEY_Z:
            self.get_model().zoom_in()
            print("Zoom in")

        elif key == glfw.KEY_X:
            self.get_model().zoom_out()
            print("Zoom out")

        elif key == glfw.KEY_W:
            self.get_model().move_up()
            print("Move up")

        elif key == glfw.KEY_S:
            self.get_model().move_down()
            print("Move down")

        elif key == glfw.KEY_A:
            self.get_model().move_left()
            print("Move left")

        elif key == glfw.KEY_D:
            self.get_model().move_right()
            print("Move right")

        elif key == glfw.KEY_ESCAPE:
            sys.exit()

        else:
            print('Unknown key')
