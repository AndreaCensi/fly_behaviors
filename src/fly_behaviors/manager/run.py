from . import logger
from ..controllers import Controller, VehicleSpec, VehicleObservations
from ..scenarios import Task
from geometry import SE2, SE2_from_SE3
from vehicles import (VehicleSimulation, instance_vehicle_spec,
    instantiate_spec_and_check)
import os
import yaml

try:
    # Try to load the C bindings
    from yaml import CDumper as Dumper
    
except ImportError:
    from yaml import Dumper
    
def run(task, vehicle, agent, log, other_options):
    if os.path.exists(log):
        logger.info('Skipping as %r already exists.' % log)
        return
    
    task_ob = instantiate_spec_and_check(task['code'], Task)
    agent_ob = instantiate_spec_and_check(agent['code'], Controller)
    vehicle_ob = instance_vehicle_spec(vehicle)
    
    run_simulation(task_ob, vehicle_ob, agent_ob, log,
                   dt=other_options.dt, maxT=other_options.T)
    
def run_simulation(task, vehicle, agent, log, dt, maxT):
        
    world = task.get_world()
    simulation = VehicleSimulation(world=world, vehicle=vehicle)
    directions = simulation.vehicle.sensors[0].sensor.directions
    vehicle_spec = VehicleSpec(directions=directions)
    agent.init(vehicle_spec)
    
    simulation.new_episode() 

    tmp_log = log + '.active'
    ldir = os.path.dirname(log)
    #last = os.path.join(ldir, 'last.yaml')
    logger.info('Writing on log %r.' % log)
    #logger.info(' (also accessible as %r)' % last)
    
    if not os.path.exists(ldir):
        os.makedirs(ldir)
    #if os.path.exists(last):
    #    os.unlink(last)
    
    logfile = open(tmp_log, 'w')
    
    #assert not os.path.exists(last)
    assert os.path.exists(tmp_log)
    #logger.info('Link %s, %s' % (tmp_log, last))
    #os.symlink(tmp_log, last)
    
    
    
    logger.info('Simulation dt=%.3f max T: %.3f' % (dt, maxT))
    while True:
        simulation.compute_observations()
        # TODO: perhaps this needs to be gerealized
        luminance = simulation.vehicle.sensors[0].current_observations['luminance']
        observations = VehicleObservations(time=simulation.timestamp,
                            dt=dt,
                            luminance=luminance)
        agent.process_observations(observations)
        commands = agent.choose_commands()
        # TODO: check format
        if logfile is not None:
            y = simulation.to_yaml()
            y['commands'] = commands.tolist()
            logfile.write('---\n')
            yaml.dump(y, logfile, Dumper=Dumper)
            
        logger.info('t=%.3f  pose: %s' % 
                    (simulation.timestamp,
                    SE2.friendly(SE2_from_SE3(simulation.vehicle.get_pose()))))
        
        if task.end_condition(simulation):
            break
        
        if simulation.timestamp > maxT:
            # TODO: add why we finished
            break
        
        simulation.simulate(commands, dt)

    logfile.close()

    if os.path.exists(log):
        os.unlink(log)
    assert not os.path.exists(log)
    os.rename(tmp_log, log)
    assert not os.path.exists(tmp_log)
    assert os.path.exists(log)

#    if os.path.exists(last):
#        os.unlink(last)
#    assert not os.path.exists(last)
#    assert os.path.exists(log)
#    logger.info('Link %s, %s' % (log, last))
#    os.symlink(log, last)    
