from abc import abstractmethod, ABCMeta



class Task:
    __metaclass__ = ABCMeta
     
    @abstractmethod
    def end_condition(self, simulation):
        ''' Return True if the episode can end. '''
        
    @abstractmethod
    def get_world(self):
        ''' Returns an instance of a PyVehicles World '''
    
