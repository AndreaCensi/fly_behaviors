from collections import namedtuple
from abc import abstractmethod, ABCMeta

# Description of the vehicle
#  directions: array of theta
VehicleSpec = namedtuple('VehicleSpec', 'directions')
    
# 
VehicleObservations = namedtuple('VehicleObservations', 'time dt luminance')


class Controller:

    __metaclass__ = ABCMeta
 
    @abstractmethod
    def init(self, vehicle_spec):
        pass
    
    @abstractmethod
    def process_observations(self, observations):
        pass
    
    @abstractmethod
    def choose_commands(self):
        pass
