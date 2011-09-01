from . import ServoingWorld, Task
from geometry import SE2_from_SE3, translation_angle_from_SE2
import numpy as np


class Servoing(Task):
    
    def __init__(self,
                 failure_radius=4,
                 max_sim_time=10,
                 environment_scale=0.5,
                 environment_radius=5):
        self.failure_radius = failure_radius
        self.max_sim_time = max_sim_time 

        self.world = ServoingWorld(radius=environment_radius, texture_scale=environment_scale)
        
    def end_condition(self, simulation):
        if simulation.vehicle_collided:
            return True
        if simulation.timestamp > self.max_sim_time:
            return True
        pose = simulation.vehicle.get_pose()
        t, theta = translation_angle_from_SE2(SE2_from_SE3(pose)) #@UnusedVariable
        d = np.linalg.norm(t)
        if d > self.failure_radius:
            return True
             
    def get_world(self):
        return self.world
    
#    parser.add_option("-s", "--environment_scale",
#                      dest='environment_scale', default=1, type='float',
#                      help="Scale of environment features. [%default].")
#
#    parser.add_option("-T", "--max_sim_time",
#                      dest='max_sim_time', default=5, type='float',
#                      help="Maximum simulation time. [%default].")
#
#    parser.add_option("-f", "--failure_radius",
#                      dest='failure_radius', default=5, type='float',
#                      help="Threshold for considering a run a failure. [%default].")
#    
