import numpy as np
from contracts import contract
from . import Controller

class Zero(Controller):
    
    @contract(ncommands='int,>=1')
    def __init__(self, ncommands):
        self.ncommands = ncommands
        
    def init(self, vehicle_spec):
        pass
    
    def process_observations(self, observations):
        pass
    
    def choose_commands(self):
        return np.zeros(self.ncommands)
