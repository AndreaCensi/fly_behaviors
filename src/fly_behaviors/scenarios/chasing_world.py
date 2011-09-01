from contracts import contract
from geometry import (SE2, SE2_from_SE3, translation_angle_from_SE2,
    SE2_from_xytheta, SE3_from_SE2, normalize_pi_scalar, translation_from_SE2)
from vehicles import (instance_dynamics, random_checkerboard, box, Circle, World,
    isodate, constant_texture)
import numpy as np
 

class ChasingWorld(World):
    ''' A simple example of a dynamic world. '''
    
    @contract(width='>0', length='>0')
    def __init__(self, width=100, length=100,
                 target_speed=0.1,
                 target_color=0,
                 target_radius=0.05,
                 target_start_distance=1,
                 target_id_dynamics='d_SE2_fwd_v',
                 target_stabilize_phi= -np.pi,
                 world_texture=random_checkerboard(0.5)):
        self.width = width
        self.target_stabilize_phi = target_stabilize_phi
        self.length = length
        self.target_dynamics = instance_dynamics(target_id_dynamics)
        self.target_speed = target_speed
        self.target_radius = target_radius
        self.target_start_distance = target_start_distance
        
        r = 1
        bounds = [[-width * r, +width * r],
                  [-length * r, +length * r],
                  [0, 5]]
        World.__init__(self, bounds)

        self.box = box(0, world_texture, width, length)
        self.target = Circle(id_object=1, tags=[],
                             texture=constant_texture(target_color),
                             center=[0, 0],
                             radius=target_radius,
                             solid=True)
        
    def get_primitives(self):
        return [self.box, self.target]
    
    def update_primitives(self):
        target_pose = self.get_target_pose()
        self.target.set_center(translation_from_SE2(target_pose))
    
    @contract(returns='SE2')
    def get_target_pose(self):
        ''' Returns the current pose of the target 
            (according to self.target_state). '''
        pose_se3 = self.target_dynamics.joint_state(self.target_state, 0)[0]
        return SE2_from_SE3(pose_se3)
    
    def new_episode(self):
        vehicle_pose = SE3_from_SE2(SE2_from_xytheta([0, 0, np.pi / 2]))
        target_pose = SE2_from_xytheta([self.target_start_distance,
                                        self.target_start_distance,
                                             np.pi / 2])
        self.target_state = self.target_dynamics.pose2state(SE3_from_SE2(target_pose))
        self.update_primitives()
        id_episode = isodate()
        return World.Episode(id_episode, vehicle_pose)
    
    def simulate(self, dt, vehicle):
        vehicle_pose = SE2_from_SE3(vehicle.get_pose())
        target_pose = self.get_target_pose()
        relative_pose = SE2.multiply(SE2.inverse(target_pose), vehicle_pose)
        t, theta = translation_angle_from_SE2(relative_pose) #@UnusedVariable
        # position on field of view
        phi = np.arctan2(t[1], t[0])
        diff = normalize_pi_scalar(self.target_stabilize_phi - phi)
        # torque command
        command = -np.sign(diff)
        commands = [command]
        self.target_state = self.target_dynamics.integrate(self.target_state,
                                                          commands, dt)
        self.update_primitives()
        return [self.target]
 
