from Tools import Tools
import json


class Arch:
    def __init__(self):
        self.name = ''
        self.switch_name = ''
        self.pipeline = []
        self.libraries = []
        self.intrinsic_metadata = {}
        self.user_defined_metadata = {}
        self.prog_blocks = {}
        self.headers = {}
        self.defines = {}
        self.constants = {}
        self.typedefs = {}
        self.main = {}

    def parse(self, path_to_obj):

        with open(path_to_obj) as f:
            arch_file = json.load(f)

        self.name = arch_file['Name']
        self.switch_name = arch_file['Switch Name']
        self.pipeline = arch_file['Pipeline']
        self.libraries = arch_file['Default Libraries']
        self.intrinsic_metadata = arch_file['Intrinsic Metadata']
        self.user_defined_metadata = arch_file['User-defined Metadata']
        self.headers = arch_file['Headers']
        self.defines = arch_file['Defines']
        self.main = arch_file['Main']

        for key, value in arch_file["Programmable Blocks"].items():
            block = self.ProgrammableBlock()
            block.extract(key, value)
            self.prog_blocks[key] = block

        for key, value in arch_file["Constants"].items():
            constant = self.Constant()
            constant.extract(key, value)
            self.constants[key] = constant

        for key, value in arch_file["Typedefs"].items():
            typedef = self.Typedef()
            typedef.extract(key, value)
            self.typedefs[key] = typedef

        for key, value in arch_file["Defines"].items():
            define = self.Define()
            define.extract(key, value)
            self.defines[key] = define


    class ProgrammableBlock:
        def __init__(self):
            self.name = ''
            self.type = ''
            self.filename = ''
            self.has_apply = False
            self.abstraction = ''
            self.default_methods = []
            self.parameters = []

        def extract(self, name, block):
            self.name = name
            self.type = block['type']
            self.filename = block['filename']
            self.has_apply = Tools.str_to_bool(block["has_apply"])
            self.abstraction = block['abstraction']
            self.default_methods = block.get("default_methods", [])

            for one_param in block["parameters"]:
                param = self.Parameter()
                param.extract(one_param)
                self.parameters.append(param)

        class Parameter:
            def __init__(self):
                self.name = ''
                self.type = ''
                self.direction = ''

            def extract(self, p):
                self.name = p["name"]
                self.type = p["type"]
                self.direction = p.get("direction", None)

            def get_num_params(self):
                i = 0
                for k,v in self.__dict__.items():
                    if v:
                        i += 1
                return i

            def get_attr_dict(self):
                return self.__dict__



            def __nonempty__(self):
                return bool(self.name and self.type)

    class Constant:
        def __init__(self):
            self.name = ''
            self.bitwidth = 0
            self.value = ''

        def extract(self, n, p):
            self.name = n
            self.bitwidth = p["bitwidth"]
            self.value = p["value"]

    class Typedef:
        def __init__(self):
            self.name = ''
            self.bitwidth = 0

        def extract(self, n, p):
            self.name = n
            self.bitwidth = p["bitwidth"]

    class Define:
        def __init__(self):
            self.name = ''
            self.value = 0

        def extract(self, n, p):
            self.name = n
            self.value = p["value"]
