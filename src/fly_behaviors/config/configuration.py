from . import logger
from ..controllers import Controller
from pprint import pformat
from vehicles import (check_type, instantiate_spec, load_configuration_entries,
    check_generic_code_desc)

class FlyBehaviorsConfig:
    loaded = False
    controllers = {}

def load_flybehaviors_config(directory=None,
                       pattern_controllers='*.controllers.yaml'):
    ''' 
        Loads all configuration files from the directory. 
        If directory is not specified, it uses the default directory. 
    '''
    FlyBehaviorsConfig.loaded = True
    
    if directory is None:
        from pkg_resources import resource_filename #@UnresolvedImport
        directory = resource_filename("fly_behaviors", "configs")
        
    logger.info('Loading configuration from %r' % directory)

    def merge(original, new):
        original.update(new)
    
    controllers = load_configuration_entries(
                        directory,
                        pattern=pattern_controllers,
                check_entry=lambda x: check_generic_code_desc(x, 'controller'))
    merge(FlyBehaviorsConfig.controllers, controllers)

    logger.debug('Found %5d controllers.' % len(FlyBehaviorsConfig.controllers))

# TODO: make generic
def instance_controller(id_controller):
    if not FlyBehaviorsConfig.loaded:
        load_flybehaviors_config()

    if not id_controller in FlyBehaviorsConfig.controllers:
        raise Exception('No controller %r known.' % id_controller)
    entry = FlyBehaviorsConfig.controllers[id_controller]
    return instance_controller_spec(entry)

def instance_controller_spec(entry):
    try:
        instance = instantiate_spec(entry['code'])
        check_type(entry, Controller, instance)
    except:
        logger.error('Error while trying to instantiate world. Entry:\n%s' 
                     % (pformat(entry)))
        raise
    return instance

