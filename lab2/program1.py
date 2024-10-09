#!/usr/bin/env python3
import sys

from glfw.GLFW import *

from OpenGL.GL import *
from OpenGL.GLU import *


def startup():
    update_viewport(None, 400, 400) # dla poprawnego działania kodu
    glClearColor(0.0, 0.0, 0.0, 1.0) # kolor oczyszczenia ekranu (rgb)


def shutdown():
    pass    # placeholder


def render(time):
    glClear(GL_COLOR_BUFFER_BIT) # wyczyszczenie ramki w pamięci

    glBegin(GL_TRIANGLES)   # jako argument funkcji wskazuje się prymityw do rysowania
    glColor3f(1.0, 0.0, 1.0)# wywołanie glColor() może się znaleźć przed każdym glVertex()
    glVertex2f(0.0, 0.0)    # umieszcza wierzchołek w pamięci, 
    glColor3f(1.0, 1.0, 0.0)# wywołanie glColor() może się znaleźć przed każdym glVertex()
    glVertex2f(0.0, 50.0)   # prymityw jest rysowany po podaniu mu odpowiedniej liczby wierzchołków
    glColor3f(0.0, 1.0, 1.0)# wywołanie glColor() może się znaleźć przed każdym glVertex()
    glVertex2f(50.0, 0.0)
    glEnd()

    glBegin(GL_TRIANGLES)   # jako argument funkcji wskazuje się prymityw do rysowania
    glColor3f(0.0, 1.0, 0.0)
    glVertex2f(0.0, 0.0)
    glColor3f(0.0, 0.0, 1.0)
    glVertex2f(0.0, 50.0)
    glColor3f(1.0, 0.0, 0.0)
    glVertex2f(-50.0, 0.0)
    glEnd()

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