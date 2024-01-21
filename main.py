import pygame
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

import math

vertices = [
    [-math.sqrt(3) / 2, -0.5, 0.0],  # A
    [math.sqrt(3) / 2, -0.5, 0.0],   # B
    [0.0, 1.0, 0.0],                 # C
    [0.0, 0.0, math.sqrt(2)]        # D
]

rotate_speed = 0.05
whichSpin = 0

light_position = [0.0, 0.0, 3.0, 1.0]

def shutdown():
    pygame.quit()
    sys.exit()

def eq_triangle(wierz1, wierz2, wierz3):
    glBegin(GL_TRIANGLES)
    glColor3f(0.0, 0.0, 1.0)
    glVertex3f(wierz1[0], wierz1[1], wierz1[2])
    glColor3f(1.0, 0.0, 1.0)
    glVertex3f(wierz2[0], wierz2[1], wierz2[2])
    glColor3f(1.0, 1.0, 0.0)
    glVertex3f(wierz3[0], wierz3[1], wierz3[2])
    glEnd()

def reg_tetrahedron(wierz1, wierz2, wierz3, wierz4):
    # glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
    # ABC
    eq_triangle(wierz1, wierz2, wierz3)
    # ACD
    eq_triangle(wierz1, wierz3, wierz4)
    # BCD
    eq_triangle(wierz2, wierz3, wierz4)
    # ABD
    eq_triangle(wierz1, wierz2, wierz4)
    # glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)

def division(v1, v2, v3, v4, n):
    v12 = [0.0, 0.0, 0.0]
    v23 = [0.0, 0.0, 0.0]
    v13 = [0.0, 0.0, 0.0]
    v14 = [0.0, 0.0, 0.0]
    v24 = [0.0, 0.0, 0.0]
    v34 = [0.0, 0.0, 0.0]
    if n > 0:
        # wierzcholek pomiedzy wierz1 i wierz2
        v12[0] = (v1[0] + v2[0]) / 2
        v12[1] = (v1[1] + v2[1]) / 2
        v12[2] = (v1[2] + v2[2]) / 2
        # wierzcholek pomiedzy wierz2 i wierz3
        v23[0] = (v3[0] + v2[0]) / 2
        v23[1] = (v3[1] + v2[1]) / 2
        v23[2] = (v3[2] + v2[2]) / 2
        # wierzcholek pomiedzy wierz1 i wierz3
        v13[0] = (v1[0] + v3[0]) / 2
        v13[1] = (v1[1] + v3[1]) / 2
        v13[2] = (v1[2] + v3[2]) / 2
        # wierzcholek pomiedzy wierz1 i wierz4
        v14[0] = (v1[0] + v4[0]) / 2
        v14[1] = (v1[1] + v4[1]) / 2
        v14[2] = (v1[2] + v4[2]) / 2
        # wierzcholek pomiedzy wierz2 i wierz4
        v24[0] = (v4[0] + v2[0]) / 2
        v24[1] = (v4[1] + v2[1]) / 2
        v24[2] = (v4[2] + v2[2]) / 2
        # wierzcholek pomiedzy wierz3 i wierz4
        v34[0] = (v4[0] + v3[0]) / 2
        v34[1] = (v4[1] + v3[1]) / 2
        v34[2] = (v4[2] + v3[2]) / 2

        division(v1, v12, v13, v14, n - 1)
        division(v12, v2, v23, v24, n - 1)
        division(v13, v23, v3, v34, n - 1)
        division(v14, v24, v34, v4, n - 1)

    else:
        reg_tetrahedron(v1, v2, v3, v4)

def spinZ(spin_angle):
    glRotatef(spin_angle, 0.0, 0.0, 1.0)

def spinX(spin_angle):
    glRotatef(spin_angle, 1.0, 0.0, 0.0)

def spinY(spin_angle):
    glRotatef(spin_angle, 0.0, 1.0, 0.0)

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

