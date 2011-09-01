from . import CorridorWorld
from geometry import SE2_from_SE3, translation_angle_from_SE2

from . import Task

class CorridorFollowing(Task):
    
    def __init__(self,
                 corridor_width=2,
                 corridor_length=100):
        self.corridor_width = corridor_width
        self.corridor_length = corridor_length
        
        self.world = CorridorWorld(corridor_width, corridor_length)

        
    def end_condition(self, simulation):
        end_line = self.corridor_length * 0.9
        
        if simulation.vehicle_collided:
            return True
        pose = simulation.vehicle.get_pose()
        t, theta = translation_angle_from_SE2(SE2_from_SE3(pose)) #@UnusedVariable
        y = t[1]
        if y > end_line:
            return True

        return False
    
    def get_world(self):
        return self.world
    
