import numpy as np
from contracts import contract
from . import Controller

class Zero(Controller):
    
    @contract(ncommands='int,>=1')
    def __init__(self, ncommands):
        self.ncommands = ncommands
        
    def get_angular_velocity(self, directions, luminance):
        return np.zeros(self.ncommands)
