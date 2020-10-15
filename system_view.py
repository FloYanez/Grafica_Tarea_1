import glfw  # Usada para interactuar con un usuario (mouse, teclado, etc)
from OpenGL.GL import *  # importa las funciones de OpenGL
import OpenGL.GL.shaders  # importa el set de shaders de OpenGL.
import numpy as np
import sys  # para hacer handling de eventos, como entradas del sistema, o cerrar el programa.
from math import *

# A class to store the application control
class Controller:
    fillPolygon = True
    useShader2 = False
    show_info = False


# We will use the global controller as communication with the callback function
controller = Controller()  # Here we declare this as a global variable.


def on_key(window, key, scancode, action, mods):
    if action != glfw.PRESS:
        return
    # Declares that we are going to use the global object controller inside this function.
    global controller

    if key == glfw.KEY_ENTER:
        controller.show_info = not controller.show_info
        print("Show/hide info")

    elif key == glfw.KEY_W:
        print("Explore up")

    elif key == glfw.KEY_S:
        print("Explore down")

    elif key == glfw.KEY_A:
        print("Explore left")

    elif key == glfw.KEY_D:
        print("Explore right")

    elif key == glfw.KEY_Z:
        print("Zoom in")

    elif key == glfw.KEY_X:
        print("Zoom out")

    elif key == glfw.KEY_LEFT:
        print("Select left")

    elif key == glfw.KEY_RIGHT:
        print("Select right")

    elif key == glfw.KEY_ESCAPE:
        sys.exit()

    else:
        print('Unknown key')


# A simple class container to reference a shape on GPU memory
class GPUShape:
    def __init__(self):
        self.vao = 0
        self.vbo = 0
        self.ebo = 0
        self.texture = 0
        self.size = 0


def drawShape(shaderProgram, shape):
    # Binding the proper buffers
    glBindVertexArray(shape.vao)
    glBindBuffer(GL_ARRAY_BUFFER, shape.vbo)
    glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, shape.ebo)

    # Setting up the location of the attributes position and color from the VBO
    # A vertex attribute has 3 integers for the position (each is 4 bytes),
    # and 3 numbers to represent the color (each is 4 bytes),
    # Henceforth, we have 3*4 + 3*4 = 24 bytes
    position = glGetAttribLocation(shaderProgram, "position")
    glVertexAttribPointer(position, 3, GL_FLOAT, GL_FALSE, 24, ctypes.c_void_p(0))
    glEnableVertexAttribArray(position)

    color = glGetAttribLocation(shaderProgram, "color")
    glVertexAttribPointer(color, 3, GL_FLOAT, GL_FALSE, 24, ctypes.c_void_p(12))
    glEnableVertexAttribArray(color)

    # Render the active element buffer with the active shader program
    glDrawElements(GL_TRIANGLES, shape.size, GL_UNSIGNED_INT, None)


def createYellowTriangle():
    # Here the new shape will be stored
    gpuShape = GPUShape()

    # Defining locations and colors for each vertex of the shape
    vertexData = np.array([
        #   positions        colors
        -0.5, -0.5, 0.0, 1.0, 1.0, 0.0,  # v0 vertex with index 0
        0.5, -0.5, 0.0, 1.0, 1.0, 0.0,  # v1 vertex with index 1
        0.0, 0.5, 0.0, 1.0, 1.0, 0.0]  # v2 vertex with index 2
        # It is important to use 32 bits data
        , dtype=np.float32)

    # Defining connections among vertices
    # We have a triangle every 3 indices specified
    indices = np.array(
        [0, 1, 2], dtype=np.uint32)

    gpuShape.size = len(indices)

    # VAO, VBO and EBO and  for the shape
    gpuShape.vao = glGenVertexArrays(1)
    gpuShape.vbo = glGenBuffers(1)
    gpuShape.ebo = glGenBuffers(1)

    # Vertex data must be attached to a Vertex Buffer Object (VBO)
    glBindBuffer(GL_ARRAY_BUFFER, gpuShape.vbo)
    # En este caso len(vertexData) * 4 porque cada dato tiene 4 bytes de mem.
    # De hecho, se ve al revisar dtype=np.float32. Donde 32 = 4 * 8
    glBufferData(GL_ARRAY_BUFFER, len(vertexData) * 4, vertexData, GL_STATIC_DRAW)

    # Connections among vertices are stored in the Elements Buffer Object (EBO)
    glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, gpuShape.ebo)
    glBufferData(GL_ELEMENT_ARRAY_BUFFER, len(indices) * 4, indices, GL_STATIC_DRAW)

    return gpuShape


