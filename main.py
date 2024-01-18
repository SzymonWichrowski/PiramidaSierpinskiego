import math
import sys

from glfw.GLFW import *

from OpenGL.GL import *
from OpenGL.GLU import *

def startup():
    glClearColor(0.5, 0.5, 0.5, 1.0)
    glEnable(GL_DEPTH_TEST)


def shutdown():
    pass

def czworoscian_foremny():
    wierzcholki = [
        [0.0, 0.0, math.sqrt(2)],       # A
        [1.0, 0.0, 0.0],                # B
        [-0.5, math.sqrt(3)/2, 0.0],    # C
        [-0.5, -math.sqrt(3)/2, 0.0]    # D
    ]
    glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
    glBegin(GL_TRIANGLES)
    #ABC
    glVertex3f(wierzcholki[0][0], wierzcholki[0][1], wierzcholki[0][2])
    glVertex3f(wierzcholki[1][0], wierzcholki[1][1], wierzcholki[1][2])
    glVertex3f(wierzcholki[2][0], wierzcholki[2][1], wierzcholki[2][2])
    #ABD
    glVertex3f(wierzcholki[0][0], wierzcholki[0][1], wierzcholki[0][2])
    glVertex3f(wierzcholki[1][0], wierzcholki[1][1], wierzcholki[1][2])
    glVertex3f(wierzcholki[3][0], wierzcholki[3][1], wierzcholki[3][2])
    #ACD
    glVertex3f(wierzcholki[0][0], wierzcholki[0][1], wierzcholki[0][2])
    glVertex3f(wierzcholki[2][0], wierzcholki[2][1], wierzcholki[2][2])
    glVertex3f(wierzcholki[3][0], wierzcholki[3][1], wierzcholki[3][2])
    #BCD
    glVertex3f(wierzcholki[1][0], wierzcholki[1][1], wierzcholki[1][2])
    glVertex3f(wierzcholki[2][0], wierzcholki[2][1], wierzcholki[2][2])
    glVertex3f(wierzcholki[3][0], wierzcholki[3][1], wierzcholki[3][2])

    glEnd()
    glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)

def spin(angle):
    glRotatef(angle, 1.0, 0.0, 0.0)
    glRotatef(angle, 0.0, 1.0, 0.0)
    glRotatef(angle, 0.0, 0.0, 1.0)

def render(time):
    glClear(GL_COLOR_BUFFER_BIT)
    glClear(GL_DEPTH_BUFFER_BIT)

    spin(time * 90 / 3.1415)

    czworoscian_foremny()

    glFlush()

def main():
    if not glfwInit():
        sys.exit(-1)

    window = glfwCreateWindow(1000, 1000, __file__, None, None)
    if not window:
        glfwTerminate()
        sys.exit(-1)

    glfwMakeContextCurrent(window)
    glfwSwapInterval(1)

    startup()
    while not glfwWindowShouldClose(window):
        render(glfwGetTime())
        glfwSwapBuffers(window)
        glfwWaitEvents()
    shutdown()

    glfwTerminate()


if __name__ == '__main__':
    main()

