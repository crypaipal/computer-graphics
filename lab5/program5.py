#!/usr/bin/env python3
import math
import random
import sys

from glfw.GLFW import *

from OpenGL.GL import *
from OpenGL.GLU import *
import numpy


viewer = [0.0, 0.0, 10.0]

theta = 0.0
phi = 0.0
pix2angle = 1.0

left_mouse_button_pressed = 0
right_mouse_button_pressed = 0
mouse_x_pos_old = 0
mouse_y_pos_old = 0
delta_x = 0
delta_y = 0
R = 5

# szereg zmiennych pomocniczych
mat_ambient = [1.0, 1.0, 1.0, 1.0] # składowe koloru materiału ()
mat_diffuse = [1.0, 1.0, 1.0, 1.0] # składowe koloru materiału (rozproszony)
mat_specular = [1.0, 1.0, 1.0, 1.0] # składowe koloru materiału (odbity)
mat_shininess = 20.0 # stopień połyskliwości materiału

light_ambient = [0.1, 0.1, 0.0, 1.0] # mówią o kolorze źródła światła (25-27)
light_diffuse = [0.8, 0.8, 0.0, 1.0]
light_specular = [1.0, 1.0, 1.0, 1.0]
light_position = [0.0, 0.0, 10.0, 1.0] # zmienna, opisująca położenie źródła światła

light_ambient1 = [1.0, 0.0, 1.3, 1.0] # mówią o kolorze źródła światła (25-27)
light_diffuse1 = [0.0, 1.0, 0.0, 1.0]
light_specular1 = [1.0, 1.0, 0.0, 1.0]
light_position1 = [0.0, 10.0, 0.0, 1.0] # zmienna, opisująca położenie źródła światła

# te zmienne określają składowe funkcji strat natężenia
att_constant = 1.0 
att_linear = 0.05
att_quadratic = 0.001

tab = [light_ambient, light_diffuse, light_specular]
i = 0
j = 0 
color = random.random()
mode = "else"

# funkcja związana z uaktywnieniem modelu oświetlenia
def startup():
    update_viewport(None, 400, 400)
    glClearColor(0.0, 0.0, 0.0, 1.0)
    glEnable(GL_DEPTH_TEST)

    # face - Specifies which face or faces are being updated
    # pname - Specifies the single-valued material parameter of the face or faces that is being updated
    # param - Specifies a pointer to the value or values that pname will be set to
    glMaterialfv(GL_FRONT, GL_AMBIENT, mat_ambient)
    glMaterialfv(GL_FRONT, GL_DIFFUSE, mat_diffuse)
    glMaterialfv(GL_FRONT, GL_SPECULAR, mat_specular)
    glMaterialf(GL_FRONT, GL_SHININESS, mat_shininess)

    # Identyfikator GL_LIGHT0 wskazuje konkretne źródło światła
    glLightfv(GL_LIGHT0, GL_AMBIENT, light_ambient)
    glLightfv(GL_LIGHT0, GL_DIFFUSE, light_diffuse)
    glLightfv(GL_LIGHT0, GL_SPECULAR, light_specular)
    glLightfv(GL_LIGHT0, GL_POSITION, light_position)

    glLightf(GL_LIGHT0, GL_CONSTANT_ATTENUATION, att_constant)
    glLightf(GL_LIGHT0, GL_LINEAR_ATTENUATION, att_linear)
    glLightf(GL_LIGHT0, GL_QUADRATIC_ATTENUATION, att_quadratic)

    glLightfv(GL_LIGHT1, GL_AMBIENT, light_ambient1)
    glLightfv(GL_LIGHT1, GL_DIFFUSE, light_diffuse1)
    glLightfv(GL_LIGHT1, GL_SPECULAR, light_specular1)
    glLightfv(GL_LIGHT1, GL_POSITION, light_position1)

    glLightf(GL_LIGHT1, GL_CONSTANT_ATTENUATION, att_constant)
    glLightf(GL_LIGHT1, GL_LINEAR_ATTENUATION, att_linear)
    glLightf(GL_LIGHT1, GL_QUADRATIC_ATTENUATION, att_quadratic)

    glShadeModel(GL_SMOOTH)
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    glEnable(GL_LIGHT1)


def shutdown():
    pass


