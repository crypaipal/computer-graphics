#!/usr/bin/env python3
import math
import random
import sys

from glfw.GLFW import *

from OpenGL.GL import *
from OpenGL.GLU import *

# Załadowano moduł, pozwalający wczytywać obrazy w języku Python
from PIL import Image
import numpy

viewer = [0.0, 0.0, 10.0]

theta = 0.0
pix2angle = 1.0

left_mouse_button_pressed = 0
mouse_x_pos_old = 0
delta_x = 0

mat_ambient = [1.0, 1.0, 1.0, 1.0]
mat_diffuse = [1.0, 1.0, 1.0, 1.0]
mat_specular = [1.0, 1.0, 1.0, 1.0]
mat_shininess = 20.0

light_ambient = [0.1, 0.1, 0.0, 1.0]
light_diffuse = [0.8, 0.8, 0.0, 1.0]
light_specular = [1.0, 1.0, 1.0, 1.0]
light_position = [0.0, 0.0, 10.0, 1.0]

att_constant = 1.0
att_linear = 0.05
att_quadratic = 0.001

showBoards = True
choice = False
# wczytanie obrazka z dysku i załadowanie go do pamięci
image = Image.open("meme.tga")
image2 = Image.open("chillGuy.tga") 
color = random.random()   

def startup():
    update_viewport(None, 400, 400)
    glClearColor(0.7, 0.0, 0.3, 1.0)
    glEnable(GL_DEPTH_TEST)

    glMaterialfv(GL_FRONT, GL_AMBIENT, mat_ambient)
    glMaterialfv(GL_FRONT, GL_DIFFUSE, mat_diffuse)
    glMaterialfv(GL_FRONT, GL_SPECULAR, mat_specular)
    glMaterialf(GL_FRONT, GL_SHININESS, mat_shininess)

    glLightfv(GL_LIGHT0, GL_AMBIENT, light_ambient)
    glLightfv(GL_LIGHT0, GL_DIFFUSE, light_diffuse)
    glLightfv(GL_LIGHT0, GL_SPECULAR, light_specular)
    glLightfv(GL_LIGHT0, GL_POSITION, light_position)

    glLightf(GL_LIGHT0, GL_CONSTANT_ATTENUATION, att_constant)
    glLightf(GL_LIGHT0, GL_LINEAR_ATTENUATION, att_linear)
    glLightf(GL_LIGHT0, GL_QUADRATIC_ATTENUATION, att_quadratic)

    glShadeModel(GL_SMOOTH)
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)

    # Dodano funkcje związane z uaktywnieniem teksturowania
    glEnable(GL_TEXTURE_2D)
    glEnable(GL_CULL_FACE)
    glTexEnvi(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_MODULATE)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR) # włączają mechanizm teksturowania i opisują jego ustawienia

    glTexImage2D(
        GL_TEXTURE_2D, 0, 3, image.size[0], image.size[1], 0,
        GL_RGB, GL_UNSIGNED_BYTE, image.tobytes("raw", "RGB", 0, -1)
    )
    # wczytanie obrazka z dysku i załadowanie go do pamięci

    glTexImage2D(
        GL_TEXTURE_2D, 0, 3, image2.size[0], image2.size[1], 0,
        GL_RGB, GL_UNSIGNED_BYTE, image2.tobytes("raw", "RGB", 0, -1)
    )


