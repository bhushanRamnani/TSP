#!/usr/bin/env python

from __future__ import division
import math
import random
import networkx as nx

"""
Implementations of d-Heaps and Prim's MST following Tarjan. Includes testing
and visualization code for both.
"""

ARITY = 3  # the branching factor of the d-Heaps

#=======================================================================
# d-Heap
#=======================================================================

class HeapItem(object):
    """Represents an item in the heap"""
    def __init__(self, key, item):
        self.key = key
        self.item = item
        self.pos = None

def makeheap(S):
    """Create a heap from set S, which should be a list of pairs (key, item)."""
    heap = list(HeapItem(k,i) for k,i in S)
    for pos in xrange(len(heap)-1, -1, -1):
        siftdown(heap[pos], pos, heap)
    return heap

def findmin(heap):
    """Return element with smallest key, or None if heap is empty"""
    return heap[0] if len(heap) > 0 else None

def deletemin(heap):
    """Delete the smallest item"""
    if len(heap) == 0: return None
    i = heap[0]
    last = heap[-1]
    del heap[-1]
    if len(heap) > 0:
        siftdown(last, 0, heap)
    return i

def heapinsert(key, item, heap):
    """Insert an item into the heap"""
    heap.append(None)
    hi = HeapItem(key,item)
    siftup(hi, len(heap)-1, heap)
    return hi

def heap_decreasekey(hi, newkey, heap):
    """Decrease the key of hi to newkey"""
    hi.key = newkey
    siftup(hi, hi.pos, heap)

def siftup(hi, pos, heap):
    """Move hi up in heap until it's parent is smaller than hi.key"""
    p = parent(pos)
    while p is not None and heap[p].key > hi.key:
        heap[pos] = heap[p]
        heap[pos].pos = pos
        pos = p
        p = parent(p)
    heap[pos] = hi
    hi.pos = pos

def siftdown(hi, pos, heap):
    """Move hi down in heap until its smallest child is bigger than hi's key"""
    c = minchild(pos, heap)
    while c != None and heap[c].key < hi.key:
        heap[pos] = heap[c]
        heap[pos].pos = pos
        pos = c
        c = minchild(c, heap)
    heap[pos] = hi
    hi.pos = pos

def parent(pos):
    """Return the position of the parent of pos"""
    if pos == 0: return None
    return int(math.ceil(pos / ARITY) - 1)

def children(pos, heap):
    """Return a list of children of pos"""
    return xrange(ARITY * pos + 1, min(ARITY * (pos + 1) + 1, len(heap)))

def minchild(pos, heap):
    """Return the child of pos with the smallest key"""
    minpos = minkey = None
    for c in children(pos, heap):
        if minkey == None or heap[c].key < minkey:
            minkey, minpos = heap[c].key, c
    return minpos


#=======================================================================
# Prim's minimum spanning tree algorithm
#=======================================================================

def prim_mst(G):
    """Compute the minimum spanning tree of G. Assumes each edge has an
    attribute 'length' giving it's length. Returns a dictionary P such
    that P[u] gives the parent of u in the MST."""

    for u in G.nodes():
        G.node[u]['distto'] = float("inf")  # key stores the Prim key
        G.node[u]['heap'] = None         # heap = pointer to node's HeapItem
    parent = {}

    heap = makeheap([])
    v = G.nodes()[0]

    # go through vertices in order of closest to current tree
    while v != None:
        G.node[v]['distto'] = float("-inf") # v now in the tree

        #snapshot_mst(G, parent)
        
        # update the estimated distance to each of v's neighbors
        for w in G.neighbors(v):
            # if new length is smaller that old length, update
            if G[v][w]['weight'] < G.node[w]['distto']:
                # closest tree node to w is v
                G.node[w]['distto'] = G[v][w]['weight']
                parent[w] = v

                # add to heap or decreae key if already in heap
                hi = G.node[w]['heap']
                if hi is None:
                    G.node[w]['heap'] = heapinsert(G.node[w]['distto'], w, heap)
                else:
                    heap_decreasekey(hi, G.node[w]['distto'], heap)
        # get the next vertex closest to the tree
        v = deletemin(heap)
        v = v.item if v is not None else None
    return parent
