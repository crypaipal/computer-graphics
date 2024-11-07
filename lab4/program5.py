#!/usr/bin/env python3
import math
import sys

from glfw.GLFW import *
from OpenGL.GL import *
from OpenGL.GLU import *

# szereg zmiennych pomocniczych
viewer = [0.0, 0.0, 0.0] # przechowuje informacje o położeniu obserwatora

theta = 0.0 # zawiera wartość kąta obrotu (oś Y)
phi = 0.0 # zawiera wartość kąta obrotu (oś X)
pix2angle = 1.0 # czynnik skalujący na potrzeby obliczeń
                #- żeby maksymalny ruch myszą odpowiadał obrotowi o 360∘
                # jej wartość jest definiowana w funkcji update_viewport().
scale = 1.0

x_eye = 0
y_eye = 0
z_eye = 0
R = 1

left_mouse_button_pressed = 0 # zawiera stan lewego przycisku myszy
right_mouse_button_pressed = 0 # zawiera stan prawego przycisku myszy
mouse_x_pos_old = 0 # przechowuje ostatnie położenie w poziomie
mouse_y_pos_old = 0 # przechowuje ostatnie położenie w pionie
delta_x = 0 # zawiera informację o różnicy położeń myszy

# mode = 'camera'  # camera - poruszanie kamerą, 
#                 # else - obracanie obiektem

look_dir = [0.0, 0.0, 0.0] # kierunek patrzenia
move_speed = 0.3 # szybkość kamery

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

# przelicza kierunek patrzenia kamery
def update_look_direction():
    global look_dir, theta, phi
    angle = math.pi / 180
    look_dir[0] = R * math.cos(theta * angle) * math.cos(phi * angle)
    look_dir[1] = R * math.sin(phi * angle)
    look_dir[2] = R * math.sin(theta * angle) * math.cos(phi * angle)

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
    # angle = math.pi / 180
    # #obsługa lewego kławisza
    # # wykonano transformacje wierzchołków
    # if mode == 'camera':
    #     if left_mouse_button_pressed:
    #         theta += delta_x * pix2angle
    #         theta = theta % 360     #zakres od 0 do 360 stopni
    #                                 # chodzimy kółkami 
    #         phi += delta_y * pix2angle
    #         phi = phi % 360

    #     if right_mouse_button_pressed:
    #         R /= 1.05  # przybliżamy/oddalamy
    #         if R < 5.0:
    #             R = 5.0  # min odległość kamery od obiektu
    #         elif R > 50.0:
    #             R = 50.0  # max odległość kamery od obiektu

    #     # współrzędne kamery
    #     x_eye = R * math.cos(theta * angle) * math.cos(phi * angle)
    #     y_eye = R * math.sin(phi * angle)
    #     z_eye = R * math.sin(theta * angle) * math.cos(phi * angle)

    #     # czy jesteśmy między 90 a 270 stopniami ? oś Y w dół : oś Y w górę
    #     if(phi * angle >= math.pi / 2 and phi * angle <= 3 * math.pi / 2 ):
    #         gluLookAt(x_eye, y_eye, z_eye,
    #           0.0, 0.0, 0.0, 0.0, -1.0, 0.0)
    #     else:
    #         gluLookAt(x_eye, y_eye, z_eye,
    #           0.0, 0.0, 0.0, 0.0, 1.0, 0.0)
    # # mode obracanie objektem
    # else:
    #     # Przekształcenie patrzenia / przemieszczenie kamery na scenie
    #     gluLookAt(viewer[0], viewer[1], viewer[2],
    #           0.0, 0.0, 0.0, 0.0, 1.0, 0.0) 
    #     if left_mouse_button_pressed:
    #         theta += delta_x * pix2angle
    #         theta = theta % 360         #zakres od 0 do 360 stopni
    #                                     # chodzimy kółkami 
    #         phi += delta_y * pix2angle
    #         phi = phi % 360
        
    #     glRotatef(theta, 0.0, 1.0, 0.0)
    #     glRotatef(phi, 1.0, 0.0, 0.0)

    #     R = 15
    
    gluLookAt(
        viewer[0], viewer[1], viewer[2], # pozycja kamery
        viewer[0] + look_dir[0], viewer[1] + look_dir[1], viewer[2] + look_dir[2], # kierunek, w który patrzymy 
        0.0, 1.0, 0.0 
    )
    spin(0.1 * time * 180 / 3.1415) 
    drawSierpinski(2) 
    axes()  # wywołanie fukcji rysującej układ współrzędnych
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
    # global mode
    if key == GLFW_KEY_ESCAPE and action == GLFW_PRESS:
        glfwSetWindowShouldClose(window, GLFW_TRUE)
    # if key == GLFW_KEY_1 and action == GLFW_PRESS:
    #     mode = 'camera' 
    # if key == GLFW_KEY_2 and action == GLFW_PRESS:
    #     mode = 'else'

    if key == GLFW_KEY_W and action == GLFW_PRESS:
        viewer[0] += look_dir[0] * move_speed
        viewer[1] += look_dir[1] * move_speed
        viewer[2] += look_dir[2] * move_speed
    if key == GLFW_KEY_S and action == GLFW_PRESS:
        viewer[0] -= look_dir[0] * move_speed
        viewer[1] -= look_dir[1] * move_speed
        viewer[2] -= look_dir[2] * move_speed
    if key == GLFW_KEY_A and action == GLFW_PRESS:
        viewer[0] += look_dir[2] * move_speed
        viewer[2] -= look_dir[0] * move_speed
    if key == GLFW_KEY_D and action == GLFW_PRESS:
        viewer[0] -= look_dir[2] * move_speed
        viewer[2] += look_dir[0] * move_speed

# oblicza różnicę w położeniu kursora myszy
def mouse_motion_callback(window, x_pos, y_pos):
    global delta_x
    global delta_y
    global mouse_x_pos_old
    global mouse_y_pos_old
    global theta
    global phi

    delta_x = x_pos - mouse_x_pos_old
    mouse_x_pos_old = x_pos

    delta_y = y_pos - mouse_y_pos_old
    mouse_y_pos_old = y_pos

    theta += delta_x * pix2angle
    phi += delta_y * pix2angle
    
    # ograniczamy kąt z -89 do 89 aby nie było pełnego obrotu 
    if phi > 89:
        phi = 89
    elif phi < -89:
        phi = -89

    update_look_direction()


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
