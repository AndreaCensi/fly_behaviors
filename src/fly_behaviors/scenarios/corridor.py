from . import CorridorWorld
from ..utils import add_common_options, run_script, run_simulation
from geometry import SE2_from_SE3, translation_angle_from_SE2
from optparse import OptionParser


def corridor_following(args):
    usage = """Corridor following simulation."""
    parser = OptionParser(usage=usage)
    parser.disable_interspersed_args()

    # Scenario -- particular
    parser.add_option("-W", "--corridor_width",
                      dest='corridor_width', default=2, type='float',
                      help="Corridor width in meters [%default].")
    
    parser.add_option("-L", "--corridor_length",
                      dest='corridor_length', default=100, type='float',
                      help="Corridor length in meters [%default].")

    add_common_options(parser)
    
    (options, args) = parser.parse_args()
    
    if args:
        raise Exception('Trailing arguments (%r)' % args)

    corridor_width = options.corridor_width
    corridor_length = options.corridor_length
    end_line = corridor_length * 0.9
    world = CorridorWorld(corridor_width, corridor_length)
    
    def end_condition(simulation):
        if simulation.vehicle_collided:
            return True
        pose = simulation.vehicle.get_pose()
        t, theta = translation_angle_from_SE2(SE2_from_SE3(pose)) #@UnusedVariable
        y = t[1]
        if y > end_line:
            return True
        
    id_scenario = 'corridor'
    run_simulation(id_scenario=id_scenario,
                   options=options,
                   world=world,
                   end_condition=end_condition)
    
    return 0

def main():
    run_script(corridor_following)
    
if __name__ == '__main__':
    main()
