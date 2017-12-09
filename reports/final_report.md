# Multi-Connection Support in Mesh Networks

## Kaitlyn Keil and Lucy Wilcox

### Coresponding notebook can be found [here](https://github.com/LucyWilcox/ParticipatoryGreedyRouting/blob/master/code/mesh_notebook2.ipynb)

**Abstract**

Networks are becoming more common, complex, and necessary. One common use is to provide internet access to communities, such as the New York City Mesh. However, the current model, which routes all traffic from any given node through a single connecting node until it reaches the source, is not scalable. Access becomes prohibitively slow until users opt out entirely. We examine a separate model where new routers that connect split their traffic through all available connection points. We found that, despite occasionally causing higher overall latency, this tended to allow more participants to gain wifi access.
_________________________

Mesh networks have been used in many commercial applications. We focus on a specific use case in cities, where they allow neighbors to connect to each other's wifi, rather than each person connecting directly to an internet service provider. We explore the growth of mesh networks, such as the New York City Mesh, where super-routers service an area of routers, and those in turn provide wifi to other routers that are farther out. Super-routers, in this context, are high-bandwidth routers which connect the rest of the mesh to the greater internet. Currently, mesh networks generally only serve a relatively small community. As more people try to access wifi through a bottleneck (such as a single router connected to the super-router), latency increases. At some point, the latency becomes too great to feasibly use, and people might begin to opt out of the connection. We explore mesh network architectures which could reduce this latency after reading and replicating a model made by Kleineberg and Helbing, discussed in "Collective navigation of complex networks: Participatory greedy routing". They create an agent based cost-benefit model in which each node has the option to cooperate, where they pass along a packet of data, or defect, where they refuse to incur the cost of passing the data. This results in a participatory greedy routing network. They continue on to identify ways to improve the likelihood than an IP routing network stabilizes in a state of high performance, where most packets are successfully transmitted.

