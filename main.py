import math
import sys

from glfw.GLFW import *

from OpenGL.GL import *
from OpenGL.GLU import *

def startup():
    glClearColor(0.0, 0.0, 0.0,  1.0)
    glEnable(GL_DEPTH_TEST)

def shutdown():
    pass

def trojkat_rownoboczny(wierz1, wierz2, wierz3):
    glBegin(GL_TRIANGLES)
    glColor(0.0, 0.0, 1.0)
    glVertex3f(wierz1[0], wierz1[1], wierz1[2])
    glColor(1.0, 0.0, 1.0)
    glVertex3f(wierz2[0], wierz2[1], wierz2[2])
    glColor(1.0, 1.0, 0.0)
    glVertex3f(wierz3[0], wierz3[1], wierz3[2])
    glEnd()

def czworoscian_foremny(wierz1, wierz2, wierz3, wierz4):
    #glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
    #ABC
    trojkat_rownoboczny(wierz1, wierz2, wierz3)
    #ACD
    trojkat_rownoboczny(wierz1, wierz3, wierz4)
    #BCD
    trojkat_rownoboczny(wierz2, wierz3, wierz4)
    #ABD
    trojkat_rownoboczny(wierz1, wierz2, wierz4)
    #glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)

def render(time):
    wierzcholki = [
        [-math.sqrt(3) / 2, -0.5, 0.0],     # A
        [math.sqrt(3) / 2, -0.5, 0.0],      # B
        [0.0, 1.0, 0.0],                    # C
        [0.0, 0.0, -1.0]                    # D
    ]
    glClear(GL_COLOR_BUFFER_BIT)
    glClear(GL_DEPTH_BUFFER_BIT)

    czworoscian_foremny(wierzcholki[0], wierzcholki[1], wierzcholki[2], wierzcholki[3])

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

