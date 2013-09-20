TSP
TSP using A* implemented in Python. We search the state space of the possible paths using the heuristic as the MST of the graph without the nodes a_2 to a_n-1. eg. h(a->b->c->d) = total weight of the MST of (G - {b,c}).

It takes a graph in gexf format.

You can run it using the command, python mst.py filename.gexf