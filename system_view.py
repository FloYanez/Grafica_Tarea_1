"""
Dibuja --> main
"""


import json
import basic_shapes as bs
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

    width  = 800
    height = 800

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
    pipeline2 = es.SimpleTextureTransformShaderProgram()

    # Telling OpenGL to use ou shader program
    glUseProgram(pipeline.shaderProgram)

    # Setting up the clear screen color
    glClearColor(23 / 255, 9 / 255, 54 / 255, 1.0)

    # Our shapes here are always fully painted
    glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
    gpuShape = es.toGPUShape(bs.createTextureQuad("starry_sky.png", 1, 1), GL_REPEAT, GL_LINEAR)

    ### Create shapes
    # gpuStars = es.to_gpu_shape(basic_shapes.creature_texture_quad('/static/starry_sky copy.png'), GL_REPEAT, GL_LINEAL)

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
    controller.set_planet_list()

    # Acá se dibuja
    while not glfw.window_should_close(window):
        # Calculamos el tiempo
        ti = glfw.get_time()
        # Using GLFW to check for input events
        glfw.poll_events()

        # Clearing the screen in both, color and depth
        glClear(GL_COLOR_BUFFER_BIT)

        #Background
        glUseProgram(pipeline2.shaderProgram)
        glUniformMatrix4fv(glGetUniformLocation(pipeline.shaderProgram, "transform"), 1, GL_TRUE, tr.uniformScale(2))
        pipeline2.drawShape(gpuShape)

        # Dibujar modelos
        glUseProgram(pipeline.shaderProgram)
        for system in systems:
            system.draw(pipeline)
            system.update(ti)

        # Once the render is done, buffers are swapped, showing only the complete scene.
        glfw.swap_buffers(window)

    glfw.terminate()