def drawEgg(N):
    random.seed(color)
    tab = numpy.zeros((N, N, 3)) # tworzenie tablicy trójwymiarowej
    tab_N = numpy.zeros((N, N, 3))
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

            # obliczenie pochodnych cząstkowych
            xu = ( -450 * u ** 4 + 900 * u ** 3 - 810 * u ** 2 + 360 * u - 45) * math.cos(math.pi * v)
            xv = math.pi * (90 * u ** 5 - 225 * u ** 4 + 270 * u ** 3 - 180 * u ** 2 + 45 * u) * math.sin(math.pi * v)
            yu = (640 * u ** 3 - 960 * u ** 2 + 320 * u)
            yv = 0
            zu = ( -450 * u ** 4 + 900 * u ** 3 - 810 * u ** 2 + 360 * u - 45) * math.sin(math.pi * v)
            zv = -math.pi * (90 * u ** 5 - 225 * u ** 4 + 270 * u ** 3 - 180 * u ** 2 + 45 * u) * math.cos(math.pi * v)

            tab_N[i][j][0] = yu * zv - zu * yv 
            tab_N[i][j][1] = zu * xv - xu * zv 
            tab_N[i][j][2] = xu * yv - yu * xv

            # odwrócenie wektoru normalnego
            if(j >= 0.5 * N):
                tab_N[i][j][1]= tab_N[i][j][1] * (-1)
                tab_N[i][j][0]= tab_N[i][j][0] * (-1)
                tab_N[i][j][2]= tab_N[i][j][2] * (-1)

            # normalizacja wektorów: wektor = wektor/l_wektora
            # l_wektora = sqrt(suma kwadratow dla kazdej wartosi)
            length = math.sqrt(tab_N[i][j][0] ** 2 + tab_N[i][j][1] ** 2 + tab_N[i][j][2] ** 2)

            tab_N[i][j][0] = tab_N[i][j][0] / length
            tab_N[i][j][1] = tab_N[i][j][1] / length
            tab_N[i][j][2] = tab_N[i][j][2] / length


    # rysowanie trójkątów na ekranie            
    for i in range(0, N):
        for j in range(0, N):
            
            glBegin(GL_TRIANGLES)

            glColor3f(random.random(), random.random(), random.random())
            glNormal(tab_N[i][j][0], tab_N[i][j][1], tab_N[i][j][2])
            # połączamy koniec linii i z końcem i + 1 pionowo
            glVertex3f(tab[i][j][0], tab[i][j][1], tab[i][j][2])
            # sprawdzamy, czy nie jest to ostatni punkt
            # zamykanie siatki pionowo
            if(i + 1 == N):
                i = -1

            glColor3f(random.random(), random.random(), random.random())
            glNormal(tab_N[i + 1][j][0], tab_N[i + 1][j][1], tab_N[i + 1][j][2])
            glVertex3f(tab[i + 1][j][0], tab[i + 1][j][1], tab[i + 1][j][2])
            # zamykanie siatki poziomo
            if(i == -1):
                i = N - 1
            if(j + 1 == N):
                j = -1
                
            glColor3f(random.random(), random.random(), random.random())
            glNormal(tab_N[i][j + 1][0], tab_N[i][j + 1][1], tab_N[i][j + 1][2])
            glVertex3f(tab[i][j + 1][0], tab[i][j + 1][1], tab[i][j + 1][2])
            if(j == -1):
                j = N - 1

            # rysowanie trójkąta dopełniającego  
            if(i + 1 == N):
                i = -1
            glNormal(tab_N[i + 1][j][0], tab_N[i + 1][j][1], tab_N[i + 1][j][2])
            glVertex3f(tab[i + 1][j][0], tab[i + 1][j][1], tab[i + 1][j][2])
            if(i == -1):
                i = N - 1

            if(j + 1 == N):
                j = -1
            glNormal(tab_N[i][j + 1][0], tab_N[i][j + 1][1], tab_N[i][j + 1][2])
            glVertex3f(tab[i][j + 1][0], tab[i][j + 1][1], tab[i][j + 1][2])
            if(j == -1):
                j = N - 1
            
            if(i + 1 == N):
                i = -1
            if(j + 1 == N):
                j = -1

            glNormal(tab_N[i + 1][j + 1][0], tab_N[i + 1][j + 1][1], tab_N[i + 1][j + 1][2])
            glVertex3f(tab[i + 1][j + 1][0], tab[i + 1][j + 1][1], tab[i + 1][j + 1][2])
            if(i == -1):
                i = N - 1
            if(j == -1):
                j = N - 1

            glEnd()
            
            if mode == "show":
                glBegin(GL_LINES)
                glColor3f(0.5, 0.5, 0.5)
                glNormal(tab_N[i][j][0], tab_N[i][j][1], tab_N[i][j][2])
                glVertex3f(tab[i][j][0], tab[i][j][1], tab[i][j][2])

                glColor3f(0.5, 0.5, 0.5)
                glNormal(tab_N[i][j][0], tab_N[i][j][1], tab_N[i][j][2])
                glVertex3f(tab[i][j][0] + tab_N[i][j][0], tab[i][j][1] + tab_N[i][j][1], tab[i][j][2] + tab_N[i][j][2])
                glEnd()
            

