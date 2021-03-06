# Reputable Greedy Networks
## Kaitlyn Keil and Lucy Wilcox
 
**Abstract**

We plan on replicating Kleineberg and Helbing’s agent-based participatory greedy routing model. They model the transfer of packages in the Internet of Things. Each node incurs a cost for transferring packages but also gets a reward if a package they pass is successfully delivered. They find that local cooperative clusters and cooperative nodes help create a stable cooperative system. Generally, they find the system is bistable and either ends up in a state of high performance or a complete breakdown. We will replicate their system and include a reputation system which biases where packages are passed.
__________________________________

We will replicate the creation of hidden metric spaces within the network of nodes and then the transferal of data across the network using greedy routing, where nodes pass the data along to the neighbor closest to the target, and the delivery fails if the same node gets the information twice. We will continue on to implement the participatory greedy routing, where each node can opt in or out of delivery, thus making the delivery fail. Once we have these working satisfactorily (with a cost-benefit system to allow for choice), we hope to add a reputation system, where nodes know how often sending to a certain node has helped in the success or failure and can decide where to deliver the data to next in accordance to this. We also are considering competitive networks, where each node can only join one at a time. These plots would show the likelihood of delivery rates for different parameters of cooperation (C) and different payoffs (b) likes the ones below by Kleineberg and Helbing.

<p align="center">
<img src="https://raw.githubusercontent.com/LucyWilcox/ParticipatoryGreedyRouting/master/reports/candbchart.jpg">
 <br><br>
</p>

We will add to this a history, from which we will determine cooperation based on the ratio of prior cooperation/defection and the last action. From this, we will see if including reputation improves the probability of a high performance end state at each breakdown and cooperation rate. We also plan to track how many packages each node passes and see how this changes with reputation. To examine this we can graph a PDF and/or CDF distribution to identify changes. We predict reputation would direct more messages through a smaller number of nodes, creating a more long-tailed distribution.

There is a lot of math in the paper, and some of it is easier to parse through than other parts. However, we feel like the paper outlines what is going on well enough that we can follow it relatively easily. The reputation system is similar enough to the IPD that we are fairly confident. We are both frequently off-campus, so we plan on staying in communication over Messenger. Lucy will do make the base of the replication and document it this weekend. Kaitlyn will continue off of this over the following week.  We will both meet on Monday to make sure we are on the same page. We intend to have the greedy routing replication (without the participatory element) done by next Friday, with a stretch goal of adding participation based on cost-benefit analysis. If this does not get completed, we will implement it over the next week. We worked similarly last time and it worked out well. We plan to keep a list of tasks in our README, so that it is easy for us to see what needs to be done next.

## Bibliography 

[Kaj-Kolja Kleineberg and Dirk Helbing. "Collective navigation of complex networks: Participatory greedy routing"](https://www.nature.com/articles/s41598-017-02910-x) *Scientific Reports 7, Article number: 2897 (2017) doi:10.1038/s41598-017-02910-x*

Kleineberg and Helbing create an agent-based model where agents represents nodes in an internet of things architecture. Node incurs a cost when passing a message, but profit from the message being successfully delivered. Only nodes which take part in passing the message are rewarded, hence the model is an example of participatory greedy routing. Nodes start as either cooperators or defectors and update their strategy after each message is sent. The author finds a bistable system which has either high performance or breaks down completely. They then go on to analyze factors which cause the system to be more likely to end in a state of high performance.

[Cuesta, J. A., Gracia-Lázaro, C., Ferrer, A., Moreno, Y. & Sánchez, A. Reputation drives cooperative behaviour and network formation in human groups.](https://www.nature.com/articles/srep07843) *Sci. Rep. 5, 7843 (2015).*

Cuesta et. al. explore how reputation can improve cooperation, particularly in a network where players can reconfigured based on reputation. They quantify reputation as a function of the fraction of cooperative to defective past actions and the last action performed. They find that cooperation decays more quickly without memory of prior actions.

