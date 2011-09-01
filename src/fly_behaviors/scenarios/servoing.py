from . import ServoingWorld, Task
from geometry import SE2_from_SE3, translation_angle_from_SE2
import numpy as np


class Servoing(Task):
    
    def __init__(self,
                 failure_radius=4,
                 max_sim_time=10,
                 environment_scale=0.5):
        self.failure_radius = failure_radius
        self.max_sim_time = max_sim_time 

        self.world = ServoingWorld(environment_scale)
        
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
    
#    
#def servoing(args):
#    usage = """Simulation of servoing task."""
#    parser = OptionParser(usage=usage)
#    parser.disable_interspersed_args()
#
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
#    add_common_options(parser)
#    
#    (options, args) = parser.parse_args()
#    
#    if args:
#        raise Exception('Trailing arguments (%r)' % args)
# 
#    world = ServoingWorld(options.environment_scale)
#    
#    def end_condition(simulation):
#        if simulation.vehicle_collided:
#            return True
#        pose = simulation.vehicle.get_pose()
#        t, theta = translation_angle_from_SE2(SE2_from_SE3(pose)) #@UnusedVariable
#        d = np.linalg.norm(t)
#        if d > options.failure_radius:
#            return True
#        
#    id_scenario = 'servoing'
#    run_simulation(id_scenario=id_scenario,
#                   options=options,
#                   world=world,
#                   end_condition=end_condition)
#    
#    return 0
#
#def main():
#    run_script(servoing)
#    
#if __name__ == '__main__':
#    main()
