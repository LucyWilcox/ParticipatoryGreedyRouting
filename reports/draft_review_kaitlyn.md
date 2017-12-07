# Review of [Gaygents](https://github.com/poosomooso/Gaygents/blob/master/reports/draft_final_report.ipynb)

## Final Project Draft for Complexity Science, Fall 2017

### Report by Serena Chen and Apurva Raman

### Review by Kaitlyn Keil

It appears that the paper they read before was modeling the effect of online dating on the number of heterosexual, interracial marriages, due to a supposedly higher number of interracial connections being drawn. They (Serena and Apurva) then went on to expand it to couples of other orientations. They call out some flaws with the model well, though I'm not sure that they go on to address the issues they found. The replication seems very straightforward, as they had code to follow, and their comparison of results is generally plausible. However, if noise was caused by a low number of simulations, it seems like running more simulations shouldn't be particularly difficult.

The explanation of how the model runs is high-level, but still detailed enough that I feel like I have a good sense for how it works. I am curious how the connections are drawn, particularly with the internet as a factor (which can ignore distance) and whether divorce is a thing that can happen (two agents find more compatible targets). It seems like with the caveat about connections, Ortega and Hergovich's assumptions are somewhat null, or at least highly unrealistic.

The question that the original paper seems to be answering is that having more interracial connections leads to stronger marriages. There is also a 'diversity' axis that I... don't quite get but okay. It seems like the opposite of diversity if 1 means perfectly matched. That might need a little more clearing up.

There is some proof reading and capitalization that needs to happen. I also feel like I don't know whether the probability of interracial connections getting higher means that any one agent has a higher percent of their connections to an agent of a different race or if it means they just get more connections.

The graphs also have r=2, dir; r=2, long; r=5, dir; r=5, long. I am not sure which of these I should be comparing. From the Python, it looks like r2dir, but having that explicitly stated would be good.

The purpose of the extension is very clear, and it's obvious what results they are expecting or hoping for. I look forward to seeing actual results, too! Overall, after some proof-reading and inclusion of a few more details, I think it will be a strong paper.