#!/usr/bin/env python3
import sys
import random

from glfw.GLFW import *

from OpenGL.GL import *
from OpenGL.GLU import *

color = random.random()

def startup():
    update_viewport(None, 400, 400) # dla poprawnego działania kodu
    glClearColor(0.0, 0.0, 0.0, 1.0) # kolor oczyszczenia ekranu (rgb)

def shutdown():
    pass    # placeholder

def drawRectangle(x, y, a, b):    
    random.seed(color)  # za każdym razem sekwencja liczb losowych będzie taka sama dla danej wartości koloru
    r1 = random.random()
    g1 = random.random()
    b1 = random.random()

    glColor3f(r1, g1, b1)
    glBegin(GL_TRIANGLES)
    glVertex2f(x, y)
    glVertex2f(x + a, y)
    glVertex2f(x, y - b)
    glEnd()

    glBegin(GL_TRIANGLES)
    glVertex2f(x + a, y)
    glVertex2f(x, y - b)
    glVertex2f(x + a, y - b)
    glEnd()

# [00 01 02]
# [10 11 12]
# [20 21 22]
def drawCarpet(x, y, a, b, similarity):
    if(similarity == 0):
        drawRectangle(x, y, a, b)
    else:
        a2 = a / 3 # podział prostokątu na 9 części
        b2 = b / 3  # każda część 1/3 szerokości, 1/3 wysokości oryg prostokąta
        similarity = similarity - 1
        for i in range(3):
            for j in range(3):
                if i != 1 or j != 1: # prostokąt centralny
                    x2 = x + i * a2
                    y2 = y - j * b2
                    drawCarpet(x2, y2, a2, b2, similarity)

def render(time):
    glClear(GL_COLOR_BUFFER_BIT) # wyczyszczenie ramki w pamięci
    drawCarpet(-60, 40, 120, 80, 2)
    glFlush()   # zawartość pamięci jest przesyłana do wyświetlenia


def update_viewport(window, width, height):
    if width == 0:
        width = 1
    if height == 0:
        height = 1
    aspect_ratio = width / height

    glMatrixMode(GL_PROJECTION) # przełączanie na macierz projekcji
    glViewport(0, 0, width, height) # rozmiary okna do renderinga
    glLoadIdentity() # to wywołanie resetuje bieżącą macierz, aby zignorować poprzedni stan
                    # zaczyna z macierzy jednostkowej

    if width <= height: # szerokość pozostaje stała, wysokość zmienia się w zależności od współczynnika proporcji
        glOrtho(-100.0, 100.0, -100.0 / aspect_ratio, 100.0 / aspect_ratio,
                1.0, -1.0)  # arg: lewa, prawa, dolna i górna granica widocznego obszaru, 
                            # 1, -1 wskazują że obiekty poza tymi granicami wzdłuż osi Z nie będą widoczne
    else:                  # wysokość jest stała, szerokość się zmienia  
        glOrtho(-100.0 * aspect_ratio, 100.0 * aspect_ratio, -100.0, 100.0,
                1.0, -1.0)

    glMatrixMode(GL_MODELVIEW) # przełączenie na macierz modelowania
    glLoadIdentity()


def main():
    if not glfwInit(): 
        sys.exit(-1) # jeśłi coś się nie powiodło, kończymy program

    window = glfwCreateWindow(400, 400, __file__, None, None) # tworzymy okno rozmiarów 400x400 o nazwie __file__
    if not window:
        glfwTerminate()
        sys.exit(-1)    # w przypadku niepowodzenia kończymy program

    glfwMakeContextCurrent(window)  # określa miejsce aktywnego obecnie kontekstu OpenGL, w którym miejscu generowany będzie przez nas obraz
    glfwSetFramebufferSizeCallback(window, update_viewport) # dla poprawnego działania kodu (update_viewport)
    glfwSwapInterval(1) # włącza tak zwaną synchronizację pionową, wpływa na funkcję glfwSwapBuffers(), ogranicza szybkość

    startup()
    while not glfwWindowShouldClose(window): # powtarzamy do zamknięcia okna
        render(glfwGetTime())   # wykonujemy funkcję render() i podmieniamy ramki obrazu
        glfwSwapBuffers(window) # dodatkowo przetworzone zostaną zaistniałe zdarzenia okien i wejść
        glfwPollEvents()
    shutdown()

    glfwTerminate()


if __name__ == '__main__':
    main()