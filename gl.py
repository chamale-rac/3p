from OpenGL.GL import *
from model import Model
from pygame import Surface
from OpenGL.GL.shaders import compileProgram, compileShader
import glm


class Renderer(object):
    def __init__(self, screen: Surface) -> None:
        self.screen = screen
        _, _, self.width, self.height = screen.get_rect()
        self.clearColor = (0.152, 0.152, 0.152, 1.0)
        self.lightPos = glm.vec3(0, 0, 0)

        glEnable(GL_DEPTH_TEST)

        glViewport(0, 0, self.width, self.height)

        self.fillMode = True
        self.sceneObjects: list[Model] = []

        self.activeShader = None

        self.camPosition = glm.vec3(0, 0, 0)
        self.camRotation = glm.vec3(0, 0, 0)

        # Projection matrix
        # fovy, aspect, near, far
        self.projectionMatrix = glm.perspective(
            glm.radians(45), (self.width / self.height), 0.1, 1000)
        self.viewMatrix = self.getViewMatrix()

        self.elapsedTime = 0.0
        self.target = glm.vec3(0, 0, 0)

    def toggleFillMode(self) -> None:
        self.fillMode = not self.fillMode
        if self.fillMode:
            glEnable(GL_CULL_FACE)  # Cull back faces
            glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
        else:
            glDisable(GL_CULL_FACE)
            glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)

    def getViewMatrix(self) -> glm.mat4:
        view = glm.mat4(1.0)
        view = glm.translate(view, self.camPosition)
        view = glm.rotate(view, glm.radians(
            self.camRotation.x), glm.vec3(1, 0, 0))    # pitch
        view = glm.rotate(view, glm.radians(
            self.camRotation.y), glm.vec3(0, 1, 0))    # yaw
        view = glm.rotate(view, glm.radians(
            self.camRotation.z), glm.vec3(0, 0, 1))    # roll
        view = glm.inverse(view)    # Inverting the view matrix

        return view

    def setShaders(self, vertexShader, fragmentShader) -> None:
        if vertexShader != None and fragmentShader != None:
            with open(vertexShader, 'r') as f:
                vertex_src = f.readlines()

            with open(fragmentShader, 'r') as f:
                fragment_src = f.readlines()

            self.activeShader = compileProgram(compileShader(vertex_src, GL_VERTEX_SHADER),
                                               compileShader(fragment_src, GL_FRAGMENT_SHADER))
        else:
            self.activeShader = None

    def update(self) -> None:
        self.viewMatrix = glm.lookAt(
            self.camPosition, self.target, glm.vec3(0, 1, 0))

    def render(self) -> None:
        glClearColor(*self.clearColor)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)  # type: ignore

        if self.activeShader != None:
            glUseProgram(self.activeShader)
            glUniformMatrix4fv(glGetUniformLocation(self.activeShader, 'viewMatrix'),
                               1, GL_FALSE, glm.value_ptr(self.viewMatrix))
            glUniformMatrix4fv(glGetUniformLocation(self.activeShader, 'projectionMatrix'),
                               1, GL_FALSE, glm.value_ptr(self.projectionMatrix))

            glUniform1f(glGetUniformLocation(self.activeShader,
                        'time'), self.elapsedTime)

        for obj in self.sceneObjects:
            if self.activeShader != None:
                glUniformMatrix4fv(glGetUniformLocation(self.activeShader, 'modelMatrix'),
                                   1, GL_FALSE, glm.value_ptr(obj.getModelMatrix()))

                # send light position to shader
                glUniform3fv(glGetUniformLocation(self.activeShader,
                                                  'lightPos'), 1, glm.value_ptr(self.lightPos))

                # send camera position to shader
                glUniform3fv(glGetUniformLocation(self.activeShader,
                                                  'camPos'), 1, glm.value_ptr(self.camPosition))
                # send time
                glUniform1f(glGetUniformLocation(self.activeShader,
                            'time'), self.elapsedTime)
                # send width and height
                glUniform1f(glGetUniformLocation(self.activeShader,
                            'width'), self.width)
                glUniform1f(glGetUniformLocation(self.activeShader,
                            'height'), self.height)
                # send view matrix
                glUniformMatrix4fv(glGetUniformLocation(self.activeShader, 'viewMatrix'),
                                   1, GL_FALSE, glm.value_ptr(self.viewMatrix))

            obj.render()
