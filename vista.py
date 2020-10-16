"""
Dibuja --> main
"""

import glfw  # Usada para interactuar con un usuario (mouse, teclado, etc)
from OpenGL.GL import *  # importa las funciones de OpenGL
import OpenGL.GL.shaders  # importa el set de shaders de OpenGL.
import easy_shaders as es
import numpy as np
import sys  # para hacer handling de eventos, como entradas del sistema, o cerrar el programa.
from math import *
import json
from modelos import *
from shaders import *

def main(*args):
    bodies = args[0]
    data = {}
    with open(bodies) as json_file:
        data = json.load(json_file)
    return data


if __name__ == "__main__":
    data = main(*sys.argv[1:])  # argv[0] es el nombre de este archivo
    print(data)
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

    glfw.make_context_current(window)

    # Assembling the shader program (pipeline) with both shaders
    pipeline = es.SimpleTransformShaderProgram()

    # Telling OpenGL to use ou shader program
    glUseProgram(pipeline.shaderProgram)

    # Setting up the clear screen color
    glClearColor(23 / 255, 9 / 255, 54 / 255, 1.0)

    ### Create shapes
    planeta = Cuerpo([1, 1, 0], 0.1, 0.5, 0.0, None)
    orbita = Orbita(0, 0, 0.5)

    # Acá se dibuja
    while not glfw.window_should_close(window):
        # Using GLFW to check for input events
        glfw.poll_events()

        # Clearing the screen in both, color and depth
        glClear(GL_COLOR_BUFFER_BIT)
        planeta.update()
        # Dibujar modelos
        glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)  # linea
        orbita.draw(pipeline)
        glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)  # fill
        planeta.draw(pipeline)

        # Once the render is done, buffers are swapped, showing only the complete scene.
        glfw.swap_buffers(window)

    glfw.terminate()
