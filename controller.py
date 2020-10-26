import glfw
import sys

from modelos import *

# A class to store the application control
class Controller():
    model: 'System'

    def __init__(self):
        self.model = None
        self.planet_list = []
        self.selected = None
        self.planet_id = 0
        self.n = 0

    def set_model(self, new_model):
        self.model = new_model
        self.selected = self.model
        self.model.select()

    def get_model(self):
        return self.model

    def get_planet_id(self):
        return self.planet_id

    def set_planet_id(self, i):
        self.planet_id = i

    def select_planet(self, direction):
        id = self.get_planet_id()
        new_id = (self.get_planet_id() + direction) % self.n
        self.set_planet_id(new_id)
        planet = self.get_planet_list()[new_id]


        self.selected.select() #deselect previous
        self.selected = planet
        self.selected.select() #select

    def get_planet_list(self):
        return self.planet_list

    # Should be recursive
    def set_planet_list(self):
        planets = self.get_planet_list()
        model = self.get_model()
        planets.append(self.get_model())
        for planeta in model.get_satellites_objects():
            planets.append(planeta)
            for satellite in planeta.get_satellites_objects():
                planets.append(satellite)
        self.n = len(planets)

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

        elif key == glfw.KEY_LEFT:
            self.select_planet(-1)
            print("Select left")

        elif key == glfw.KEY_RIGHT:
            self.select_planet(1)
            print("Select right")

        elif key == glfw.KEY_ESCAPE:
            sys.exit()

        else:
            print('Unknown key')
