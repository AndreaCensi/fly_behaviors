from .. import logger
from vehicles import (check_generic_code_desc, check_necessary,
    load_configuration_entries)


class ManagerConfig:
    def __init__(self, config_dir):
        self.tasks = load_configuration_entries(config_dir, '*.tasks.yaml',
                    check_entry=lambda x: check_generic_code_desc(x, 'task'))
    
        self.controllers = load_configuration_entries(config_dir, '*.controllers.yaml',
                    check_entry=lambda x: check_generic_code_desc(x, 'controller'))
        
        self.combinations = load_configuration_entries(config_dir, '*.combinations.yaml',
                    check_entry=check_combination)
        
        logger.info('Loaded %d tasks (%s)' % 
                    (len(self.tasks), self.tasks.keys()))
        logger.info('Loaded %d controllers (%s)' % 
                    (len(self.controllers), self.controllers.keys()))
        logger.info('Loaded %d combinations (%s)' % 
                    (len(self.combinations), self.combinations.keys()))

def check_combination(x):    
    necessary = [ 
                 ('id', str),
                  ('agents', list),
                  ('vehicles', list),
                  ('tasks', list),
                  ]
    check_necessary(x, necessary)

