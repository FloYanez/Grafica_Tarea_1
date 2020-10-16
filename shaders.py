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