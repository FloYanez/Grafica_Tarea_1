"""
Todos los modelos
1.- Cuerpo celeste
2.- Info???
"""
from OpenGL.GL import *  # importa las funciones de OpenGL
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
        self.orbit_color = [x / 2 for x in color]

        if satellites != "Null":
            for cuerpo in satellites:
                self.satelites.append(Cuerpo(cuerpo['Color'], cuerpo['Radius'], cuerpo['Distance'], cuerpo['Velocity'], cuerpo['Satellites']))
        self.x = 0
        self.y = 1 * distance
        gpu_body_circle = es.toGPUShape(s.createColorCircle(*color))
        gpu_orbit_circumference = es.toGPUShape(s.createColorCircumference(*self.orbit_color))

        # Cuerpo
        # The circle and it's scale
        body_circle = sg.SceneGraphNode('body_circle')
        body_circle.transform = tr.uniformScale(radius)
        body_circle.childs += [gpu_body_circle]

        # Then the translation
        body = sg.SceneGraphNode('body')
        body.transform = tr.translate(self.get_x(), self.get_y(), 0)
        body.childs += [body_circle]

        # Orbita
        orbit = sg.SceneGraphNode('orbit')
        orbit.transform = tr.uniformScale(distance)
        orbit.childs += [gpu_orbit_circumference]

        # Ensamble
        planeta = sg.SceneGraphNode('Planeta')
        planeta.childs += [body, orbit]

        transform_planeta = sg.SceneGraphNode('planetaTR')
        transform_planeta.childs += [planeta]

        self.model = transform_planeta

    def draw(self, pipeline):
        model = self.get_model()
        # Draw orbit in line mode
        orbit = sg.findNode(model, 'orbit')
        glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)  # linea
        sg.drawSceneGraphNode(orbit, pipeline, 'transform')
        # Draw body in fill mode
        body = sg.findNode(model, 'body')
        body.transform = tr.translate(self.get_x(), self.get_y(), 0)
        glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)  # fill
        sg.drawSceneGraphNode(body, pipeline, 'transform')

    def get_model(self):
        return self.model

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

    # Make the body move with mcu
    def update(self, t):
        d = self.get_distance()
        w = self.get_velocity()
        new_x = d * sin(w * t)
        new_y = d * cos(w * t)
        self.set_x(new_x)
        self.set_y(new_y)
