#!/usr/bin/env python3
import math
import random
import sys

from glfw.GLFW import *

from OpenGL.GL import *
from OpenGL.GLU import *
import numpy

#tab = [[0] * 3 for i in range(N) for j in range(N)]  # tablica N x N x 3
color = random.random()


def startup():
    update_viewport(None, 400, 400)
    glClearColor(0.0, 0.0, 0.0, 1.0)
    glEnable(GL_DEPTH_TEST) # mechanizm bufora głębi


def shutdown():
    pass


def axes():
    glBegin(GL_LINES)

    glColor3f(1.0, 0.0, 0.0)
    glVertex3f(-5.0, 0.0, 0.0)
    glVertex3f(5.0, 0.0, 0.0)

    glColor3f(0.0, 1.0, 0.0)
    glVertex3f(0.0, -5.0, 0.0)
    glVertex3f(0.0, 5.0, 0.0)

    glColor3f(0.0, 0.0, 1.0)
    glVertex3f(0.0, 0.0, -5.0)
    glVertex3f(0.0, 0.0, 5.0)

    glEnd()

def drawEgg(N):
    random.seed(color)
    tab = numpy.zeros((N, N, 3)) # tworzenie tablicy trójwymiarowej
    tablica_u = [0 for i in range(N)] # tworzenie tabeli dla u
    tablica_v = [0 for i in range(N)] # tworzenie tabeli dla v

    # wypełneinie tablic u, v wartościami z zakresu [0;1]
    for i in range(0, N):
        tablica_u[i] = i * (1.0 / (N - 1.0))
        tablica_v[i] = i * (1.0 / (N - 1.0))

    # obliczamy koordynaty x, y, z dla każdego punktu 
    for i in range(0, N):
        for j in range(0,N):
            u = tablica_u[j]
            v = tablica_v[i]
            tab[i][j][0] = (-90 * u ** 5 + 225 * u ** 4 - 270 * u ** 3 + 180 * u ** 2 - 45 * u) * math.cos(math.pi * v)
            tab[i][j][1] = 160 * u ** 4 - 320 * u ** 3 + 160 * u ** 2 - 5
            tab[i][j][2] = (-90 * u ** 5 + 225 * u **4 - 270 * u ** 3 + 180 * u ** 2 - 45 * u) * math.sin(math.pi * v)       
    
    # rysowanie trójkątów na ekranie            
    for i in range(0, N):
        for j in range(0, N):
            
            glBegin(GL_TRIANGLES)

            glColor3f(random.random(), random.random(), random.random())
            # połączamy koniec linii i z końcem i + 1 pionowo
            glVertex3f(tab[i][j][0], tab[i][j][1], tab[i][j][2])
            # sprawdzamy, czy nie jest to ostatni punkt
            # zamykanie siatki pionowo
            if(i + 1 == N):
                i = -1

            glColor3f(random.random(), random.random(), random.random())
            glVertex3f(tab[i + 1][j][0], tab[i + 1][j][1], tab[i + 1][j][2])
            # zamykanie siatki poziomo
            if(i == -1):
                i = N - 1
            if(j + 1 == N):
                j = -1
                
            glColor3f(random.random(), random.random(), random.random())
            glVertex3f(tab[i][j + 1][0], tab[i][j + 1][1], tab[i][j + 1][2])
            if(j == -1):
                j = N - 1

            # rysowanie trójkąta dopełniającego  
            if(i + 1 == N):
                i = -1
            glVertex3f(tab[i + 1][j][0], tab[i + 1][j][1], tab[i + 1][j][2])
            if(i == -1):
                i = N - 1

            if(j+1 == N):
                j = -1  
            glVertex3f(tab[i][j + 1][0], tab[i][j + 1][1], tab[i][j + 1][2])
            if(j == -1):
                j = N - 1
            
            if(i + 1 == N):
                i = -1
            if(j + 1 == N):
                j = -1

            glVertex3f(tab[i + 1][j + 1][0], tab[i + 1][j + 1][1], tab[i + 1][j + 1][2])
            if(i == -1):
                i = N - 1
            if(j == -1):
                j = N - 1

            glEnd()

            

def spin(angle):
    glRotatef(angle, 1.0, 0.0, 0.0) # Następuje obrót o wartość kąta w stopniach (angle)
    glRotatef(angle, 0.0, 1.0, 0.0) # wokół osi obrotu opisanej przez wektor (trzy kolejne argumenty)
    glRotatef(angle, 0.0, 0.0, 1.0)


def render(time):
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    spin(time * 180 / 3.1415) 
    drawEgg(20)
    axes() # wywołanie fukcji rysującej układ współrzędnych
    glFlush()


# zakresy rysowania ustalono na [−7.5; 7.5]
def update_viewport(window, width, height):
    if width == 0:
        width = 1
    if height == 0:
        height = 1
    aspect_ratio = width / height

    glMatrixMode(GL_PROJECTION)
    glViewport(0, 0, width, height)
    glLoadIdentity()

    if width <= height:
        glOrtho(-7.5, 7.5, -7.5 / aspect_ratio, 7.5 / aspect_ratio, 7.5, -7.5)
    else:
        glOrtho(-7.5 * aspect_ratio, 7.5 * aspect_ratio, -7.5, 7.5, 7.5, -7.5)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()


def main():
    if not glfwInit():
        sys.exit(-1)

    window = glfwCreateWindow(400, 400, __file__, None, None)
    if not window:
        glfwTerminate()
        sys.exit(-1)

    glfwMakeContextCurrent(window)
    glfwSetFramebufferSizeCallback(window, update_viewport)
    glfwSwapInterval(1)

    startup()
    while not glfwWindowShouldClose(window):
        render(glfwGetTime())
        glfwSwapBuffers(window)
        glfwPollEvents()
    shutdown()

    glfwTerminate()


if __name__ == '__main__':
    main()