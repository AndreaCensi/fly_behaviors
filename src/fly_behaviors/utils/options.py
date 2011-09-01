#from vehicles import instance_vehicle
#from ..config import instance_controller
#
#def add_common_options(parser):
#    # Simulation
##    parser.add_option("-c", dest='conf_directory',
##                      help="Configuration directory [%default].")
#    
#    parser.add_option("-l", dest='log_directory', default='.',
#                      help="Where to save logs [%default].")
#
#    parser.add_option("--dt",
#                      dest='dt', default=0.05, type='float',
#                      help="Simulation interval (s) [%default].")
#
#    # Scenario -- common
#    parser.add_option("-r", "--vehicle",
#                      dest='id_vehicle', default='v_fly_kin_360',
#                      help="Vehicle ID [%default].")
#    
#    parser.add_option("-c", "--controller",
#                      dest='id_controller', default='random_controller',
#                      help="Controller ID [%default].")
#
#    parser.add_option("--fast", default=False, action='store_true',
#                      help="Disables contracts checking [%default].")
#
#def instance_vehicle_from_options(options):
#    id_vehicle = options.id_vehicle    
#    return instance_vehicle(id_vehicle)
#    
#def instance_controller_from_options(options):
#    id_controller = options.id_controller
#    return instance_controller(id_controller)
