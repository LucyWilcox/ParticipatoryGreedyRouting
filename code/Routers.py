import numpy as np
import networkx as nx
import CityViewer
from scipy.signal import correlate2d
import operator
import copy
import collections
import RouterGraphs

class RouterBase(object):

    def __init__(self, graph, array, loc, range_access, friendliness, multi_connect = False):
        """ Inputs:
        graph - networkx graph to add itself to
        array - the np array represting the city map
        loc - tuple of locations on grid
        range_access - range of wifi
        friendliness - integer that represents
            their willingness to accept connections
        """
        self.graph = graph
        self.graph.add_node(self)
        self.array = array
        self.n, _ = array.shape
        self.loc = loc
        self.range_access = range_access
        self.friendliness = friendliness
        self.multi_connect = multi_connect
        self.latency = 0
        self.connected_routers = []
        self.has_wifi = False

    def accept_connection(self):
        """ Checks to see if the Router
        is willing to accept another connection
        returns: boolean
        """
        if self.latency >= self.friendliness: 
            # if the latency is too high, the router will refuse connection
            return False
        else:
            ratio = self.latency/self.friendliness
            try:
                res = np.random.choice([True, False], p = [1-ratio, ratio])# chance of accept goes down as latency goes up
            except ValueError:
                res = False
            return res

    def add_connection(self, other_router, city):
        """ Adds the connection and makes sure all relevent lists are
        updated.
        inputs:
        other_router-the router to which this router connects
        city-instance of the city that keeps track of everything else.
        """
        
        # Increase latency of self and the other router (simple model)
        if isinstance(other_router, PersonalRouter):
            other_router.latency += 1
            self.graph.add_edge(other_router, self)
        else:
            self.graph.add_edge(other_router, self)
        self.latency = other_router.latency + 1

        # Check to see which thing needs to be updated
        if not self.has_wifi and other_router.has_wifi:
            self.has_wifi = True
            try: city.no_wifi_routers.remove(self)
            except ValueError: pass
            city.has_wifi_routers.append(self)

        elif self.has_wifi and not other_router.has_wifi:
            other_router.has_wifi = True
            city.no_wifi_routers.remove(other_router)
            city.has_wifi_routers.append(other_router)

    def try_connection(self, other_router, city):
        """ Attempts to connect the two. """
        if other_router.accept_connection():
            return self.add_connection(other_router, city)

    def wifi_range(self):
        """ Returns tuples of all the areas for which it effects
        
        returns: tuple, coordinates of best cell
        """
        # find all visible cells
        locs = make_visible_locs(self.array, self.loc, self.range_access)
        
        # convert rows of the array to tuples
        locs = [tuple(loca) for loca in locs]
        return locs

    def search_for_connection(self, city):
        """ Looks around and tries to connect to wifi 
        input:
        city-instance of city class that controls everything else
        """

        # Scans visible area and checks to see if something is there
        #  It will try to connect to SuperRouters first
        search_spaces = self.wifi_range()
        for space in search_spaces:
            if space in city.occupied:
                other_router = city.search_for_loc(space, city.super_routers) # checks if it is a Super
                try:
                    # tries to connect if it is
                    self.try_connection(other_router, city)
                    break # Stops looking if it connects
                except AttributeError:
                    pass
        if not self.has_wifi:
            for space in search_spaces:
                if space in city.occupied: # otherwise, tries to connect to normal routers
                    other_router = city.search_for_loc(space, city.has_wifi_routers)
                    try:
                        if other_router.has_wifi:
                            self.try_connection(other_router, city)
                            if not self.multi_connect:
                                break
                    except AttributeError:
                        pass

    def get_num_children_split(self, seen = set()):
        successors = list(self.graph.successors(self))
        if len(successors) is 0:
            return 1/len(list(self.graph.predecessors(self)))
        else:
            total = 0
            for s in successors:
                if s not in seen:
                    seen.add(s)
                    total += 1 + s.get_num_children_split(seen)/len(list(self.graph.predecessors(s)))
            return total

    def update_latency(self):
    # updates latency so that it is correlated with the average of it's parents latency 
        successors = list(self.graph.successors(self)) #successors of SR
        queue = collections.deque()
        seen = set()
        queue.extend(successors)

        while queue:
            s = queue.popleft()
            successors = list(self.graph.successors(s))
            parents = list(self.graph.predecessors(s))
            if s not in seen:
                parent_latency_split = sum([p.latency for p in parents]) / len(parents)
                s.latency = parent_latency_split + s.get_num_children_split()
                queue.extend(successors)
                seen.add(s)

class SuperRouter(RouterBase):
    """ Creates a Router that has a range of 20
    and will always accept connections """

    def __init__(self, graph, array, loc, multi_connect = False):
        """ Starts up as a normal router, but with a large range,
        lots of friendliness, and wifi
        """
        RouterBase.__init__(self, graph, array, loc, 10, 1000, multi_connect)
        self.has_wifi = True

    def accept_connection(self):
        """ SuperRouter will always accept """
        return True

    def try_connection(self, other_router, city):
        """ Always accepts, always adds the other router """
        self.add_connection(other_router, city)

    def search_for_connection(self, city):
        """ Searches for any non-connected router in range and connects """
        search_spaces = self.wifi_range()
        for space in search_spaces:
            if space in city.occupied:
                other_router = city.search_for_loc(space, city.no_wifi_routers)
                if isinstance(other_router, PersonalRouter):
                    # Does not add other super routers, but will add normal
                    if not other_router.has_wifi:
                        self.add_connection(other_router, city)

