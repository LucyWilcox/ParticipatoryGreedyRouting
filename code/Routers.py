import numpy as np
import networkx as nx
import CityViewer

class RouterBase(object):

	def __init__(self, graph, array, loc, range_access, friendliness):
		""" Inputs:
		graph - networkx graph to add itself to
		loc - tuple of locations on grid
		range - range of wifi
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
		self.latency = 0
		self.connected_routers = []
		self.has_wifi = False

	def accept_connection(self):
		""" Checks to see if the Router
		is willing to accept another connection
		returns: boolean
		"""
		if self.latency >= self.friendliness:
			return False
		ratio = self.latency/self.friendliness
		return np.random.choice([True, False], p = [1-ratio, ratio])

	def add_connection(self, other_router, city):
		""" """
		self.latency += 1
		other_router.latency += 1

		self.graph.add_edge(self, other_router)

		if not self.has_wifi and other_router.has_wifi:
			self.has_wifi = True
		elif self.has_wifi and not other_router.has_wifi:
			other_router.has_wifi = True

		city.no_wifi_routers.remove(self)
		city.has_wifi_routers.append(self)
		for space in self.wifi_range:
			city.has_wifi_spaces.add(space)

	def try_connection(self, other_router, city):
		if other_router.accept_connection:
			self.add_connection(other_router, city)

	def wifi_range(self):
		""" Returns tuples of all the areas for which it effects
		
		returns: tuple, coordinates of best cell
		"""
		# find all visible cells
		locs = make_visible_locs(self.range_access)
		locs = (locs + self.loc) % self.n
		print(locs)
		
		# convert rows of the array to tuples
		locs = [tuple(loca) for loca in locs]
		return locs

	def search_for_connection(self, city):
		""" Looks around and tries to connect to wifi """
		search_spaces = self.wifi_range()
		for space in search_spaces:
			if space in city.occupied:
				other_router = city.search_for_loc(space)
				try:
					if other_router.isinstance(SuperRouter):
						self.try_connection(other_router, city)
						break
				except AttributeError:
					pass

		for space in search_spaces:
			if space in city.occupied:
				other_router = city.search_for_loc(space)
				try:
					if other_router.isinstance(PersonalRouter) and not self.has_wifi:
						self.try_connection(other_router, city)
				except AttributeError:
					pass


class SuperRouter(RouterBase):
	""" Creates a Router that has a range of 20
	and will always accept connections """

	def __init__(self, graph, array, loc):
		RouterBase.__init__(self, graph, array, loc, 20, 1000)
		self.has_wifi = True

	def accept_connection(self):
		""" SuperRouter will always accept """
		return True

class PersonalRouter(RouterBase):

	def __init__(self, graph, array, loc):
		friendliness = np.random.randint(1, 10)
		range_access = 5
		RouterBase.__init__(self, graph, array, loc, range_access, friendliness)

class City(object):

	def __init__(self, n, **params):
		"""Initializes the attributes.

		n: number of rows
		m: number of columns
		num_super_routers: desired number of super routers
		params: dictionary of parameters
		"""
		self.n = n
		self.graph = nx.Graph()
		self.array = np.zeros((n,n))
		self.params = params
		self.no_wifi_routers = []
		#self.has_wifi_routers = []
		self.has_wifi_spaces = set()
		self.occupied = set()
		self.super_routers = []

		self.place_super_routers()
		num_routers = self.params.get('num_routers', self.n//5)
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
		self.has_wifi_routers = [SuperRouter(self.graph, self.array, tuple(locs[i])) 
					   for i in range(num_super_routers)]

		# For each super router, addb it and its range
		for router in self.has_wifi_routers:
			self.occupied.add(router.loc)
			self.super_routers.append(router.loc)
			for loc in router.wifi_range():
				self.array[loc] = 5

	def place_router(self):
		new_router = PersonalRouter(self.graph, self.array, self.random_loc())
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
		random_order = np.random.permutation(self.no_wifi_routers)
		for router in random_order:            
			# execute one step
			router.search_for_connection(self)
		return len(self.has_wifi_routers)/(len(self.has_wifi_routers) + len(self.no_wifi_routers))

	def search_for_loc(self, loc):
		""" Searches through all connected routers for one
		that has connection at that location. """
		for router in self.has_wifi_routers:
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

def make_visible_locs(vision):
	"""Computes the kernel of visible cells.
		
	vision: int distance
	"""
	def make_array(d):
		"""Generates visible cells with increasing distance."""
		a = np.array([[-d, 0], [-d, -d], [-d, d], [d, 0], [d,-d], [d, d], [0, -d], [0, d]])
		#np.random.shuffle(a)
		return a
					 
	arrays = [make_array(d) for d in range(1, vision+1)]
	return np.vstack(arrays)

if __name__ == '__main__':
	city = City(50, num_routers = 5)
	viewer = CityViewer.CityViewer(city)
	viewer.draw()
	# ratios = []
	# for _ in range(20):
	# 	ratios.append(city.step())

	# print(ratios)