# coding: UTF-8
import networkx as nx
import random

# betweenness最大のノードをシンクノードに選択する
def bet(G) :
  initial_betweenness = {}
  initial_betweenness = nx.betweenness_centrality(G)
  print '---betweenness centrality---'
  print initial_betweenness
  sinknode = max((v,k) for k,v in initial_betweenness.iteritems())[1]
  print '---sink node---'
  print sinknode
  return initial_betweenness[sinknode]

# ランダムにシンクノード選択
def rand(G) :
  sink_node = random.randint(0, len(G.nodes()) - 1)
  print '---sink node---'
  print sink_node
  return sink_node
