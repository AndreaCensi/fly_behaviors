import numpy as np
from . import Controller

class Random(Controller):
    
    def __init__(self, ncommands):
        self.ncommands = ncommands
        
    def init(self, vehicle_spec):
        pass
    
    def process_observations(self, observations):
        pass
    
    def choose_commands(self):
        return (np.random.rand(self.ncommands) - 0.5) * 2
