import os

import pandas as pd
import valohai

params = {
    "param1": True,
    "param2": "asdf",
    "param3": 123,
    "param4": 0.0001,
}

inputs = {"input1": "asdf", "input2": ["yolol", "yalala"]}


def prepare(a, b):
    print("this is fake method %s %s" % (a, b))


foobar = pd.read_csv("yeah.csv")  # Assignment that can't be evaluated (and should be ignored) by AST parser
prepare("this should not be parsed", "ever")
valohai.utils.prepare(step="this should not be parsed either")
valohai.prepare(step="foobar1", parameters=params, inputs=inputs)
