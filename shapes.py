# coding=utf-8
from math import *
import numpy as np
import matplotlib.pyplot as plt
from basic_shapes import Shape


def createColorCircle(radio, sides, r, g, b):
    steps = pi / sides
    t = np.arange(-np.pi, np.pi, steps)
    x = radio * np.sin(t)
    y = radio * np.cos(t)
    plt.plot(x, y)
    plt.axis('equal')
    plt.show()
    # Defining locations and colors for each vertex of the shape
    vertices = []

    for i in range(len(x)):
        # Positions
        vertices.append(x[i])
        vertices.append(y[i])
        vertices.append(0.0)
        # Colors
        vertices.append(r)
        vertices.append(g)
        vertices.append(b)

    # Defining connections among vertices
    indices = []
    for i in range(len(x)):
        indices.append(i)
    indices.append(0)

    return Shape(vertices, indices)
