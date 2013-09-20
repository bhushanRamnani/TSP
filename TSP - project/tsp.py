'''
Created on Mar 14, 2013

@Andrew ID: bramnani
@Title : Implementation of the A star algorithm used to solve TSP. Homework 5
@Author: Bhushan Ramnani
''' 

import networkx as nx
import mst
import heapq
import copy
import sys

if __name__ == '__main__':
    pass


class path:
    p = []
    g = 0
    f = 0
    def __cmp__(self, other):
        """Function used by heap in order to order the objects of type path"""
        return cmp(self.f, other.f)


def heuristic(path, G):
    """Takes a path and the associated graph. Returns the MST based heuristic"""
    
    H = copy.deepcopy(G)
    l = len(path)
    if l>2:
        path = path[1:(l-1)]
        H.remove_nodes_from(path)
    elif l==2:
        H.remove_edge(path[0],path[1])    
    M = mst.prim_mst(H)
    weight = 0
    for u,v in M.edges():
        weight = weight + M[u][v]['weight']
    return weight            


def generatePaths(G,u):
    """ Returns a list of possible paths by extending the path u by one more node in the graph G"""
    start = u.p[-1]
    result = []
    List = G.neighbors(start)
    for v in List:
        if v not in u.p:
            newP = path()
            newP.p = copy.deepcopy(u.p)
            newP.p.append(v)
            edgeWt = G.edge[start][v]['weight']
            newP.g = u.g + edgeWt
            newP.f = newP.g + heuristic(newP.p, G)
            result.append(newP)                
    return result


def generateLastPath(G,u):
    """In case the last node to be added in the path is just the source, add the last node and return the final path"""
    start = u.p[-1]
    List = G.neighbors(start)
    newP = None
    for v in List:
        if v==u.p[0]:
            newP = path()
            newP.p = copy.deepcopy(u.p)
            newP.p.append(v)
            newP.g = u.g + G[start][v]['weight']
            newP.f = newP.g
    return newP

      

def aStarTSP(G,s):
    """Resolves the TSP problem using A Star algorithm"""
    """Returns the TSP path"""
    numberOfNodes = G.number_of_nodes()
    H = []
    x = path()
    x.p = [s]    
    while x is not None:
        if len(x.p)== (numberOfNodes+1) and x.p[-1]==s:
            return x
        
        if len(x.p)==(numberOfNodes):
            q = generateLastPath(G,x)
            if q is None:
                continue
            else:
                heapq.heappush(H,q)
        else:        
            for q in generatePaths(G,x):
                heapq.heappush(H, q)#add q to the heap
                    
        try:
            x = heapq.heappop(H)#remove the minimum path from the heap
            #print "Current path = ",x.p
        except IndexError:
            x = None            
    return None
        
def main(inputFile):
    fileName = str(inputFile[1])    
    G = nx.read_gexf(fileName)
    V = G.nodes()
    s = min(V)
    P = aStarTSP(G,s)
    tour = P.p
    print "Tour: ",
    for i in range(len(tour)-1):
        print tour[i],

    print ""
    print "Cost: ",P.f

main(sys.argv)