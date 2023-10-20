from OpenGL.GL import *
from numpy import array, float32, uint32

class Buffer(object):
    def __init__(self, data: list) -> None:
        self.vertBuffer = array(data, dtype=float32)
        
        self.VBO = glGenBuffers(1) # Vertex Buffer Object

        self.VAO = glGenVertexArrays(1) # Vertex Array Object

    def render(self) -> None:
        # Where is gonna be stored the information of the vertex buffer
        glBindBuffer(GL_ARRAY_BUFFER, self.VBO)
        glBindVertexArray(self.VAO)

        # Specifying the information of the vertex buffer
        glBufferData(GL_ARRAY_BUFFER,        # Buffer ID (VBO)
                     self.vertBuffer.nbytes, # Size of the buffer in bytes
                     self.vertBuffer,        # Data to be copied to the buffer
                     GL_STATIC_DRAW)         # How the buffer is going to be used

        # Specifying the attributes of the vertex buffer
        glVertexAttribPointer(0,                  # Attribute index
                              3,                  # Number of elements per vertex
                              GL_FLOAT,           # Type of the elements
                              GL_FALSE,           # Normalized?
                              4 * 6,              # Stride, 3 floats, each float is 4 bytes
                              ctypes.c_void_p(0)) # Array buffer offset

        glEnableVertexAttribArray(0)

        glVertexAttribPointer(1,                  # Attribute index
                              3,                  # Number of elements per vertex
                              GL_FLOAT,           # Type of the elements
                              GL_FALSE,           # Normalized?
                              4 * 6,              # Stride, 3 floats, each float is 4 bytes
                              ctypes.c_void_p(4*3)) # Array buffer offset

        glEnableVertexAttribArray(1)

        glDrawArrays(GL_TRIANGLES, 0, len(self.vertBuffer) // 3)
        
