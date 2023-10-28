from OpenGL.GL import *
import glm
from numpy import array, float32
import pygame


class Model(object):
    def __init__(self, data: list) -> None:
        self.vertBuffer = array(data, dtype=float32)

        self.VBO = glGenBuffers(1)  # Vertex Model Object

        self.VAO = glGenVertexArrays(1)  # Vertex Array Object

        self.position = glm.vec3(0, 0, 0)
        self.rotation = glm.vec3(0, 0, 0)
        self.scale = glm.vec3(1, 1, 1)

    def loadTexture(self, path: str) -> None:
        self.textureSurface = pygame.image.load(path)
        self.textureData = pygame.image.tostring(self.textureSurface, "RGB", 1)
        self.textureBuffer = glGenTextures(1)

    def getModelMatrix(self) -> glm.mat4:
        model = glm.mat4(1.0)
        model = glm.translate(model, self.position)
        model = glm.rotate(model, glm.radians(
            self.rotation.x), glm.vec3(1, 0, 0))    # pitch
        model = glm.rotate(model, glm.radians(
            self.rotation.y), glm.vec3(0, 1, 0))    # yaw
        model = glm.rotate(model, glm.radians(
            self.rotation.z), glm.vec3(0, 0, 1))    # roll
        model = glm.scale(model, self.scale)
        return model

    def render(self) -> None:
        # Where is gonna be stored the information of the vertex buffer
        glBindBuffer(GL_ARRAY_BUFFER, self.VBO)
        glBindVertexArray(self.VAO)

        # Specifying the information of the vertex buffer
        glBufferData(GL_ARRAY_BUFFER,        # Model ID (VBO)
                     self.vertBuffer.nbytes,  # Size of the buffer in bytes
                     self.vertBuffer,        # Data to be copied to the buffer
                     GL_STATIC_DRAW)         # How the buffer is going to be used

        # Specifying the attributes of the vertex buffer
        glVertexAttribPointer(0,                  # Attribute index
                              3,                  # Number of elements per vertex
                              GL_FLOAT,           # Type of the elements
                              GL_FALSE,           # Normalized?
                              4 * 8,              # Stride, 3 floats, each float is 4 bytes
                              ctypes.c_void_p(0))  # Array buffer offset

        glEnableVertexAttribArray(0)

        glVertexAttribPointer(1,                  # Attribute index
                              3,                  # Number of elements per vertex
                              GL_FLOAT,           # Type of the elements
                              GL_FALSE,           # Normalized?
                              4 * 8,              # Stride, 3 floats, each float is 4 bytes
                              ctypes.c_void_p(4*3))  # Array buffer offset

        glEnableVertexAttribArray(1)

        # UVs

        glVertexAttribPointer(2,                  # Attribute index
                              2,                  # Number of elements per vertex
                              GL_FLOAT,           # Type of the elements
                              GL_FALSE,           # Normalized?
                              4 * 8,              # Stride, 3 floats, each float is 4 bytes
                              ctypes.c_void_p(4*6))

        glEnableVertexAttribArray(2)

        # Texture
        glActiveTexture(GL_TEXTURE0)
        glBindTexture(GL_TEXTURE_2D, self.textureBuffer)

        glTexImage2D(GL_TEXTURE_2D,                     # Target
                     0,                                 # Level
                     GL_RGB,                            # Internal format
                     self.textureSurface.get_width(),   # Width
                     self.textureSurface.get_height(),  # Height
                     0,                                 # Border
                     GL_RGB,                            # Format
                     GL_UNSIGNED_BYTE,                  # Type
                     self.textureData)                  # Data

        glGenerateTextureMipmap(self.textureBuffer)
        # glGenerateMipmap(GL_TEXTURE_2D)

        glDrawArrays(GL_TRIANGLES, 0, len(self.vertBuffer) // 8)
