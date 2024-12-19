#!/usr/bin/env python3
import math
import sys

from glfw.GLFW import *
from OpenGL.GL import *
from OpenGL.GLU import *

def startup():
    update_viewport(None, 400, 400)
    glClearColor(0.0, 0.0, 0.0, 1.0)
    glEnable(GL_DEPTH_TEST)  # mechanizm bufora głębi

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

# szuka punkt środkowy między dwoma wierzchołkami
def midpoint(v1, v2):
    return [(v1[i] + v2[i]) / 2.0 for i in range(3)]

# rusuje piramide z 4 trójkątów
def drawTriangles(v0, v1, v2, v3):

    glBegin(GL_TRIANGLES)
    
    # pierwszy trójkąt
    glColor3f(1.0, 0.65, 0.0)
    glVertex3fv(v0)
    glVertex3fv(v1)
    glVertex3fv(v2)
    
    # drugi trójkąt
    glColor3f(1.0, 1.0, 0.0)
    glVertex3fv(v0)
    glVertex3fv(v1)
    glVertex3fv(v3)
    
    # trzeci trójkąt
    glColor3f(1.0, 1.0, 0.0)
    glVertex3fv(v0)
    glVertex3fv(v2)
    glVertex3fv(v3)
    
    # czwarty trójkąt
    glColor3f(1.0, 0.65, 0.0)
    glVertex3fv(v1)
    glVertex3fv(v2)
    glVertex3fv(v3)
    
    glEnd()

# rekurencyjnie rysujemy piramide
def sierpinskiTriangle3d(v0, v1, v2, v3, depth):
    if depth == 0:
        drawTriangles(v0, v1, v2, v3)
    else:
        # poszukiwanie punktów środkowych każdej krawędzi
        v01 = midpoint(v0, v1)
        v02 = midpoint(v0, v2)
        v03 = midpoint(v0, v3)
        v12 = midpoint(v1, v2)
        v13 = midpoint(v1, v3)
        v23 = midpoint(v2, v3)
        
        # rekurencja dla każdego z 4 trójkątów
        sierpinskiTriangle3d(v0, v01, v02, v03, depth - 1)
        sierpinskiTriangle3d(v1, v01, v12, v13, depth - 1)
        sierpinskiTriangle3d(v2, v02, v12, v23, depth - 1)
        sierpinskiTriangle3d(v3, v03, v13, v23, depth - 1)

# dane do rysowania
def drawSierpinski(N):
    # wierzchołki początkowe
    v0 = [4.0, 4.0, 4.0]
    v1 = [-4.0, -4.0, 4.0]
    v2 = [-4.0, 4.0, -4.0]
    v3 = [4.0, -4.0, -4.0]
    sierpinskiTriangle3d(v0, v1, v2, v3, N)

def spin(angle):
    glRotatef(angle, 1.0, 0.0, 0.0)  # Następuje obrót o wartość kąta w stopniach (angle)
    glRotatef(angle, 0.0, 1.0, 0.0)  # wokół osi obrotu opisanej przez wektor (trzy kolejne argumenty)
    glRotatef(angle, 0.0, 0.0, 1.0)  

def render(time):
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    spin(0.1 * time * 180 / 3.1415) 
    drawSierpinski(0) 
    axes()  # wywołanie fukcji rysującej układ współrzędnych
    glFlush()

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
