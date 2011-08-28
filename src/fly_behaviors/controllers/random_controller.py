import numpy as np
from . import Controller

class Random(Controller):
    
    def __init__(self, ncommands):
        self.ncommands = ncommands
        
    def get_angular_velocity(self, directions, luminance):
        return (np.random.rand(self.ncommands) - 0.5) * 2
