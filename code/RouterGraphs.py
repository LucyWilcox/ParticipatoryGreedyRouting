import matplotlib.pyplot as plt
import matplotlib
import plotly.graph_objs as go

matplotlib.rc('ytick', labelsize = 12)
matplotlib.rc('xtick', labelsize = 12)
matplotlib.rc('axes', titlesize = 16, labelsize = 14)
# colors from our friends at http://colorbrewer2.org
COLORS = ['#8dd3c7','#ffffb3','#bebada','#fb8072','#80b1d3','#fdb462',
          '#b3de69','#fccde5','#d9d9d9','#bc80bd','#ccebc5','#ffed6f']

def graph_routers(data):
	# print(data)
	for k, v in data.items():
		x_axis = range(len(v[0]))
		all_r = plt.plot(x_axis, v[0], 's', label="all routers")
		conn_r = plt.plot(x_axis, v[1], 's', label="all connected routers")
		disconn_r = plt.plot(x_axis, v[2], 's', label='all disconneced routers')
		plt.ylabel("Num Routers")
		plt.xlabel("Steps")
		plt.title("Connected and Disconnected Routers per Step")
		plt.legend(loc='upper left')
		plt.show()
		plt.plot(x_axis, v[3], 's')
		plt.ylabel("Num Spaces")
		plt.xlabel("Steps")
		plt.title("Connected Spaces per Step")
		plt.show()
