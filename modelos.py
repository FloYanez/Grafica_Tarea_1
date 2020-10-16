"""
Todos los modelos
1.- Cuerpo celeste
2.- Info???
"""
from math import *
import numpy as np
import transformations as tr
import basic_shapes as bs
import shapes as s
import scene_graph as sg
import easy_shaders as es


class Cuerpo(object):
    def __init__(self, color, radius, distance, velocity, satellites, padre=None):
        # Figuras básicas
        self.color = color
        self.radius = radius
        self.distance = distance
        self.velocity = velocity
        self.padre = padre
        self.satellites = satellites
        self.x = 0
        self.y = 0
        self.alpha = 0
        gpu_body_circle = es.toGPUShape(s.createColorCircle(*color))

        # Cuerpo
        body = sg.SceneGraphNode('body')
        body.transform = tr.uniformScale(radius)
        body.childs += [gpu_body_circle]

        # Ensamble
        ensamble = sg.SceneGraphNode('ensamble')
        ensamble.childs += [body]

        transform_ensamble = sg.SceneGraphNode('ensambleTR')
        transform_ensamble.childs += [ensamble]

        self.model = transform_ensamble

    def draw(self, pipeline):
        sg.drawSceneGraphNode(self.model, pipeline, 'transform')

    def get_alpha(self):
        return self.alpha

    def set_alpha(self, beta):
        self.alpha = beta

    def set_x(self, x):
        self.x = x

    def set_y(self, y):
        self.y = y

    def get_distance(self):
        return self.distance

    def update(self):
        current_alpha = self.get_alpha()
        if current_alpha == 2 * pi:
            new_alpha = 0
        else:
            new_alpha = current_alpha + 2 * pi / 32
        self.set_alpha(new_alpha)
        d = self.get_distance()
        self.set_x(d * sin(self.get_alpha()))
        self.set_y(d * cos(self.get_alpha()))


class Orbita():
    def __init__(self, x0, y0, distance, color=[1, 1, 1]):
        self.x0 = x0
        self.y0 = y0
        self.distance = distance
        self.color = [x / 2 for x in color]

        gpu_orbit_circumference = es.toGPUShape(s.createColorCircumference(*color))

        # Cuerpo
        body = sg.SceneGraphNode('body')
        body.transform = tr.uniformScale(distance)
        body.childs += [gpu_orbit_circumference]

        transform_ensamble = sg.SceneGraphNode('ensambleTR')
        transform_ensamble.childs += [body]

        self.model = transform_ensamble

    def draw(self, pipeline):
        sg.drawSceneGraphNode(self.model, pipeline, 'transform')
