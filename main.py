import math
import sys

from glfw.GLFW import *

from OpenGL.GL import *
from OpenGL.GLU import *

def startup():
    glClearColor(0.0, 0.0, 0.0,  1.0)
    update_viewport(None, 1000, 1000)
    glEnable(GL_DEPTH_TEST)

def shutdown():
    pass

def update_viewport(window, width, height):
    if height == 0:
        height = 1
    if width == 0:
        width = 1
    aspectRatio = width / height

    glMatrixMode(GL_PROJECTION)
    glViewport(0,0,width, height)
    glLoadIdentity()

    zakres = 1.5

    if width <= height:
        glOrtho(-zakres, zakres, -zakres / aspectRatio, zakres / aspectRatio, zakres, -zakres)
    else:
        glOrtho(-zakres * aspectRatio, zakres * aspectRatio, -zakres, zakres, zakres, -zakres)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()


def axes():
    glBegin(GL_LINES)

    glColor3f(1.0, 0.0, 0.0)
    glVertex3f(-5.0, 0.0, 0.0)
    glVertex3f(5.0, 0.0, 0.0)

    glColor3f(0.0, 1.0, 0.0)
    glVertex3f(0.0, -5.0, 0.0)
    glVertex3f(0.0, 5.0, 0.0)

    glColor3f(0.0, 1.0, 1.0)
    glVertex3f(0.0, 0.0, -5.0)
    glVertex3f(0.0, 0.0, 5.0)

    glEnd()

def spin(kat_obrotu):
    glRotatef(kat_obrotu, 0.0, 0.0, 1.0)

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

def podzial(wierz1, wierz2, wierz3, wierz4, n):
    wierz12 = [0.0, 0.0, 0.0]
    wierz23 = [0.0, 0.0, 0.0]
    wierz13 = [0.0, 0.0, 0.0]
    wierz14 = [0.0, 0.0, 0.0]
    wierz24 = [0.0, 0.0, 0.0]
    wierz34 = [0.0, 0.0, 0.0]
    if (n > 0):
        #wierzcholek pomiedzy wierz1 i wierz2
        wierz12[0] = (wierz1[0] + wierz2[0]) / 2
        wierz12[1] = (wierz1[1] + wierz2[1]) / 2
        wierz12[2] = (wierz1[2] + wierz2[2]) / 2
        #wierzcholek pomiedzy wierz2 i wierz3
        wierz23[0] = (wierz3[0] + wierz2[0]) / 2
        wierz23[1] = (wierz3[1] + wierz2[1]) / 2
        wierz23[2] = (wierz3[2] + wierz2[2]) / 2
        # wierzcholek pomiedzy wierz1 i wierz3
        wierz13[0] = (wierz1[0] + wierz3[0]) / 2
        wierz13[1] = (wierz1[1] + wierz3[1]) / 2
        wierz13[2] = (wierz1[2] + wierz3[2]) / 2
        # wierzcholek pomiedzy wierz1 i wierz4
        wierz14[0] = (wierz1[0] + wierz4[0]) / 2
        wierz14[1] = (wierz1[1] + wierz4[1]) / 2
        wierz14[2] = (wierz1[2] + wierz4[2]) / 2
        # wierzcholek pomiedzy wierz2 i wierz4
        wierz24[0] = (wierz4[0] + wierz2[0]) / 2
        wierz24[1] = (wierz4[1] + wierz2[1]) / 2
        wierz24[2] = (wierz4[2] + wierz2[2]) / 2
        # wierzcholek pomiedzy wierz3 i wierz4
        wierz34[0] = (wierz4[0] + wierz3[0]) / 2
        wierz34[1] = (wierz4[1] + wierz3[1]) / 2
        wierz34[2] = (wierz4[2] + wierz3[2]) / 2

        podzial(wierz1, wierz12, wierz13, wierz14, n-1)
        podzial(wierz12, wierz2, wierz23, wierz24, n-1)
        podzial(wierz13, wierz23, wierz3, wierz34, n-1)
        podzial(wierz14, wierz24, wierz34, wierz4, n-1)

    else:
        czworoscian_foremny(wierz1, wierz2, wierz3, wierz4)


def render(time, N):

    wierzcholki = [
        [-math.sqrt(3) / 2, -0.5, 0.0],     # A
        [math.sqrt(3) / 2, -0.5, 0.0],      # B
        [0.0, 1.0, 0.0],                    # C
        [0.0, 0.0, -math.sqrt(2)]           # D
    ]
    glClear(GL_COLOR_BUFFER_BIT)
    glClear(GL_DEPTH_BUFFER_BIT)

    glLoadIdentity()
    axes()

    glLoadIdentity()
    spin(time * 180 / 3.1415)

    podzial(wierzcholki[0], wierzcholki[1], wierzcholki[2], wierzcholki[3], N)

    glFlush()

def main():
    ok = 0
    print("Algorytm konstrukcji Piramidy Sierpinskiego przyjmuje jako parametr liczbe podzialow czworoscianu foremnego na mniejsze czworosciany foremne")
    while(ok == 0):
        print("Podaj liczbe podzialow:")
        N = int(input())
        if(N < 0):
            print("Nieprawidlowa liczba podzialow. Prosze sprobowac ponownie!")
        else:
            ok = 1

    if not glfwInit():
        sys.exit(-1)

    window = glfwCreateWindow(1000, 1000, __file__, None, None)
    if not window:
        glfwTerminate()
        sys.exit(-1)

    glfwMakeContextCurrent(window)
    glfwSetFramebufferSizeCallback(window, update_viewport)
    glfwSwapInterval(1)

    startup()
    while not glfwWindowShouldClose(window):
        render(glfwGetTime(), N)
        glfwSwapBuffers(window)
        glfwWaitEvents()
    shutdown()

    glfwTerminate()


if __name__ == '__main__':
    main()