def shutdown():
    pass

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
        for j in range(0, N):
            u = tablica_u[j]
            v = tablica_v[i]
            tab[i][j][0] = (-90 * u ** 5 + 225 * u ** 4 - 270 * u ** 3 + 180 * u ** 2 - 45 * u) * math.cos(math.pi * v)
            tab[i][j][1] = 160 * u ** 4 - 320 * u ** 3 + 160 * u ** 2 - 5
            tab[i][j][2] = (-90 * u ** 5 + 225 * u **4 - 270 * u ** 3 + 180 * u ** 2 - 45 * u) * math.sin(math.pi * v)       
    
    # # rysowanie linii na ekranie
    # for i in range(0, N):
    #     for j in range(0, N):
    #         glColor3f(random.random(), random.random(), random.random())
    #         glBegin(GL_LINES)
    #         # połączamy koniec linii i z końcem i + 1 pionowo
    #         glVertex3f(tab[i][j][0], tab[i][j][1], tab[i][j][2])
    #         # sprawdzamy, czy nie jest to ostatni punkt
    #         if(i + 1 == N):
    #             i = -1
    #         glVertex3f(tab[i + 1][j][0], tab[i + 1][j][1], tab[i + 1][j][2])
    #         # jeśli indeks jest -1, to zmieniamy i, żeby pętla dalej działała
    #         if(i == -1):
    #             i = N - 1

    #         # połączamy koniec linii i z końcem i + 1 poziomo
    #         glVertex3f(tab[i][j][0], tab[i][j][1], tab[i][j][2])
    #         if(j + 1 == N):
    #             j = -1
    #         glVertex3f(tab[i][j + 1][0], tab[i][j + 1][1], tab[i][j + 1][2])
    #         if(j == -1):
    #             j = N - 1

    #         glEnd()

    # rysowanie grupy trójkątów na ekranie            
    for i in range(0, N):
        # glColor3ub(random.randint(0,255), random.randint(0,255), random.randint(0,255))
        glBegin(GL_TRIANGLE_STRIP)

        for j in range(0, math.floor(N / 2)):
            # współrzędna tekstury w osi v
            height = j * (1.0 / (math.floor(N / 2) - 1.0)) # dzielimy na rowne czesci

            # tekstura jest dzielona przez 2- mipmapping, przesunięta o 75%
            glTexCoord2f(tablica_v[i] / 2 + 0.75, height)
            glVertex3f(tab[N - 1 - i][j][0], tab[N - 1 - i][j][1], tab[N - 1 - i][j][2])
            
            if(i + 1 == N):
                i = -1
            
            glTexCoord2f(tablica_v[i + 1] / 2 + 0.75, height)
            glVertex3f(tab[N - 2 - i][j][0], tab[N - 2 - i][j][1], tab[N - 2 - i][j][2])
        
            if(i == -1):
                i = N - 1

        glEnd()

    for i in range(0, N):
        # glColor3ub(random.randint(0,255), random.randint(0,255), random.randint(0,255))
        glBegin(GL_TRIANGLE_STRIP)
        
        for j in range(0, math.floor(N / 2)):
            height = j * (1.0 / (math.floor(N / 2) - 1.0))
            
            # tekstura jest dzielona przez 2 - mipmapping, przesunięta o 25% 
            glTexCoord2f(tablica_v[i] / 2 + 0.25, height)
            # punkty w dolnej połowie siatki
            glVertex3f(tab[N - 1 - i][N - 1 - j][0], tab[N - 1 - i][N - 1 - j][1], tab[N - 1 - i][N - 1 - j][2])
            
            if(i + 1 == N):
                i = -1
            
            glTexCoord2f(tablica_v[i + 1] / 2 + 0.25, height)
            glVertex3f(tab[N - 2 - i][N - 1 - j][0], tab[N - 2 - i][N - 1 - j][1], tab[N - 2 - i][N - 1 - j][2])

            if(i == -1):
                i = N - 1

        glEnd()


def render(time):
    global theta, choice

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    gluLookAt(viewer[0], viewer[1], viewer[2],
              0.0, 0.0, 0.0, 0.0, 1.0, 0.0)

    if left_mouse_button_pressed:
        theta += delta_x * pix2angle

    glRotatef(theta, 0.0, 1.0, 0.0)
    
    if choice:
        glTexImage2D(
            GL_TEXTURE_2D, 0, 3, image.size[0], image.size[1], 0,
            GL_RGB, GL_UNSIGNED_BYTE, image.tobytes("raw", "RGB", 0, -1)
        )
        # wczytanie obrazka z dysku i załadowanie go do pamięci
    else:
        glTexImage2D(
            GL_TEXTURE_2D, 0, 3, image2.size[0], image2.size[1], 0,
            GL_RGB, GL_UNSIGNED_BYTE, image2.tobytes("raw", "RGB", 0, -1)
        )

    drawEgg(20)

    glFlush()


def update_viewport(window, width, height):
    global pix2angle
    pix2angle = 360.0 / width

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()

    gluPerspective(70, 1.0, 0.1, 300.0)

    if width <= height:
        glViewport(0, int((height - width) / 2), width, width)
    else:
        glViewport(int((width - height) / 2), 0, height, height)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()


def keyboard_key_callback(window, key, scancode, action, mods):
    global showBoards, choice
    if key == GLFW_KEY_ESCAPE and action == GLFW_PRESS:
        glfwSetWindowShouldClose(window, GLFW_TRUE)

    if key == GLFW_KEY_0 and action == GLFW_PRESS:
        showBoards = not showBoards
    
    if key == GLFW_KEY_SPACE and action == GLFW_PRESS:
        choice = not choice

def mouse_motion_callback(window, x_pos, y_pos):
    global delta_x
    global mouse_x_pos_old

    delta_x = x_pos - mouse_x_pos_old
    mouse_x_pos_old = x_pos


def mouse_button_callback(window, button, action, mods):
    global left_mouse_button_pressed

    if button == GLFW_MOUSE_BUTTON_LEFT and action == GLFW_PRESS:
        left_mouse_button_pressed = 1
    else:
        left_mouse_button_pressed = 0


def main():
    if not glfwInit():
        sys.exit(-1)

    window = glfwCreateWindow(400, 400, __file__, None, None)
    if not window:
        glfwTerminate()
        sys.exit(-1)

    glfwMakeContextCurrent(window)
    glfwSetFramebufferSizeCallback(window, update_viewport)
    glfwSetKeyCallback(window, keyboard_key_callback)
    glfwSetCursorPosCallback(window, mouse_motion_callback)
    glfwSetMouseButtonCallback(window, mouse_button_callback)
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