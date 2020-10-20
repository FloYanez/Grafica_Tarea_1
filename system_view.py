"""
Dibuja --> main
"""

import glfw  # Usada para interactuar con un usuario (mouse, teclado, etc)
from OpenGL.GL import *  # importa las funciones de OpenGL
import OpenGL.GL.shaders  # importa el set de shaders de OpenGL.

import basic_shapes
import easy_shaders as es
import numpy as np
import sys  # para hacer handling de eventos, como entradas del sistema, o cerrar el programa.
from math import *
import json

import shapes
from modelos import *
from controller import *


def main(*args):
    bodies = args[0]
    data = {}
    with open(bodies) as json_file:
        data = json.load(json_file)
    return data


if __name__ == "__main__":
    # Initialize glfw
    if not glfw.init():
        sys.exit()

    width = 600
    height = 600


    window = glfw.create_window(width, height, "Sistema Planetario", None, None)

    if not window:
        glfw.terminate()
        sys.exit()

    glfw.make_context_current(window)

    controller = Controller()

    # Connecting the callback function 'on_key' to handle keyboard events
    glfw.set_key_callback(window, controller.on_key)

    # Assembling the shader program (pipeline) with both shaders
    pipeline = es.SimpleTransformShaderProgram()
    textureShaderProgram = es.SimpleTextureModelViewProjectionShaderProgram()
    colorShaderProgram = es.SimpleModelViewProjectionShaderProgram()

    # Telling OpenGL to use ou shader program
    glUseProgram(pipeline.shaderProgram)

    # Setting up the clear screen color
    glClearColor(23 / 255, 9 / 255, 54 / 255, 1.0)

    ### Create shapes
    #gpuStars = es.to_gpu_shape(basic_shapes.creature_texture_quad('/static/starry_sky copy.png'), GL_REPEAT, GL_LINEAL)

    data = main(*sys.argv[1:])  # argv[0] es el nombre de este archivo
    systems = []
    for system in data:
        color = system['Color']
        radius = system['Radius']
        distance = system['Distance']
        velocity = system['Velocity']
        satellites = system['Satellites']
        sun = Cuerpo(color, radius, distance, velocity, satellites)
        systems.append(sun)
        controller.set_model(sun)

    # Acá se dibuja
    while not glfw.window_should_close(window):
        # Calculamos el tiempo
        ti = glfw.get_time()
        # Using GLFW to check for input events
        glfw.poll_events()

        # Clearing the screen in both, color and depth
        glClear(GL_COLOR_BUFFER_BIT)

        # Dibujar modelos
        for system in systems:
            system.draw(pipeline)
            system.update(ti)

        # Once the render is done, buffers are swapped, showing only the complete scene.
        glfw.swap_buffers(window)

    glfw.terminate()
