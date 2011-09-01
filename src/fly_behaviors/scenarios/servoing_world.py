from contracts import contract
from geometry import SE2_from_xytheta, SE3_from_SE2
from vehicles import World, isodate, random_checkerboard, Circle

class ServoingWorld(World):
    ''' World used for servoing.
    
        Geometry consists of a circle at a given radius, with
        random checkerboard of given scale.
    
    '''
    
    @contract(radius='>0', texture_scale='>0')
    def __init__(self, radius=1, texture_scale=0.1):
        
        texture = random_checkerboard(texture_scale)
        
        R = radius
        bounds = [[-R, +R], [-R, R], [0, 5]]
        World.__init__(self, bounds) 
        
        self.circle = Circle(id_object=0, tags=[],
                               texture=texture, center=[0, 0], radius=R)

    def get_primitives(self):
        return [self.circle]
    
    def simulate(self, dt, vehicle_pose):
        # no primitives changed
        return []
    
    def new_episode(self):
        vehicle_state = SE3_from_SE2(SE2_from_xytheta([0, 0, 0]))
        id_episode = isodate()
        return World.Episode(id_episode, vehicle_state)

