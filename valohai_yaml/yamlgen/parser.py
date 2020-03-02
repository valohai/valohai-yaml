import ast
from collections import namedtuple
from typing import List


def is_module_function_call(node, module, function):
    try:
        return node.func.attr == function and node.func.value.id == module
    except AttributeError:
        return False


class PrepareParser(ast.NodeVisitor):
    """Parses .py file for Valohai inputs, parameters, step name

    Using AST parser, visits all method calls of a Python file.

    If a call to valohai.prepare() method is found, iterate through
    it's arguments and look for inputs, parameters and a step name.

    All possible ways to call prepare() are not supported

    Works:
        valohai.prepare(parameters={"param1": "foobar"})

    Works:
        parameters={"param1": "foobar"}
        valohai.prepare(parameters=parameters)

    Fails:
        import valohai as herpderp
        herpderp.prepare(parameters={"param1": "foobar"})

    Fails:
        from valohai import prepare
        prepare(parameters={"param1": "foobar"})

    Fails:
        valohai.prepare(parameters=get_parameters())

    """

    def __init__(self):
        self.assignments = {}
        self.parameters = {}
        self.inputs = {}
        self.step = None

    def visit_Assign(self, node):
        try:
            self.assignments[node.targets[0].id] = ast.literal_eval(node.value)
        except ValueError:
            # We don't care about assignments that can't be literal_eval():ed
            pass

    def visit_Call(self, node):
        if is_module_function_call(node, "valohai", "prepare"):
            self.process_valohai_prepare_call(node)

    def process_valohai_prepare_call(self, node):
        self.step = "default"
        if hasattr(node, "keywords"):
            for key in node.keywords:
                if key.arg == "parameters":
                    if isinstance(key.value, ast.Name) and key.value.id in self.assignments:
                        self.parameters = self.assignments[key.value.id]
                    elif isinstance(key.value, ast.Dict):
                        self.parameters = ast.literal_eval(key.value)
                    else:
                        raise NotImplementedError()
                elif key.arg == "inputs":
                    if isinstance(key.value, ast.Name) and key.value.id in self.assignments:
                        self.inputs = {
                            key: value if isinstance(value, List) else [value]
                            for key, value in self.assignments[key.value.id].items()
                        }
                    elif isinstance(key.value, ast.Dict):
                        self.inputs = {
                            key: value if isinstance(value, List) else [value]
                            for key, value in ast.literal_eval(key.value).items()
                        }
                    else:
                        raise NotImplementedError()
                elif key.arg == "step":
                    self.step = ast.literal_eval(key.value)


def parse(source):
    tree = ast.parse(source)
    parser = PrepareParser()
    parser.visit(tree)
    result = namedtuple("result", ["step", "parameters", "inputs"])
    return result(step=parser.step, parameters=parser.parameters, inputs=parser.inputs)