def createCircle(radius, sides, x0, y0):
    gpuShape = GPUShape()
    glBegin(GL_POLYGON)
    for i in range(100):
        top = radius * cos(i * 2 * pi / sides) + x0
        bottom = radius * sin(i * 2 * pi / sides) + y0
        glVertex2f(top, bottom)


def createBody(color, radius, position):
    gpuShape = GPUShape()


def main(*args):
    bodies = args[0]
    data = {}
    with open(bodies) as json_file:
        data = json.load(json_file)


if __name__ == "__main__":
    # Initialize glfw
    if not glfw.init():
        sys.exit()

    width = 800
    height = 600

    window = glfw.create_window(width, height, "Sistema Planetario", None, None)

    if not window:
        glfw.terminate()
        sys.exit()

    glfw.make_context_current(window)

    # Connecting the callback function 'on_key' to handle keyboard events
    glfw.set_key_callback(window, on_key)

    # Defining shaders for our pipeline
    vertex_shader = """
    #version 130
    in vec3 position;
    in vec3 color;

    out vec3 fragColor;

    void main()
    {
        fragColor = color;
        gl_Position = vec4(position, 1.0f);
    }
    """

    fragment_shader = """
    #version 130

    in vec3 fragColor;
    out vec4 outColor;

    void main()
    {
        outColor = vec4(fragColor, 1.0f);
    }
    """

    # Estamos entregando un segundo vertex shader
    # Notemos que multiplica la posición por dos :o
    vertex_shader2 = """
    #version 130
    in vec3 position;
    in vec3 color;

    out vec3 fragColor;

    void main()
    {
        fragColor = color;
        gl_Position = vec4(2 * position, 1.0f);
    }
    """

    # Estamos entregando un segundo fragment shader
    # Notemos que define como color el color promedio :o
    fragment_shader2 = """
    #version 130

    in vec3 fragColor;
    out vec4 outColor;

    void main()
    {
        float meanColor = (fragColor.r + fragColor.g + fragColor.b) / 3;
        outColor = vec4(meanColor, meanColor, meanColor,  1.0f);
    }
    """

    # Assembling the shader program (pipeline) with both shaders
    shaderProgram = OpenGL.GL.shaders.compileProgram(
        OpenGL.GL.shaders.compileShader(vertex_shader, GL_VERTEX_SHADER),
        OpenGL.GL.shaders.compileShader(fragment_shader, GL_FRAGMENT_SHADER))

    shaderProgram2 = OpenGL.GL.shaders.compileProgram(
        OpenGL.GL.shaders.compileShader(vertex_shader2, GL_VERTEX_SHADER),
        OpenGL.GL.shaders.compileShader(fragment_shader2, GL_FRAGMENT_SHADER))

    # Setting up the clear screen color
    glClearColor(0.15, 0.15, 0.15, 1.0)

    ### Create shapes
    gpuTriangle = createYellowTriangle()

    while not glfw.window_should_close(window):
        # Using GLFW to check for input events
        glfw.poll_events()

        # Filling or not the shapes depending on the controller state
        if controller.show_info:
            print("show")
            # glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
        else:
            glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)

        # Clearing the screen in both, color and depth
        glClear(GL_COLOR_BUFFER_BIT)

        # Drawing the shapes with a specific shader program depending on the controller state
        if controller.useShader2:
            # Telling OpenGL to use our shader program
            glUseProgram(shaderProgram2)
            # Telling OpenGL to draw our shapes using the previous shader program.
            drawShape(shaderProgram2, gpuTriangle)

        else:
            # Telling OpenGL to use our shader program
            glUseProgram(shaderProgram)
            # Telling OpenGL to draw our shapes using the previous shader program.
            drawShape(shaderProgram, gpuTriangle)

        # Once the render is done, buffers are swapped, showing only the complete scene.
        glfw.swap_buffers(window)

    glfw.terminate()
