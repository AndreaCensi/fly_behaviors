from . import ManagerConfig, logger, run
from ..utils import run_script
from optparse import OptionParser
from pkg_resources import resource_filename #@UnresolvedImport
from vehicles import VehiclesConfig, load_vehicles_config
import contracts
import itertools
import os

def manager(args):
    configs_dir = resource_filename("fly_behaviors", "configs")
        
    usage = """"""
    parser = OptionParser(usage=usage)
    parser.disable_interspersed_args()

    parser.add_option("-c", dest='configs_dir', default=configs_dir,
                      help="Directory containing configuration [%default].")

    parser.add_option("-l", dest='log_directory', default='behaviors-sims',
                      help="Where to save logs [%default].")

    parser.add_option("--dt",
                      dest='dt', default=0.05, type='float',
                      help="Simulation interval (s) [%default].")

    parser.add_option("-T", default=100, type='float',
                      help="Maximum simulation time (s) [%default].")

    parser.add_option("--fast", default=False, action='store_true',
                      help="Disables contracts checking [%default].")

    parser.add_option("--num_episodes", default=1,
                      help="Number of episodes to run for each combination.")

    parser.add_option("--video", default=False, action='store_true',
                      help="Creates videos [%default].")

    (options, args) = parser.parse_args()

    if options.fast:
        contracts.disable_all()
    
    print options
        
    logger.info('Loading standard PyVehicles configuration.')
    load_vehicles_config()
    logger.info('Loading our additional PyVehicles configuration.')
    load_vehicles_config(options.configs_dir)
    logger.info('Loading our configuration (tasks, controllers, combinations).')
    manager_config = ManagerConfig(options.configs_dir)
    
    all_combinations = manager_config.combinations.keys()
    
    if args:
        use = args
    else:
        use = all_combinations
  
    logger.info('Using combinations %s' % use)

    for x in use:
        if not x in all_combinations:
            raise ValueError('No known combination %r.' % x)
        run_combinations(manager_config=manager_config,
                         comb_id=x,
                         other_options=options)

def run_combinations(manager_config, comb_id, other_options):
    comb = manager_config.combinations[comb_id]
    out = os.path.join(other_options.log_directory, comb_id)
    out = os.path.realpath(out)
    logger.info('Target directory %r' % out)
    for task_id, vehicle_id, agent_id in \
        itertools.product(comb['tasks'], comb['vehicles'], comb['agents']):
        task = manager_config.tasks[task_id]
        vehicle = VehiclesConfig.vehicles[vehicle_id]
        agent = manager_config.controllers[agent_id]

        base = '%s-%s-%s' % (task_id, vehicle_id, agent_id)
        for i in range(other_options.num_episodes):
            target = os.path.join(out, base, '%s-%04d.vlog.yaml' % (base, i))
            run(task=task, vehicle=vehicle, agent=agent, log=target,
                other_options=other_options)
            
            if other_options.video:
                for pg_model in comb['visualizations']:
                    create_visualization(target, pg_model) 
        
def create_visualization(log, pg_model):
    out = log + '-%s.avi' % pg_model
    if os.path.exists(out):
        logger.info('Skipping because %r already exists.' % out)
        return
    from procgraph import pg
    import procgraph_vehicles #@UnusedImport
    import fly_behaviors.visualization #@UnusedImport
    config = {'file': log, 'output': out}
    pg(pg_model, config=config)

def main():
    run_script(manager)
    
if __name__ == '__main__':
    main()

    
