# coding=utf-8
from math import *
import numpy as np
import matplotlib.pyplot as plt
from basic_shapes import Shape


# Sides must be an even number
# The number of triangles is sides/2 - 2
def createColorCircle(r, g, b, radius=1):
    sides = 32
    steps = pi / sides
    t = np.arange(-np.pi, np.pi, steps)
    x = radius * np.sin(t)
    y = radius * np.cos(t)
    # Defining locations and colors for each vertex of the shape
    vertices = []

    for i in range(len(x)):
        # Positions
        vertices.append(x[i])
        vertices.append(y[i])
        vertices.append(0.0)  # 2D
        # Colors
        vertices.append(r)
        vertices.append(g)
        vertices.append(b)

    # Defining connections among vertices
    indices = []
    nodos = len(x)
    for i in range(nodos):
        if (i != 0) and (i != (nodos - 1)):
            indices.append(0)
            indices.append(i)
            indices.append(i + 1)

    return Shape(vertices, indices)


# Sides must be an even number
# The number of triangles is sides/2 - 2
def createColorCircumference(r, g, b, radius=1):
    sides = 32
    steps = pi / sides
    t = np.arange(-np.pi, np.pi, 0.01)
    x = radius * np.sin(t)
    y = radius * np.cos(t)
    # Defining locations and colors for each vertex of the shape
    vertices = []

    for i in range(len(x)):
        # Positions
        vertices.append(x[i])
        vertices.append(y[i])
        vertices.append(0.0)  # 2D
        # Colors
        vertices.append(r)
        vertices.append(g)
        vertices.append(b)

    # Defining connections among vertices
    indices = []
    nodos = len(x)
    for i in range(nodos):
        indices.append(i)

    return Shape(vertices, indices)
