from . import (instance_controller_from_options, instance_vehicle_from_options,
    logger)
from geometry import SE2, SE2_from_SE3
from vehicles import VehicleSimulation, isodate
import os
import yaml
import contracts


def run_simulation(id_scenario, options, world, end_condition):
    if options.fast:
        contracts.disable_all()
        
    vehicle = instance_vehicle_from_options(options)
    controller = instance_controller_from_options(options)
    
    dt = options.dt
    
    id_vehicle = options.id_vehicle
    id_controller = options.id_controller
    log_directory = options.log_directory

    basename = '%s-%s-%s-%s.yaml' % (id_scenario, id_vehicle, id_controller, isodate())
    log = os.path.join(log_directory, basename)
    last = os.path.join(log_directory, 'last.yaml')
    if os.path.exists(last):
        os.unlink(last)
    os.symlink(log, last)
    logfile = open(log, 'w')
    
    logger.info('Writing on log %r.' % log)
    logger.info(' (also accessible as %r)' % last)
    
    simulation = VehicleSimulation(world=world, vehicle=vehicle)
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

    logfile.close()
