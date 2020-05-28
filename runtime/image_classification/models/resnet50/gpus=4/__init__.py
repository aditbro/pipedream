from .resnet50 import RESNET50Partitioned
from .stage0 import Stage0
from .stage1 import Stage1

def arch():
    return "resnet50"

def model(criterion):
    return [
        (Stage0(), ["input0"], ["out1"]),
        (Stage1(), ["out1"], ["out2"]),
        (criterion, ["out2"], ["loss"])
    ]

def full_model():
    return RESNET50Partitioned()
