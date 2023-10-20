from OpenGL.GL import *
from buffer import Buffer
from pygame import Surface
from OpenGL.GL.shaders import compileProgram, compileShader

class Renderer(object):
    def __init__(self, screen: Surface) -> None:
        self.screen = screen
        _, _, self.width, self.height = screen.get_rect()
        self.clearColor = (0.0, 0.0, 0.0, 1.0)

        glEnable(GL_DEPTH_TEST)
        glViewport(0, 0, self.width, self.height)

        self.sceneObjects: list[Buffer] = []

        self.activeShader = None

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

        for obj in self.sceneObjects:
            obj.render()