class PersonalRouter(RouterBase):

    def __init__(self, graph, array, loc, multi_connect = False):
        friendliness = np.random.randint(5, 15) # TODO: Lucy's going to test this with some different values
        range_access = 5
        RouterBase.__init__(self, graph, array, loc, range_access, friendliness, multi_connect)
        self.has_wifi = False

    def stop_sharing(self, city):
        neighbors = list(self.graph.neighbors(self))
        num_disconnected = 0
        # remove wifi from routers and they check for new connections in the next part of step
        for neighbor in neighbors:
            try:
                num_disconnected += neighbor.disconnect(self, city)
            except Exception as e:
                pass

        self.friendliness = 1
        self.latency -= num_disconnected

    def disconnect(self, other_router, city):
        """ Disconnects self and all routers connected
        to self. Returns the number of routers disconnected.
        """
        self.graph.remove_edge(other_router, self)
        no_connection = True
        for parent in self.predecessors:
            if parent.has_wifi:
                no_connection = False
                break
        if no_connection:
            self.latency = 0
            disconnected = 1
            city.has_wifi_routers.remove(self)
            city.no_wifi_routers.append(self)
            for neighbor in self.graph.neighbors(self):
                try:
                    disconnected += neighbor.disconnect(self, city)
                except Exception as e:
                    pass
        return disconnected


class City(object):

    def __init__(self, n, multi_connect = False, **params):
        """Initializes the attributes.

        n: number of rows
        m: number of columns
        num_super_routers: desired number of super routers
        params: dictionary of parameters
        """
        self.n = n
        self.graph = nx.DiGraph()
        self.array = np.zeros((n,n))
        self.params = params
        self.no_wifi_routers = []
        self.has_wifi_routers = []
        self.occupied = set()
        self.super_routers_loc = []
        self.multi_connect = multi_connect

        self.place_super_routers()
        num_routers = self.params.get('num_routers', self.n//5)
        self.num_routers_per_step = self.params.get('num_routers_per_step', self.n//10)
        for _ in range(num_routers):
            self.place_router()


    def place_super_routers(self):
        """ Place either the specified number of routers, or 5 """
        n, m = self.params.get('starting_box', self.array.shape)

        # Make a list of all potential locations, then choose randomly
        locs = make_locs(n, m)
        np.random.shuffle(locs)
        num_super_routers = self.params.get('num_super_routers', 5)

        # Place super routers at those places
        self.super_routers = [SuperRouter(self.graph, self.array, tuple(locs[i])) 
                       for i in range(num_super_routers)]

        # For each super router, add it and its range
        for router in self.super_routers:
            self.occupied.add(router.loc)
            self.super_routers_loc.append(router.loc)

    def place_router(self):
        new_router = PersonalRouter(self.graph, self.array, self.random_loc(), self.multi_connect)
        new_router.search_for_connection(self)
        if new_router.has_wifi:
            pass
        else:
            self.no_wifi_routers.append(new_router)
        self.occupied.add(new_router.loc)

    def random_loc(self):
        """Choose a random unoccupied cell.
        
        returns: tuple coordinates
        """
        while True:
            loc = tuple(np.random.randint(self.n, size=2))
            if loc not in self.occupied:
                return loc

    def step(self):
        """ Goes through all the routers and tries to connect them
        to wifi. """
        for super_router in self.super_routers:
            super_router.search_for_connection(self)

        for router in self.has_wifi_routers:
            if router.latency >= router.friendliness and len(list(self.graph.successors(router))) > 0:
                router.stop_sharing(self)

        random_order = np.random.permutation(self.no_wifi_routers)
        for router in random_order:            
            # execute one step
            router.search_for_connection(self)

        for _ in range(self.num_routers_per_step):
            self.place_router()

        for super_router in self.super_routers:
            super_router.update_latency()

        return len(self.has_wifi_routers)/(len(self.has_wifi_routers) + len(self.no_wifi_routers))

    def search_for_super(self, loc):
        """ Searches through all connected routers for one
        that has connection at that location. """
        for router in self.super_routers:
            if router.loc == loc:
                return router
        return None

    def search_for_loc(self, loc, router_list):
        """ Searches through all connected routers for one
        that has connection at that location.
        loc: tuple of location
        router_list: list of routers to search
        """
        for router in router_list:
            if router.loc == loc:
                return router
        return None

def make_locs(n, m):
    """Makes array where each row is an index in an `n` by `m` grid.
    
    n: int number of rows
    m: int number of cols
    
    returns: NumPy array
    """
    left = np.repeat(np.arange(m), n)
    right = np.tile(np.arange(n), m)
    return np.transpose([left, right])

def make_visible_locs(array, loc, vision):
    """Computes the kernel of visible cells.
        
    vision: int distance
    """
    kernel = np.ones((2*vision,2*vision))
    a = np.zeros(array.shape)
    a[loc] = 1
    can_see = correlate2d(a, kernel, mode='same', boundary='fill', fillvalue=0)

    return np.argwhere(can_see > 0)

if __name__ == '__main__':
    cities = []
    for i in range(1):
        cities.append(City(100, num_routers = 15))

    connect = [False, True]
    connect_options = dict.fromkeys(connect)
    for conn in connect_options:
        print(conn)
        num_routers = []
        num_connected = []
        num_disconnected = []
        for city in cities: # test on different cities
            num_routers.append([])
            num_connected.append([])
            num_disconnected.append([])
            city_copy = copy.deepcopy(city)
            city_copy.multi_connect = conn

            for _ in range(200): #steps
                city_copy.step()
                num_routers[-1].append(len(city_copy.occupied))
                num_connected[-1].append(len(city_copy.has_wifi_routers))
                num_disconnected[-1].append(len(city_copy.no_wifi_routers))
                
            viewer = CityViewer.CityViewer(city_copy)
            viewer.draw()
            connect_options[conn] = (num_routers, num_connected, num_disconnected)
    RouterGraphs.graph_routers(connect_options)