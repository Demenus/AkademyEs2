# -*- coding: utf-8 -*-

""" Copyright (C) 2011  Aarón Negrín Santamaría

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>."""

import pygame
from pygame.locals import *

from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GL.shaders import *


WIDTH = 600
HEIGHT = 600

vertices = (GLfloat * (4*4))(
    1.0, 1.0, 0.0, 1.0,
    1.0,-1.0, 0.0, 1.0,
    -1.0,-1.0, 0.0, 1.0,
    -1.0, 1.0, 0.0, 1.0)

#Matriz de rotación, esta al ser aplicada sobre un punto
#lo rota 45 grados alrededor del eje X
rotacion = (GLfloat * (4*4))(
    1.0, 0.0, 0.0, 0.0,
    0.0, 0.707107, 0.707107, 0.0,
    0.0, -0.707107, 0.707107, 0.0,
    0.0, 0.0, 0.0, 1.0)

faceIndex = (GLushort * 4)(0, 1, 2, 3)

def init():
    pygame.init()

    flags = DOUBLEBUF|OPENGL|RESIZABLE
    screen = pygame.display.set_mode((WIDTH, HEIGHT), flags)


def init_gl():
    glClearColor(0.0,0.0,0.0,1.0); 
    glClearDepth(1.0);

def resize_glscene(w,h):
    glViewport(0,0,w,h);

    glMatrixMode(GL_PROJECTION);
    glLoadIdentity();

    gluPerspective(45.0, float(w)/float(h), 0.1, 100.0);

    glMatrixMode(GL_MODELVIEW);
    glLoadIdentity();
    
def draw_scene(position):
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);

    glLoadIdentity();
    glTranslatef(0.0, 0.0, -6.0);

    glVertexAttribPointer(position, 4, GL_FLOAT, 1, 0, vertices);
    glEnableVertexAttribArray(position);

    glDrawElements(GL_QUADS, len(faceIndex), GL_UNSIGNED_SHORT, faceIndex);

    glDisableVertexAttribArray(position);


def load_Shaders(vsFileName, fsFileName):
    program = glCreateProgram();

    vsSource = open(vsFileName, 'r').read()
    fsSource = open(fsFileName, 'r').read()

    vsShader = glCreateShader(GL_VERTEX_SHADER);   
    glShaderSource(vsShader, vsSource);

    fsShader = glCreateShader(GL_FRAGMENT_SHADER); 
    glShaderSource(fsShader, fsSource);

    glCompileShader(vsShader);
    glCompileShader(fsShader);

    glAttachShader(program, vsShader);
    glAttachShader(program, fsShader);

    glLinkProgram(program);

    return program



def main():
    running = True
    init()
    init_gl()
    resize_glscene(WIDTH, HEIGHT)

    program = load_Shaders("Shader2.vsh", "Shader2.fsh")
    glUseProgram(program);

    #Recibimos las localizaciones de las variables de atributos de position
    #Y se la atribuimos a la variable "position" del shader
    position = glGetAttribLocation(program, "position");
    glBindAttribLocation(program, position, "position");

    #Recibimos las localizaciones de las variables uniformes matriz y t
    matriz = glGetUniformLocation(program, "matriz");
    t = glGetUniformLocation(program, "t");

    
    #Declaramos dos variables para recorrer el intervalo [0,1]
    h = 0.0
    suma = True

    clock = pygame.time.Clock()

    while running:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
        draw_scene(position)

        #Pasamos al programa actual la matriz de rotacion asi
        #como el parametro t que recorre el intervalo [0,1]
        #Ver comentarios en el VS para mas informacion
        glUniformMatrix4fv(matriz, 1, 0, rotacion);
        glUniform1f(t, (GLfloat)(h));

        #Recorremos el intervalo [0,1] arriba y abajo
        #Si llegamos al 1 empezamos a retroceder hacia el 0
        #Si llegamos al 0 empezamos a aumentar hacia el 1
        if suma:
            h = h + 0.01
            if h >= 1.0:
                suma = False
                h = 1.0
        if (not suma):
            h = h - 0.01
            if h <= 0.0:
                suma = True
                h = 0.0

        pygame.display.flip()

    pygame.quit()

main()
	
