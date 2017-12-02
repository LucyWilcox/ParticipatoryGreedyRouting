# Multi-Connection Support in Mesh Networks

## Kaitlyn Keil and Lucy Wilcox

**Abstract**

TODO
_________________________

With the rise of the internet and, specifically, the Internet of Things, networks are becoming increasingly necessary, whether it be between multiple devices owned by a single individual or across many households. These networks can allow for the transferal of data to a separate device as well as the delivery of a commodity such as wifi from one point to another. However, this transferral does not come without some cost. The more data being sent through a single point, or node, the slower that node will be able to operate. Kleineberg and Helbing used this cost model to examine networks in which each node has the option to be either a cooperator, which passes along a packet of data, or a defector, which refuses to incur the cost of passing the data, to create a participatory greedy routing network. Through this model, they begin to analyze what factors contribute to the system being more likely to end in a state of high performance, where most packets are successfully transmitted.

We were inspired by this idea of optimizing networks to attempt our own model of a cost-based network. We chose to focus on mesh networks, such as the one based in New York City, where super-routers service an area of routers, and those routers in turn provide wifi to others. Currently, mesh networks can only serve a relatively small community, and the more people trying to access wifi through a bottleneck (such as a single router connected to the super-router), the greater the latency to all. At some point, the latency becomes too great to feasibly use, and people might begin to opt out of the connection. We want to see whether it is better for the community as a whole for each router to only connect to a single other router that has access--in theory decreasing the number of routers connected through any one given router--or to connect to any router with access in range--increasing the number of connected routers for any other router, but also distributing the work routed through any access point. The idea for this multi-connection mesh network in part came from [Strix Systems’ Wireless Mesh](http://www.strixsystems.com/products/datasheets/strixwhitepaper_multihop.pdf).

We created a model of a mesh network to test our hypothesis on based off of [NYC Mesh’s description](https://nycmesh.net/). This model includes super-routers, which reliably provide internet to routers in range, and regular routers which can provide wifi to their neighbors in a smaller range. We model our city as a 100 by 100 unit grid where at each position there can be one router. Cities are initially created with 15 routers, and 5 super-routers. To model the expansion of the mesh network, during each timestep several steps occur:
- Super-routers attempt to connect with any router in range
- Regular routers attempt to connect to other routers, with wifi, in range
- Router owners decide if there is too much latency due to sharing with others and have the option to stop sharing
- A number of new routers are added to the city (people deciding to join the mesh network)
- The latency of regular routers is updated

Router owners take latency into account when making decisions. A router owner will not let any routers connect to it and will stop sharing with any routers it currently provides internet to if their randomly assigned friendliness is lower than the latency they are experiencing. They are also more likely to share wifi if they have a low latency relative to their friendliness.

We model two different styles of mesh network. In both, when a router is added, it attempts to connect to another router with wifi-access in range. In the first model, the traditional mesh network, as soon as a router connects it stops looking for any other connections. In other words, each router has a single ‘parent’ router that supplies it with wifi. In the second model, each router attempts to connect to every router with access in range, then shares its load equally across all of them.

Latency is calculated based on the number of ‘child’ routers attempting to transmit through a given router as well as the latency of the routers above. The equation becomes:

<p align="center">
latency = A + 1/N(1 + c)
</p>

Where A is the average parent latency, N is the number of parents, and c is the child contribution. If a node has no children, its contribution is 1N. If it is connected to a super-router, A is 0. When calculating child contribution, the A-term is ignored. In the traditional model, N is always 1 and c is the number of ‘child’ nodes in the graph.

To give an example of the latency distribution in these two models, we create a simple graph and show the latency at each node. The S router is a superrouter which contributes no latency to our model.


The left graph is the single-connection model and the right is the multi-connection model. In the single-connection model, D has a latency of 4 because it’s parent, B, has latency 3 (2 childern and itself), so D is that latency plus itself because it has no children. In the multi-connection model D has latency 4.125, because the average latency of its parents is 3, the latency contributed from child F is 0.5 (1 split over each of F’s parents), and contribution from C is 0.75 (1.5 split over each of C’s parents). Our formula then is latency =3 +12(1+1.25)=4.125. The multi-connection model has a slightly lower total latency that the single-connection model, and it is better distributed over the routers.

When running each of these models over the same 10 different city configurations for 200 steps we find that the two models lead to different behavior. For each model we graph the average number of routers connected and disconnected at each time step as shown in Figure 2.



These graphs show that the percentage of routers connected is higher in the multi-connection model than in the single-connection model. An example end state after 200 steps for cities with identical superrounter placement is shown below in Figure 3.



In the single-connection model, wifi does not reach the lower right area of the city. We hypothesize that this is because there are some nodes which end up with latency that are too high and stop sharing for the rest of the simulation.

Our simulation suggests that a mesh network architecture which supports multiple-connection between routers would yield a more connected city mesh, where router owners on average experience less latency and in turn are less likely to stop sharing their wifi. There are some other possible ways to optimize coverage which could be tested such as intelligent placement of the superrouters or other incentives for routers owners to share their internet. NYC Mesh does this by encouraging restaurant owners to join the mesh because they often already have open wifi. Other considerations could also be taken into account like the required direct line of sight required to connect with a superrouter. 

## Bibliography 

[Kaj-Kolja Kleineberg and Dirk Helbing. "Collective navigation of complex networks: Participatory greedy routing"](https://www.nature.com/articles/s41598-017-02910-x) *Scientific Reports 7, Article number: 2897 (2017) doi:10.1038/s41598-017-02910-x*

Kleineberg and Helbing create an agent-based model where agents represents nodes in an internet of things architecture. Node incurs a cost when passing a message, but profit from the message being successfully delivered. Only nodes which take part in passing the message are rewarded, hence the model is an example of participatory greedy routing. Nodes start as either cooperators or defectors and update their strategy after each message is sent. The author finds a bistable system which has either high performance or breaks down completely. They then go on to analyze factors which cause the system to be more likely to end in a state of high performance.

[“Solving the Wireless Mesh Multi-Hop Dilemma”](http://www.strixsystems.com/products/datasheets/strixwhitepaper_multihop.pdf) *Strix Systems: Networks Without Wires, 2005*

Strix Systems discusses methods to reduce latency, or bandwidth degradation, when routers are several hops away from the supernodes. They mention the multi-radio technique where there are different links for client traffic, ingress wireless backhaul traffic, and egress backhaul traffic. This allows for nodes to receive and transmit simultaneously. We do not replicate this architecture, but were inspired by the concept of splitting traffic as they also discussing have main and failover wireless links.



