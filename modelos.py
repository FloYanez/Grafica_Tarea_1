"""
Todos los modelos
1.- Cuerpo celeste
2.- Info???
"""

import transformations as tr
import basic_shapes as bs
import shapes as s
import scene_graph as sg
import easy_shaders as es

class Cuerpo(object):
    def __init__(self, color, radius, distance, velocity, satellites, padre=None):
        #Figuras básicas
        self.color = color
        self.radius = radius
        self.distance = distance
        self.velocity = velocity
        self.padre = padre
        self.satellites = satellites
        gpu_body_circle = es.toGPUShape(s.createColorCircle(color[0], color[1], color[2]))
        gpu_orbit_circle = es.toGPUShape(s.createColorCircle(color[0], color[1], color[2]))

        # Cuerpo
        body = sg.SceneGraphNode('body')
        body.transform = tr.uniformScale(radius)
        body.childs += [gpu_body_circle]

        # Orbita
        orbit = sg.SceneGraphNode('orbit')
        orbit.transform = tr.uniformScale(distance)
        orbit.childs += [gpu_orbit_circle]

        # Ensamble
        ensamble = sg.SceneGraphNode('ensamble')
        ensamble.childs += [body, orbit]

        transform_ensamble = sg.SceneGraphNode('ensambleTR')
        transform_ensamble.childs += [ensamble]

        self.model = transform_ensamble

    def draw(self, pipeline):
        sg.drawSceneGraphNode(self.model, pipeline, 'transform')


