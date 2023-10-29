class ObjectLoader(object):
    def __init__(self) -> None:
        self.buffer = []

    def loadObject(self, path: str) -> None:
        if self.buffer != []:
            self.cleanUp()

        vertexCoords = []
        textureCoords = []
        normalCoords = []

        allIndices = []  # [vertex, texture, normal] AKA face

        with open(path, "r") as file:
            line = file.readline()
            while line:
                values = line.split()
                match values[0]:
                    case 'v':
                        vertexCoords.extend([float(value)
                                             for value in values[1:4]])
                    case 'vt':
                        textureCoords.extend([float(value)
                                              for value in values[1:3]])
                    case 'vn':
                        normalCoords.extend([float(value)
                                             for value in values[1:4]])
                    case 'f':
                        for value in values[1:]:
                            split = value.split('/')
                            allIndices.extend(
                                [int(index) - 1 for index in split])

                line = file.readline()

        # Sort the indices
        for i, index in enumerate(allIndices):
            # get remaining indices
            remainder = i % 3
            match remainder:
                case 0:
                    startAt = index * 3
                    endAt = startAt + 3
                    self.buffer.extend(vertexCoords[startAt:endAt])
                case 1:
                    startAt = index * 2
                    endAt = startAt + 2
                    self.buffer.extend(textureCoords[startAt:endAt])
                case 2:
                    startAt = index * 3
                    endAt = startAt + 3
                    self.buffer.extend(normalCoords[startAt:endAt])

        # Final order of the buffer
        # [vertex, texture, normal, vertex, texture, normal, ...]
        return self.buffer

    def cleanUp(self):
        self.buffer = []

# References: https://github.com/totex/Learn-OpenGL-in-python/blob/master/ObjLoader.py
