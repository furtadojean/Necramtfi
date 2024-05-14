"""Provides functions to deal with textures."""

from OpenGL.GL import GL_NEAREST, GL_NEAREST_MIPMAP_LINEAR, GL_REPEAT, GL_RGBA, GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_TEXTURE_MIN_FILTER, GL_TEXTURE_WRAP_S, GL_TEXTURE_WRAP_T, GL_UNSIGNED_BYTE
from OpenGL.GL import glBindTexture, glEnable, glGenerateMipmap, glTexImage2D, glGenTextures, glTexParameteri
from PIL import Image

def textures_create(size):
    return _texture_bank(size)

def textures_load(textures, name, filepath, parameters=None):
    if textures._current_index >= textures.size:
        return None


    glBindTexture(textures.type, textures.bank[textures._current_index])

    if parameters == None:
        textures.default_parameters()
    else:
        parameters()

    try:
        img = Image.open(filepath)
        img_width = img.size[0]
        img_height = img.size[1]
        converted = img.convert("RGBA")
        image_data = converted.tobytes("raw", "RGBA", 0, -1)
        glTexImage2D(textures.type, 0, GL_RGBA, img_width, img_height, 0, GL_RGBA, GL_UNSIGNED_BYTE, image_data)
        glGenerateMipmap(textures.type)

        textures.named_textures[name] = textures.bank[textures._current_index]
        textures._current_index += 1
    except:
        print("Texture {} could not be loaded. Path: {}".format(name, filepath))

def textures_use(textures, name):
    if name not in textures.named_textures:
        glBindTexture(textures.type, 0)
        return None

    glBindTexture(textures.type, textures.named_textures[name])



class _texture_bank():
    def __init__(self, size, type=GL_TEXTURE_2D):
        glEnable(type)
        self.type = type
        self.size = size
        self.bank = glGenTextures(size+1)
        self.named_textures = dict()
        self._current_index = 0

    def default_parameters(self):
        glTexParameteri(self.type, GL_TEXTURE_WRAP_S, GL_REPEAT)
        glTexParameteri(self.type, GL_TEXTURE_WRAP_T, GL_REPEAT)
        glTexParameteri(self.type, GL_TEXTURE_MIN_FILTER, GL_NEAREST_MIPMAP_LINEAR)
        glTexParameteri(self.type, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
