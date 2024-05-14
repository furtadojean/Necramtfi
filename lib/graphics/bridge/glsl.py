from enum import Enum

class var:
    """Represents a shader variable.

    Instance methods:
        get_declaration -- gets a declaration statement
        get_new -- gets a new variable expression
    """

    SQualifier = Enum('SQualifier', ['uniform', 'attribute', 'varying'])
    DType = Enum('DType', ['vec2', 'vec3', 'vec4', 'mat4', 'sampler2D'])

    def __init__(self, dtype):
        self.dtype = dtype

    def get_declaration(self, squalifier, name):
        return "{} {} {};".format(squalifier.name, self.dtype.name, name)

    def get_new(self, value):
        return "{}({})".format(self.dtype.name, value)

# Some default instances
vec2 = var(var.DType.vec2)
vec3 = var(var.DType.vec3)
vec4 = var(var.DType.vec4)
mat4 = var(var.DType.mat4)

class GLSL:
    """Allows to non-sequentially modify shader code.

    Instance attributes:
        code: str [ro] -- gets the full code
    Instance methods:
        add_to_global -- adds global code
        add_to_function -- adds code to a function
    """

    def __init__(self):
        self._global_code = ""
        self._function_to_code = {
            "void main()": ""
        }
    @property
    def code(self):
        return \
                self._global_code \
                + \
                '\n'.join([name+' {\n'+self._function_to_code[name]+'\n}' for name in self._function_to_code])

    def add_to_global(self, string):
        self._global_code += string + '\n'

    def add_to_function(self, name, string):
        if name not in self._function_to_code:
            self._function_to_code[name] = string
        else:
            self._function_to_code[name] += '\n' + string
