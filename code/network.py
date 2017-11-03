import numpy as np
import math
import itertools
import scipy
from decimal import Decimal

class Network:
	def __init__(self, n, T, k, y):
		self.n = n
		self.T = T
		self.k = k
		self.y = y
		self.nodes = []

		self.k_min = k*((y-2)/(y-1))
		probs = []
		for i in range(1, 5000):
			# print (y-1), (self.k_min**(y-1)), (i**(-y))
			# incomplete_gamma = special.gammainc(i + 1 - y, self.k_min)
			probs.append((y-1)*(self.k_min**(y-1))*(i**(-y)))
			# probs.append((y-1)*(self.k_min**(y-1))*incomplete_gamma)
		probs = np.array(probs)
		self.range = range(1, 5000)
		probs /= probs.sum()
		self.probs = probs

	def create_nodes(self):
		for i in range(self.n):
			theta = np.random.uniform(0, 2*math.pi)
			degree = np.random.choice(range(1, 5000), p=self.probs)
			self.nodes.append(Node(degree, theta))

	def connect_nodes(self):
		for n1, n2 in itertools.combinations(self.nodes, 2):
			diff_t = abs(math.pi - abs(math.pi - abs(n1.theta - n2.theta)))
			angular_distance = (self.n/(2*math.pi))*diff_t
			u = math.sin(self.T*math.pi)/(2*self.k*self.T*math.pi)
			# I added the / 10, seems to have better results:
			prob = (1/(1+((angular_distance/(u*n1.degree*n2.degree))**(1/self.T))/10))
			if np.random.choice([True, False],p=[prob,1-prob]):
				n1.add_edge(n2)
				n2.add_edge(n1)

	def nodes_to_h2(self):
		f = (((self.y - 2)/(self.y - 1))**2)
		c = self.k*(math.sin(self.T*math.pi)/(2*self.T))* f
		self.R = 2*math.log(self.n/c)
		for n in self.nodes:
			r = self.R - (2*math.log(n.degree/self.k_min))
			n.add_radial(r)

class Node:
	def __init__(self, degree, theta):
		self.degree = degree
		self.theta = theta
		self.neighbors = []
		self.strat = None
		self.points = 0

	def add_edge(self, n2):
		self.neighbors.append(n2)

	def add_radial(self, r):
		self.r = r

	def set_strat(self, strat):
		self.strat = strat

def initialize(c):
	network = Network(500, 0.4, 6, 2.5) #from paper 10000, 0.4, 6, 2.5
	network.create_nodes()
	network.nodes_to_h2()
	network.connect_nodes()

	for n in network.nodes:
		n.set_strat(np.random.choice(['C', 'D'],p=[c,1-c]))

	return network


def path(i, j):
	participants = [i]
	while j not in participants:
		min_j_v = float('inf')
		min_j = None
		for j_n in i.neighbors:
			diff_t = math.pi - abs(math.pi - abs(i.theta - j_n.theta))
			x_ij = math.acosh(math.cosh(i.r)*math.cosh(j_n.r) - math.sinh(i.r)*math.sinh(j_n.r)*math.cos(diff_t))
			if x_ij < min_j:
				min_j_v = x_ij
				min_j = j_n
		if j_n in participants:
			return []
		elif j_n.strat is 'D':
			return []
		else:
			j_n.points -= 1
			participants.append(j_n)

	return participants

def navigation(network, b):
	ns = [n for n in network.nodes if len(n.neighbors) > 0]
	for _ in range(len(ns)):
		i, j = np.random.choice(ns, 2)
		participants = path(i, j)
		if participants:
			reward = float(b)/len(participants)
			for p in participants:
				p.points += reward

	return network

def update(network):
	ns = [n for n in network.nodes if len(n.neighbors) > 0]
	for n in ns:
		neighbor = np.random.choice(n.neighbors)
		diff = neighbor.points - n.points
		if diff > 650: # this is because otherwise you get overflows even using Decimal
			diff = 650
		elif diff < -650:
			diff = -650
		ediff = Decimal(math.e**(-diff))
		prob = Decimal(1) / Decimal(1 + ediff)
		strat = np.random.choice([neighbor.strat, n.strat], p=[prob, 1-prob])
		n.set_strat(strat)

def run(c, b):
	network = initialize(c)

	#just to see over time:
	for _ in range(1000):
		navigation(network, b)
		update(network)
		c = 0
		d = 0
		for n in network.nodes:
			if n.neighbors:
				if n.strat == 'C':
					c += 1
				if n.strat == 'D':
					d += 1
		print c, d


# run(.7, 4000) # seems to edge up a bit with this but barely...
run(.4, 2) # doesn't really go down..

