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
    sides = 10
    steps = 0.01
    t = np.arange(-np.pi, np.pi, steps)
    x = radius * np.sin(t)
    y = radius * np.cos(t)
    radius2 = 0.99
    x2 = radius2 * np.sin(t)
    y2 = radius2 * np.cos(t)
    # Defining locations and colors for each vertex of the shape
    vertices = []

    for i in range(len(x)):
        # Outer circle
        # Positions
        vertices.append(x[i])
        vertices.append(y[i])
        vertices.append(0.0)  # 2D
        # Colors
        vertices.append(r)
        vertices.append(g)
        vertices.append(b)

    for i in range(len(x)):
        # Inner circle
        # Positions
        vertices.append(x2[i])
        vertices.append(y2[i])
        vertices.append(0.0)  # 2D
        # Colors
        vertices.append(r)
        vertices.append(g)
        vertices.append(b)

    # Defining connections among vertices
    indices = []
    nodos = len(x)
    for i in range(nodos):
        if i < nodos-1:
            indices.append(i)
            indices.append(i + 1)
            indices.append(i + 629)
            indices.append(i + 629)
            indices.append(i + 629 + 1)
            indices.append(i + 1)
    return Shape(vertices, indices)

def createGradientQuad(r1, g1, b1, r2, g2, b2):
    # Defining locations and colors for each vertex of the shape
    vertices = [
        #   positions        colors
        -0.5, -0.5, 0.0, r1, g1, b1,
        0.5, -0.5, 0.0, r1, g1, b1,
        0.5, 0.5, 0.0, r2, g2, b2,
        -0.5, 0.5, 0.0, r2, g2, b2]

    # Defining connections among vertices
    # We have a triangle every 3 indices specified
    indices = [
        0, 1, 2,
        2, 3, 0]

    return Shape(vertices, indices)
