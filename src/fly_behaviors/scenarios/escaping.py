from . import ChasingWorld, Task
from vehicles import random_checkerboard

class Escaping(Task):
    
    def __init__(self,
                 world_radius=100,
                 target_id_dynamics='d_SE2_fwd_v',
                 target_start_distance=1,
                 target_color=0,
                 target_radius=0.05,
                 world_texture_scale=0.5):
        
        self.world = ChasingWorld(width=world_radius,
                 target_color=target_color,
                 target_radius=target_radius,
                 target_start_distance=target_start_distance,
                 target_id_dynamics=target_id_dynamics,
                 target_stabilize_phi=0,
                 world_texture=random_checkerboard(world_texture_scale))

    def end_condition(self, simulation):
        if simulation.vehicle_collided:
            return True
        
        
    def get_world(self):
        return self.world
    
