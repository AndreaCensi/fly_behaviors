from contracts import contract
from geometry import SE2_from_xytheta, SE3_from_SE2
from vehicles import PolyLine, World, isodate, random_checkerboard
import numpy as np

class CorridorWorld(World):
    ''' A simple box. '''
    
    @contract(width='>0', length='>0')
    def __init__(self, width=2, length=100,
                 texture_L=None, texture_R=None):
        
        if texture_L is None:
            texture_L = random_checkerboard(0.5)
        if texture_R is None:
            texture_R = random_checkerboard(0.5)
            
        L = width / 2.0
        
        bounds = [[-L, +L], [0, length], [0, 5]]
        World.__init__(self, bounds) 
        
        points_L = [ [-L, 0], [-L, length]]
        points_R = [ [+L, 0], [+L, length]]
        self.wall_L = PolyLine(id_object=0, tags=[],
                               texture=texture_L, points=points_L)
        self.wall_R = PolyLine(id_object=1, tags=[],
                               texture=texture_R, points=points_R)
        # FIXME: bug; if id_object is the same, this is ignored
        
    def get_primitives(self):
        return [self.wall_L, self.wall_R]
    
    def simulate(self, dt, vehicle_pose):
        # no primitives changed
        return []
    
    def new_episode(self):
        ''' 
            Returns an episode tuple. By default it just
            samples a random pose for the robot.
        ''' 
        vehicle_state = SE3_from_SE2(SE2_from_xytheta([0, 0, np.pi / 2]))
        id_episode = isodate()
        return World.Episode(id_episode, vehicle_state)

