from . import ChasingWorld
from ..utils import add_common_options, run_script, run_simulation
from optparse import OptionParser
from vehicles import random_checkerboard
import numpy as np

def add_target_options(parser):
    parser.add_option("-R", "--world_radius", default=100, type='float',
                      help="Size of the world [%default].")

    parser.add_option("--target_id_dynamics", default='d_SE2_fwd_v',
                      help="Dynamics of the target [%default].")

    parser.add_option("--target_start_distance", default=1, type='float',
                      help="Initial distance of the target [%default].")

    parser.add_option("--target_color", default=0, type='float',
                      help="Color of the target (0-1 luminance value).")
    
    parser.add_option("--target_radius", default=0.05, type='float',
                      help="Size of the target")

    parser.add_option("--world_texture_scale", default=0.5, type='float',
                      help="Scale of the random world texture.")


def chasing(args):
    usage = """Chasing simulation."""
    parser = OptionParser(usage=usage)
    parser.disable_interspersed_args()

    add_target_options(parser)

    add_common_options(parser)
    
    (options, args) = parser.parse_args()
    
    if args:
        raise Exception('Trailing arguments (%r)' % args)

    world = ChasingWorld(width=options.world_radius,
                 target_color=options.target_color,
                 target_radius=options.target_radius,
                 target_start_distance=options.target_start_distance,
                 target_id_dynamics=options.target_id_dynamics,
                 target_stabilize_phi= -np.pi,
                 world_texture=random_checkerboard(options.world_texture_scale))

    
    def end_condition(simulation):
        if simulation.vehicle_collided:
            return True
        
    id_scenario = 'chasing'
    run_simulation(id_scenario=id_scenario,
                   options=options,
                   world=world,
                   end_condition=end_condition)
    
    return 0

def main():
    run_script(chasing)
    
if __name__ == '__main__':
    main()
