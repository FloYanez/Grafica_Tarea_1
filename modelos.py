"""
Todos los modelos
1.- Cuerpo celeste
2.- Info???
"""
import random

from OpenGL.GL import *  # importa las funciones de OpenGL
from math import *
import transformations as tr
import shapes as s
import scene_graph as sg
import easy_shaders as es


class Cuerpo(object):
    def __init__(self, color, radius, distance, velocity, satellites, parent=None):
        self.selected = False
        self.color = color
        self.radius = radius
        self.distance = distance
        self.velocity = velocity
        self.parent = parent
        if parent is None:
            self.parent_x = 0
            self.parent_y = 0
        else:
            self.parent_x = parent.get_x()
            self.parent_y = parent.get_y()
        self.satellites = satellites  # Lista de jsons
        self.satellites_objects = []
        self.satellites_nodes = []
        self.orbit_color = [x / 2 for x in color]
        self.x = 0 + self.parent_x
        self.x2 = self.x
        self.y = 1 * distance + self.parent_y
        self.y2 = self.y
        self.zoom = 1

        # Figuras básicas
        gpu_body_circle = es.toGPUShape(s.createColorCircle(*self.color))
        gpu_orbit_circumference = es.toGPUShape(s.createColorCircumference(*self.orbit_color))
        gpu_selection = es.toGPUShape(s.createColorCircle(1, 1, 1))

        # Create Satellites
        if satellites != "Null":
            for cuerpo in satellites:
                new_cuerpo = Cuerpo(cuerpo['Color'], cuerpo['Radius'], cuerpo['Distance'],
                                    cuerpo['Velocity'], cuerpo['Satellites'], self)
                self.satellites_objects.append(new_cuerpo)
                self.satellites_nodes.append(new_cuerpo.get_model())

        # Orbita
        # The circumference and it's scale
        orbit_circumference = sg.SceneGraphNode('orbit')
        orbit_circumference.transform = tr.uniformScale(distance)
        orbit_circumference.childs += [gpu_orbit_circumference]

        # Then the translation
        orbit = sg.SceneGraphNode('orbit')
        orbit.transform = tr.translate(self.parent_x, self.parent_y, 0)
        orbit.childs += [orbit_circumference]

        # Selection circle
        selection = sg.SceneGraphNode('selection_circle')
        selection.transform = tr.uniformScale(0)
        selection.childs += [gpu_selection]

        # Cuerpo
        # The circle and it's scale
        body_circle = sg.SceneGraphNode('body_circle')
        body_circle.transform = tr.uniformScale(self.radius)
        body_circle.childs += [gpu_body_circle]

        # Then the translation
        body = sg.SceneGraphNode('body')
        body.transform = tr.translate(self.x, self.y, 0)
        body.childs += [selection, body_circle]

        # Satellites
        satellites_node = sg.SceneGraphNode('satellites')
        satellites_node.transform = tr.translate(self.parent_x, self.parent_y, 0)
        satellites_node.childs += [*self.satellites_nodes]

        # Ensamble
        planeta = sg.SceneGraphNode('Planeta')
        planeta.childs += [orbit, body, satellites_node]

        transform_planeta = sg.SceneGraphNode('planetaTR')
        transform_planeta.childs += [planeta]

        self.model = transform_planeta

    def draw(self, pipeline):
        model = self.get_model()
        sg.drawSceneGraphNode(model, pipeline, 'transform')

    # Make the body move with mcu
    def update(self, t):
        self.update_parent_x()
        self.update_parent_y()
        parent_x = self.get_parent_x()
        parent_y = self.get_parent_y()
        d = self.get_distance()
        w = self.get_velocity()
        new_x = d * sin(w * t)
        new_y = d * cos(w * t)
        self.set_x(new_x + parent_x)
        self.set_y(new_y + parent_y)
        satellites = self.get_satellites_objects()

        model = self.get_model()
        body = sg.findNode(model, 'body')
        body.transform = tr.translate(self.get_x(), self.get_y(), 0)
        orbit = sg.findNode(model, 'orbit')
        orbit.transform = tr.matmul(
            [tr.uniformScale(self.get_zoom()), tr.translate(self.get_parent_x(), self.get_parent_y(), 0)])

        for planeta in satellites:
            planeta.update(t)

        selection = sg.findNode(model, 'selection_circle')
        if self.selected:
            selection.transform = tr.uniformScale(self.radius + 0.009)
        else:
            selection.transform = tr.uniformScale(0)


    def zoom_in(self):
        model = self.get_model()
        zoom = self.get_zoom()
        new_zoom = zoom + 0.1
        self.set_zoom(new_zoom)
        model.transform = tr.matmul([
            tr.uniformScale(new_zoom),
            tr.translate(self.x2, self.y2, 0)
        ])

    def zoom_out(self):
        model = self.get_model()
        zoom = self.get_zoom()
        new_zoom = zoom - 0.1
        self.set_zoom(new_zoom)
        model.transform = tr.matmul([
            tr.uniformScale(new_zoom),
            tr.translate(self.x2, self.y2, 0)
        ])

    def move_up(self):
        model = self.get_model()
        self.y2 = (self.y2 + 0.05)
        model.transform = tr.matmul([
            tr.uniformScale(self.get_zoom()),
            tr.translate(self.x2, self.y2, 0)
        ])

    def move_down(self):
        model = self.get_model()
        self.y2 = (self.y2 - 0.05)
        model.transform = tr.matmul([
            tr.uniformScale(self.get_zoom()),
            tr.translate(self.x2, self.y2, 0)
        ])

    def move_left(self):
        model = self.get_model()
        self.x2 = (self.x2 - 0.05)
        model.transform = tr.matmul([
            tr.uniformScale(self.get_zoom()),
            tr.translate(self.x2, self.y2, 0)
        ])

    def move_right(self):
        model = self.get_model()
        self.x2 = (self.x2 + 0.05)
        model.transform = tr.matmul([
            tr.uniformScale(self.get_zoom()),
            tr.translate(self.x2, self.y2, 0)
        ])

    def select(self):
        self.selected = not self.selected

    def get_zoom(self):
        return self.zoom

    def set_zoom(self, new_zoom):
        self.zoom = new_zoom

    def get_model(self):
        return self.model

    def get_parent(self):
        return self.parent

    def set_x(self, x):
        self.x = x

    def get_x(self):
        return self.x

    def set_y(self, y):
        self.y = y

    def get_y(self):
        return self.y

    def update_parent_x(self):
        if self.get_parent() is None:
            self.parent_x = 0
        else:
            self.parent_x = self.get_parent().get_x()

    def get_parent_x(self):
        return self.parent_x

    def update_parent_y(self):
        if self.get_parent() is None:
            self.parent_y = 0
        else:
            self.parent_y = self.get_parent().get_y()

    def get_parent_y(self):
        return self.parent_y

    def get_distance(self):
        return self.distance

    def get_velocity(self):
        return self.velocity

    def get_satellites_nodes(self):
        return self.satellites_nodes

    def get_satellites_objects(self):
        return self.satellites_objects
