from . import ChasingWorld
from ..utils import add_common_options, run_script, run_simulation
from .chasing import add_target_options
from optparse import OptionParser
from vehicles import random_checkerboard

def escaping(args):
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
                 target_stabilize_phi=0,
                 world_texture=random_checkerboard(options.world_texture_scale))

    
    def end_condition(simulation):
        if simulation.vehicle_collided:
            return True
        
    id_scenario = 'escaping'
    run_simulation(id_scenario=id_scenario,
                   options=options,
                   world=world,
                   end_condition=end_condition)
    
    return 0

def main():
    run_script(escaping)
    
if __name__ == '__main__':
    main()