def render(N):
    global vertices
    global rotate_speed
    global whichSpin

    axes()
    time_passed = pygame.time.get_ticks()
    if whichSpin == 0:
        spinZ(time_passed * rotate_speed)
    elif whichSpin == 1:
        spinY(time_passed * rotate_speed)
    elif whichSpin == 2:
        spinX(time_passed * rotate_speed)

    division(vertices[0], vertices[1], vertices[2], vertices[3], N)

    glFlush()

def light():
    global light_position
    #zrodla swiatla
    glLightfv(GL_LIGHT0, GL_POSITION, (5.0, 0.0, 0.0, 0.0))
    glLightfv(GL_LIGHT1, GL_POSITION,  light_position)

    # Ustawienie koloru światła otoczenia
    glLightfv(GL_LIGHT0, GL_AMBIENT, (0.0, 0.0, 1.0, 1.0))
    glLightfv(GL_LIGHT1, GL_AMBIENT, (0.0, 1.0, 0.0, 1.0))

    # Ustawienie koloru światła rozproszonego
    glLightfv(GL_LIGHT0, GL_DIFFUSE, (1.0, 1.0, 1.0, 1.0))
    glLightfv(GL_LIGHT1, GL_DIFFUSE, (1.0, 1.0, 1.0, 1.0))

    # Ustawienie koloru światła wypukłego
    glLightfv(GL_LIGHT0, GL_SPECULAR, (1.0, 1.0, 1.0, 1.0))
    glLightfv(GL_LIGHT1, GL_SPECULAR, (1.0, 1.0, 1.0, 1.0))

    constant_attenuation = 1.0
    linear_attenuation = 0.5
    quadratic_attenuation = 0.0

    glLightf(GL_LIGHT1, GL_CONSTANT_ATTENUATION, constant_attenuation)
    glLightf(GL_LIGHT1, GL_LINEAR_ATTENUATION, linear_attenuation)
    glLightf(GL_LIGHT1, GL_QUADRATIC_ATTENUATION, quadratic_attenuation)

    glColorMaterial(GL_FRONT, GL_AMBIENT_AND_DIFFUSE)

def main():
    ok = 0
    print(
        "Algorytm konstrukcji Piramidy Sierpinskiego przyjmuje jako parametr liczbe podzialow czworoscianu foremnego na mniejsze czworosciany foremne")
    while ok == 0:
        print("Podaj liczbe podzialow:")
        N = int(input())
        if N < 0:
            print("Nieprawidlowa liczba podzialow. Prosze sprobowac ponownie!")
        else:
            ok = 1

    global whichSpin, vertices

    pygame.init()
    display = (800, 600)
    pygame.display.set_mode(display, pygame.OPENGL | pygame.DOUBLEBUF)

    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    glEnable(GL_LIGHT1)
    glEnable(GL_COLOR_MATERIAL)

    glEnable(GL_DEPTH_TEST)
    gluPerspective(45, (display[0] / display[1]), 0.1, 50.0)
    glMatrixMode(GL_MODELVIEW)
    gluLookAt(0, 0, 4,  #eye
              0, 0, 0,  #center
              0, 1, 0)  #up

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                shutdown()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    shutdown()
                if event.key == pygame.K_UP:
                    glTranslatef(0, 0.2, 0)
                if event.key == pygame.K_DOWN:
                    glTranslatef(0, -0.2, 0)
                if event.key == pygame.K_LEFT:
                    glTranslatef(-0.2, 0, 0)
                if event.key == pygame.K_RIGHT:
                    glTranslatef(0.2, 0, 0)
                if event.key == pygame.K_z:
                    whichSpin = 0
                if event.key == pygame.K_y:
                    whichSpin = 1
                if event.key == pygame.K_x:
                    whichSpin = 2

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glEnable(GL_DEPTH_TEST)
        glPushMatrix()
        render(N)
        light()
        glPopMatrix()

        pygame.display.flip()
        pygame.time.wait(10)


if __name__ == "__main__":
    main()