We want to see whether it is better for the community as a whole for each router to only connect to a single other router with wifi access, or to connect to all routers with access within range. In theory connecting to a single router would decrease the number of routers connected through any one given router. Connecting to all routers with access would distribute the work routed through any access point. The idea for this multi-connection mesh network in part came from [Strix Systems’ Wireless Mesh](http://www.strixsystems.com/products/datasheets/strixwhitepaper_multihop.pdf).

We create a model of a mesh network to test our hypothesis on based off of [NYC Mesh’s description](https://nycmesh.net/). This model includes super-routers, which reliably provide internet to routers in range, and regular routers which can provide wifi to their neighbors in a smaller range. We model our city as a 100 by 100 unit grid where at each position there can be one router. Cities are initially created with 15 routers, and 5 super-routers. To model the expansion of the mesh network, during each timestep several steps occur:
- Super-routers attempt to connect with any router in range
- Regular routers attempt to connect to other routers, with wifi, in range
- Router owners decide if there is too much latency (latency is larger than their randomly assigned friendliness) due to sharing with others and have the option to stop sharing
- A number of new routers are added to the city (people deciding to join the mesh network)
- The latency of regular routers is updated

Router owners take latency into account when making decisions. A router owner will not let any routers connect to it and will stop sharing with any routers it currently provides internet to if their randomly assigned friendliness is lower than the latency they are experiencing. This corresponds to someone putting a password on their access, or opting out of the network. They are also more likely to share wifi if they have a low latency relative to their friendliness.

We model two different styles of mesh network. In both, when a router is added, it attempts to connect to another router with wifi-access in range. In the first model, the traditional mesh network, as soon as a router connects it stops looking for any other connections. In other words, each router has a single ‘parent’ router that supplies it with wifi. In the second model, each router attempts to connect to every router with access in range, then shares its load equally across all of them.

Latency is calculated based on the number of ‘child’ routers attempting to transmit through a given router as well as the latency of the routers above. The equation becomes:

<p align="center">
latency = A + (1 + c)/N
</p>

where A is the average parent latency, N is the number of parents, and c is the child contribution. If a node has no children, its contribution is 1/N. If it is connected to a super-router, A is 0. When calculating child contribution, the A-term is ignored. In the traditional model, N is always 1 and c is the number of ‘child’ nodes in the graph.

To give an example of the latency distribution in these two models, we create a simple graph and show the latency at each node. The S router is a super-router which contributes no latency to our model.

<p align="center">
<img src="https://raw.githubusercontent.com/LucyWilcox/ParticipatoryGreedyRouting/master/reports/latencycompare.png" width="600">
  <br><br>
  <caption align="bottom"><b>Fig. 1</b> Latency at each router in a hypothetical network in both the single and multi-connetion model.</caption>
</p>

The left graph is the single-connection model and the right is the multi-connection model. In the single-connection model, D has a latency of 4 because it’s parent, B, has latency 3 (2 childern and itself), so D is that latency plus itself because it has no children. In the multi-connection model D has latency 4.125, because the average latency of its parents is 3, the latency contributed from child F is 0.5 (1 split over each of F’s parents), and contribution from C is 0.75 (1.5 split over each of C’s parents). Our formula then is latency =3 + 1/2(1 + 1.25) = 4.125. The multi-connection model has a slightly lower total latency that the single-connection model, and it is better distributed over the routers.

When running each of these models over the same 10 different city configurations for 200 steps we find that the two models lead to different behavior. For each model we graph the average number of routers connected and disconnected at each time step as shown in Figure 2.

<p align="center">
<img src="https://raw.githubusercontent.com/LucyWilcox/ParticipatoryGreedyRouting/master/reports/perstep.png" width="800">
  <br><br>
  <caption align="bottom"><b>Fig. 2</b> Average number of connected and disconnected routers at each step for ten runs. The multi-connection model approaches the rate of routers added (15/step), while the single-connection stays fairly even between number of connected routers and number of disconnected.</caption>
</p>

These graphs show that the percentage of routers connected is higher in the multi-connection model than in the single-connection model. An example end state after 200 steps for cities with identical super-rounter placement is shown below in Figure 3.

<p align="center">
<img src="https://raw.githubusercontent.com/LucyWilcox/ParticipatoryGreedyRouting/master/reports/map.png" width="600">
  <br><br>
  <caption align="bottom"><b>Fig. 3</b> A representation of a single starting city configuration after 200 steps in both the single-connection and multi-connection model. Red circles are the super-routers, and are the same for both models. Red pixels are connected routers. Blue pixels are disconnected routers. Orange background shows the overall range of the routers that have wifi access. Despite the same initial set-up of super-routers, the multi-connection model covers more area with wifi, and more of the routers within that area are connected.</caption>
</p>

In the single-connection model, wifi does not reach the lower right area of the city. We hypothesize that this is because there are some nodes which end up with latency that are too high and stop sharing for the rest of the simulation.

We ran both of these models several times. From this, we found that the multi-connection model did not tend to have significantly lower or higher latency for each router than the single-connection. In fact, at times the mean latency was 1.5 points higher than that of the traditional model, with a higher median value and a lower standard deviation. Other times, each of these value was lower. This may be because the overall latency grows at a slower pace, so disconnections happen less often and the latency slowly builds.

Our simulation suggests that a mesh network architecture which supports multiple-connection between routers would yield a more connected city mesh, where router owners on average experience less latency and in turn are less likely to stop sharing their wifi. There are some other possible ways to optimize coverage which could be tested such as intelligent placement of the superrouters or other incentives for routers owners to share their internet. NYC Mesh does this by encouraging restaurant owners to join the mesh because they often already have open wifi. Other considerations could also be taken into account like the required direct line of sight required to connect with a super-router. 

## Bibliography 

[Kaj-Kolja Kleineberg and Dirk Helbing. "Collective navigation of complex networks: Participatory greedy routing"](https://www.nature.com/articles/s41598-017-02910-x) *Scientific Reports 7, Article number: 2897 (2017) doi:10.1038/s41598-017-02910-x*

Kleineberg and Helbing create an agent-based model where agents represents nodes in an internet of things architecture. Node incurs a cost when passing a message, but profit from the message being successfully delivered. Only nodes which take part in passing the message are rewarded, hence the model is an example of participatory greedy routing. Nodes start as either cooperators or defectors and update their strategy after each message is sent. The author finds a bistable system which has either high performance or breaks down completely. They then go on to analyze factors which cause the system to be more likely to end in a state of high performance.

[“Solving the Wireless Mesh Multi-Hop Dilemma”](http://www.strixsystems.com/products/datasheets/strixwhitepaper_multihop.pdf) *Strix Systems: Networks Without Wires, 2005*

Strix Systems discusses methods to reduce latency, or bandwidth degradation, when routers are several hops away from the supernodes. They mention the multi-radio technique where there are different links for client traffic, ingress wireless backhaul traffic, and egress backhaul traffic. This allows for nodes to receive and transmit simultaneously. We do not replicate this architecture, but were inspired by the concept of splitting traffic as they also discussing have main and failover wireless links.



