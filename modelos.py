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
        self.satellites = satellites  # Lista de jsons
        self.satelites = []
        if satellites != "Null":
            for cuerpo in satellites:
                self.satelites.append(Cuerpo(cuerpo['Color'], cuerpo['Radius'], cuerpo['Distance'], cuerpo['Velocity'], cuerpo['Satellites']))
        self.x = 0
        self.y = 1 * distance
        gpu_body_circle = es.toGPUShape(s.createColorCircle(*color))

        # Cuerpo
        body = sg.SceneGraphNode('body')
        body.transform = tr.uniformScale(radius)
        body.childs += [gpu_body_circle]

        # Ensamble
        ensamble = sg.SceneGraphNode('ensamble')
        ensamble.childs += [body]
        # Orbita
        if self.distance != 0:
            gpu_orbit_circumference = es.toGPUShape(s.createColorCircumference(*color))
            orbit = sg.SceneGraphNode('orbit')
            orbit.transform = tr.uniformScale(distance)
            orbit.childs += [gpu_orbit_circumference]
            ensamble.childs += [orbit]
        transform_ensamble = sg.SceneGraphNode('ensambleTR')
        transform_ensamble.childs += [ensamble]

        self.model = transform_ensamble

    def draw(self, pipeline):
        self.model.transform = tr.translate(self.get_x(), self.get_y(), 0)
        sg.drawSceneGraphNode(self.model, pipeline, 'transform')

    def set_x(self, x):
        self.x = x

    def get_x(self):
        return self.x

    def set_y(self, y):
        self.y = y

    def get_y(self):
        return self.y

    def get_distance(self):
        return self.distance

    def get_velocity(self):
        return self.velocity

    def update(self, t):
        print("t = " + str(t))
        d = self.get_distance()
        print("d = " + str(d))
        w = self.get_velocity()
        print("w = " + str(w))
        new_x = d * sin(w * t)
        new_y = d * cos(w * t)
        print("x = " + str(new_x))
        print("y = " + str(new_y))
        self.set_x(new_x)
        self.set_y(new_y)


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
