#!/usr/bin/env python3
import math
import sys

from glfw.GLFW import *

from OpenGL.GL import *
from OpenGL.GLU import *

# szereg zmiennych pomocniczych
viewer = [0.0, 0.0, 10.0] # przechowuje informacje o położeniu obserwatora

theta = 0.0 # zawiera wartość kąta obrotu (oś Y)
phi = 0.0 # zawiera wartość kąta obrotu (oś X)
pix2angle = 1.0 # czynnik skalujący na potrzeby obliczeń
                #- żeby maksymalny ruch myszą odpowiadał obrotowi o 360∘
                # jej wartość jest definiowana w funkcji update_viewport().
scale = 1.0

x_eye = 0
y_eye = 0
z_eye = 0
R = 15

left_mouse_button_pressed = 0 # zawiera stan lewego przycisku myszy
right_mouse_button_pressed = 0 # zawiera stan prawego przycisku myszy
mouse_x_pos_old = 0 # przechowuje ostatnie położenie w poziomie
mouse_y_pos_old = 0 # przechowuje ostatnie położenie w pionie
delta_x = 0 # zawiera informację o różnicy położeń myszy

def startup():
    update_viewport(None, 400, 400)
    glClearColor(0.0, 0.0, 0.0, 1.0)
    glEnable(GL_DEPTH_TEST)

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

# funkcja rysującą przykładowy model
def example_object():
    glColor3f(1.0, 1.0, 1.0)

    quadric = gluNewQuadric()
    gluQuadricDrawStyle(quadric, GLU_LINE)
    glRotatef(90, 1.0, 0.0, 0.0)
    glRotatef(-90, 0.0, 1.0, 0.0)

    gluSphere(quadric, 1.5, 10, 10)

    glTranslatef(0.0, 0.0, 1.1)
    gluCylinder(quadric, 1.0, 1.5, 1.5, 10, 5)
    glTranslatef(0.0, 0.0, -1.1)

    glTranslatef(0.0, 0.0, -2.6)
    gluCylinder(quadric, 0.0, 1.0, 1.5, 10, 5)
    glTranslatef(0.0, 0.0, 2.6)

    glRotatef(90, 1.0, 0.0, 1.0)
    glTranslatef(0.0, 0.0, 1.5)
    gluCylinder(quadric, 0.1, 0.0, 1.0, 5, 5)
    glTranslatef(0.0, 0.0, -1.5)
    glRotatef(-90, 1.0, 0.0, 1.0)

    glRotatef(-90, 1.0, 0.0, 1.0)
    glTranslatef(0.0, 0.0, 1.5)
    gluCylinder(quadric, 0.1, 0.0, 1.0, 5, 5)
    glTranslatef(0.0, 0.0, -1.5)
    glRotatef(90, 1.0, 0.0, 1.0)

    glRotatef(90, 0.0, 1.0, 0.0)
    glRotatef(-90, 1.0, 0.0, 0.0)
    gluDeleteQuadric(quadric)


def render(time):
    global theta
    global phi
    global scale
    global x_eye
    global y_eye
    global z_eye
    global R

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity() # Identyczność / cofnięcie wszystkich przekształceń

    # Przekształcenie patrzenia / przemieszczenie kamery na scenie
    # gluLookAt(viewer[0], viewer[1], viewer[2],
    #           0.0, 0.0, 0.0, 0.0, 1.0, 0.0) 
    angle = math.pi / 180
    #obsługa lewego kławisza
    # wykonano transformacje wierzchołków
    if left_mouse_button_pressed:
        theta += delta_x * pix2angle
        theta = theta % 360     #zakres od 0 do 360 stopni
                                # chodzimy kółkami  
        phi += delta_y * pix2angle
        phi = phi % 360

    # glRotatef(theta, 0.0, 1.0, 0.0)

    # if left_mouse_button_pressed:
        
        
    # glRotatef(phi, 1.0, 0.0, 0.0)

    # obsługa prawego kławisza
    if right_mouse_button_pressed:
        phi += delta_y * pix2angle
        theta += delta_x * pix2angle
        scale *= 1.005
        R /= 1.05
        
    # glRotatef(theta, 0.0, 1.0, 0.0)
    # glRotatef(phi, 1.0, 0.0, 0.0)
    # glScalef(scale, scale, scale)

    # współrzędne kamery
    x_eye = R * math.cos(theta * angle) * math.cos(phi * angle)
    y_eye = R * math.sin(phi * angle)
    z_eye = R * math.sin(theta * angle) * math.cos(phi * angle)
    
    # czy jesteśmy między 90 a 270 stopniami ? oś Y w dół : oś Y w górę
    if(phi * angle >= math.pi / 2 and phi * angle <= 3 * math.pi / 2 ):
        gluLookAt(x_eye, y_eye, z_eye,
              0.0, 0.0, 0.0, 0.0, -1.0, 0.0)
    else:
        gluLookAt(x_eye, y_eye, z_eye,
              0.0, 0.0, 0.0, 0.0, 1.0, 0.0)

    axes()
    example_object()

    glFlush()


def update_viewport(window, width, height):
    global pix2angle
    pix2angle = 360.0 / width

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    # Zmieniono parametry rzutowania – perspektywiczne w zakresie [0.1; 300].
    gluPerspective(70, 1.0, 0.1, 300.0) # Rzutowanie perspektywiczne

    if width <= height:
        glViewport(0, int((height - width) / 2), width, width) # Określenie rozmiaru rzutni w pikselach
    else:
        glViewport(int((width - height) / 2), 0, height, height)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

# Dodano funkcje związane z obsługą zdarzeń klawiatury i myszy
def keyboard_key_callback(window, key, scancode, action, mods):
    if key == GLFW_KEY_ESCAPE and action == GLFW_PRESS:
        glfwSetWindowShouldClose(window, GLFW_TRUE)

# oblicza różnicę w położeniu kursora myszy
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
    global right_mouse_button_pressed

    if button == GLFW_MOUSE_BUTTON_LEFT and action == GLFW_PRESS:
        left_mouse_button_pressed = 1
    else:
        left_mouse_button_pressed = 0

    if button == GLFW_MOUSE_BUTTON_RIGHT and action == GLFW_PRESS:
        right_mouse_button_pressed = 1
    else:
        right_mouse_button_pressed = 0


def main():
    if not glfwInit():
        sys.exit(-1)

    window = glfwCreateWindow(400, 400, __file__, None, None)
    if not window:
        glfwTerminate()
        sys.exit(-1)

    glfwMakeContextCurrent(window)
    glfwSetFramebufferSizeCallback(window, update_viewport)
    # wywołanie do obsługi zdarzeń
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