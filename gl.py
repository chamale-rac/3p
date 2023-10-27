from OpenGL.GL import *
from model import Model
from pygame import Surface
from OpenGL.GL.shaders import compileProgram, compileShader
import glm

class Renderer(object):
    def __init__(self, screen: Surface) -> None:
        self.screen = screen
        _, _, self.width, self.height = screen.get_rect()
        self.clearColor = (0.0, 0.0, 0.0, 1.0)

        glEnable(GL_DEPTH_TEST)
        glViewport(0, 0, self.width, self.height)

        self.sceneObjects: list[Model] = []

        self.activeShader = None

        # View matrix
        self.camPosition = glm.vec3(0,0,0)
        self.camRotation = glm.vec3(0,0,0)

        # Projection matrix
                                # fovy, aspect, near, far
        self.projectionMatrix = glm.perspective(glm.radians(45), (self.width / self.height), 0.1, 1000)
     

    def getViewMatrix(self) -> glm.mat4:
        view = glm.mat4(1.0)
        view = glm.translate(view, self.camPosition)
        view = glm.rotate(view, glm.radians(self.camRotation.x), glm.vec3(1,0,0))    # pitch
        view = glm.rotate(view, glm.radians(self.camRotation.y), glm.vec3(0,1,0))    # yaw
        view = glm.rotate(view, glm.radians(self.camRotation.z), glm.vec3(0,0,1))    # roll
        view = glm.inverse(view)    # Inverting the view matrix

        return view

    def setShaders(self, vertexShader, fragmentShader) -> None:
        if vertexShader != None and fragmentShader != None:
            self.activeShader = compileProgram(compileShader(vertexShader, GL_VERTEX_SHADER),
                                           compileShader(fragmentShader, GL_FRAGMENT_SHADER))
        else:
            self.activeShader = None

    def render(self) -> None:
        glClearColor(*self.clearColor)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        if self.activeShader != None:
            glUseProgram(self.activeShader)
            glUniformMatrix4fv(glGetUniformLocation(self.activeShader, 'viewMatrix'), 
                               1, GL_FALSE, glm.value_ptr(self.getViewMatrix()))
            glUniformMatrix4fv(glGetUniformLocation(self.activeShader, 'projectionMatrix'),
                               1, GL_FALSE, glm.value_ptr(self.projectionMatrix))
                

        for obj in self.sceneObjects:
            if self.activeShader != None:
                glUniformMatrix4fv(glGetUniformLocation(self.activeShader, 'modelMatrix'),
                                   1, GL_FALSE, glm.value_ptr(obj.getModelMatrix()))

            obj.render()