def spin(angle):
    glRotatef(angle, 1.0, 0.0, 0.0) # Następuje obrót o wartość kąta w stopniach (angle)
    glRotatef(angle, 0.0, 1.0, 0.0) # wokół osi obrotu opisanej przez wektor (trzy kolejne argumenty)
    glRotatef(angle, 0.0, 0.0, 1.0)

def render(time):
    global theta
    global phi

    angle = math.pi / 180

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    gluLookAt(viewer[0], viewer[1], viewer[2],
            0.0, 0.0, 0.0, 0.0, 1.0, 0.0)
    
    if left_mouse_button_pressed:
        theta += delta_x * pix2angle
        theta = theta % 360
        phi += delta_y * pix2angle
        phi = phi % 360
    glRotatef(theta, 0.0, 1.0, 0.0)
    glRotatef(phi, 1.0, 0.0, 0.0)

    drawEgg(20)

    quadric = gluNewQuadric()
    gluQuadricDrawStyle(quadric, GLU_FILL)
    gluSphere(quadric, 3.0, 10, 10)
    gluDeleteQuadric(quadric)

    xs = R * math.cos(theta * angle) * math.cos(phi * angle)
    ys = R * math.sin(phi * angle)
    zs = R * math.sin(theta * angle) * math.cos(phi * angle)

    glTranslate(xs, ys, zs)

    # wizualizacja (sfera zbudowana z linii)
    quadric1 = gluNewQuadric()
    gluQuadricDrawStyle(quadric1, GLU_LINE)
    gluSphere(quadric1, 0.5, 6, 10)
    gluDeleteQuadric(quadric1)

    # wspólrzędne pozycji światła
    light_position[0] = xs
    light_position[1] = ys
    light_position[2] = zs

    glLightfv(GL_LIGHT1, GL_AMBIENT, light_ambient)
    glLightfv(GL_LIGHT1, GL_DIFFUSE, light_diffuse)
    glLightfv(GL_LIGHT1, GL_SPECULAR, light_specular)

    glLightfv(GL_LIGHT1, GL_POSITION, light_position)

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
    global i
    global j
    global mode
    if key == GLFW_KEY_ESCAPE and action == GLFW_PRESS:
        glfwSetWindowShouldClose(window, GLFW_TRUE)

    if key == GLFW_KEY_SPACE and action == GLFW_PRESS:
        i += 1 
        if(i == 4):
            i = 0
            j += 1
            if(j == 3):
                j = 0
        print("Now you can change ", j, " parametr ",  i, " value!")

    if key == GLFW_KEY_UP and action == GLFW_PRESS:
        tab[j][i] = tab[j][i] + 0.1
        if(tab[j][i] >= 1):
            tab[j][i] = 1.0
        print("Value of ", j, " parametr and ", i, " value sets to:", tab[j][i])

    if key == GLFW_KEY_DOWN and action == GLFW_PRESS:
        tab[j][i] = tab[j][i] - 0.1
        if(tab[j][i] <= 0):
            tab[j][i] = 0.0
        print("Value of ", j, " parametr and ", i, " value sets to:", tab[j][i])

    if key == GLFW_KEY_1 and action == GLFW_PRESS:
        mode = "show"

    if key == GLFW_KEY_0 and action == GLFW_PRESS:
        mode = "else"


def mouse_motion_callback(window, x_pos, y_pos):
    global delta_x
    global delta_y
    global mouse_x_pos_old 
    global mouse_y_pos_old

    delta_x = x_pos - mouse_x_pos_old
    mouse_x_pos_old = x_pos

    delta_y = y_pos - mouse_y_pos_old
    mouse_y_pos_old = y_pos


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