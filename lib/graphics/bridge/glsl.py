from enum import Enum

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
