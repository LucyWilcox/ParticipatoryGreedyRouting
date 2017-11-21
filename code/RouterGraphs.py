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
	for k, v in data.items():
		v_0 = v[0]
		v_0_z = [sum(x) for x in zip(*v_0)]
		v_1 = v[1]
		v_1_z = [sum(x) for x in zip(*v_1)]
		v_2 = v[2]
		v_2_z = [sum(x) for x in zip(*v_2)]
		v_3 = v[3]
		v_3_z = [sum(x) for x in zip(*v_3)]
		
		x_axis = range(len(v_0_z))
		all_r = plt.plot(x_axis, v_0_z, 's', label="all routers")
		conn_r = plt.plot(x_axis, v_1_z, 's', label="all connected routers")
		disconn_r = plt.plot(x_axis, v_2_z, 's', label='all disconneced routers')
		plt.ylabel("Num Routers")
		plt.xlabel("Steps")
		plt.title("Connected and Disconnected Routers per Step")
		plt.legend(loc='upper left')
		plt.tight_layout()
		plt.show()
		# plt.savefig("numrouters")
		plt.plot(x_axis, v_3_z, 's')
		plt.ylabel("Num Spaces")
		plt.xlabel("Steps")
		plt.title("Connected Spaces per Step")
		plt.tight_layout()
		# plt.savefig("numspaces")
		plt.show()
