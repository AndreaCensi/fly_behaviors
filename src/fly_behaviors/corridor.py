from . import logger
from . import CorridorWorld
from geometry import SE2_from_SE3, translation_angle_from_SE2
from optparse import OptionParser
from vehicles.configuration.instance_all import instance_vehicle
from vehicles.interfaces.world import isodate
from vehicles.simulation.simulation import VehicleSimulation
import numpy as np
import sys
import traceback
import yaml
import os
from geometry.manifolds import SE2

class RandomFlyController:
    def get_angular_velocity(self, directions, luminance):
        return (np.random.rand() - 0.5) * 2

def corridor_following(args):
    usage = """ """
    parser = OptionParser(usage=usage)
    parser.disable_interspersed_args()
    parser.add_option("-c", dest='conf_directory',
                      help="Configuration directory [%default].")
    parser.add_option("-l", dest='log_directory',
                      default="~/.ros/log",
                      help="Log directory [%default].") 
    (options, args) = parser.parse_args()
    
    if args:
        raise Exception('Trailing arguments (%r)' % args)

    id_vehicle = 'v_fly_kin_360'
    vehicle = instance_vehicle(id_vehicle)
    corridor_width = 2
    corridor_length = 50
    end_line = corridor_length * 0.9
    world = CorridorWorld(corridor_width, corridor_length)
    simulation = VehicleSimulation(vehicle, world)
    dt = 0.05
    
    id_controller = 'random'
    controller = RandomFlyController()
    
    log = 'corridor-%s-%s-%s.yaml' % (id_vehicle, id_controller, isodate())
    last = 'last.yaml'
    if os.path.exists(last):
        os.unlink(last)
    os.symlink(log, last)
    logfile = open(log, 'w')
    
    logger.info('Writing on log %r.' % log)
    logger.info(' (also accessible as %r)' % last)
    
    def end_condition(simulation):
        if simulation.vehicle_collided:
            return True
        pose = simulation.vehicle.get_pose()
        t, theta = translation_angle_from_SE2(SE2_from_SE3(pose)) #@UnusedVariable
        y = t[1]
        if y > end_line:
            return True
        
    run_simulation(simulation=simulation,
                   controller=controller,
                   logfile=logfile,
                   dt=dt,
                   end_condition=end_condition)
    
    return 0

def run_simulation(simulation, controller, dt, end_condition, logfile=None):
    simulation.new_episode()
    while True:
        simulation.compute_observations()
        directions = simulation.vehicle.sensors[0].sensor.directions
        luminance = simulation.vehicle.sensors[0].current_observations['luminance']
        command = controller.get_angular_velocity(directions, luminance)
        commands = [command]
        if logfile is not None:
            y = simulation.to_yaml()
            y['commands'] = commands
            logfile.write('---\n')
            yaml.dump(y, logfile)
            
        logger.info('Timestamp: %.3f  pose: %s' % 
                    (simulation.timestamp,
                    SE2.friendly(SE2_from_SE3(simulation.vehicle.get_pose()))))
        if end_condition(simulation):
            break
        simulation.simulate(commands, dt)
        
def run_script(f):
    try:
        ret = f(sys.argv[1:])
        logger.debug('Graceful exit with return code %d.' % ret)
        sys.exit(ret)
    except Exception as e:
        logger.error(str(e))
        logger.error(traceback.format_exc())
        sys.exit(-2) 

def main():
    run_script(corridor_following)
    
if __name__ == '__main__':
    main()
