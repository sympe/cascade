# coding: UTF-8
import networkx as nx
import matplotlib.pyplot as plt
import random

# ランダムに削除
def rand(G) :
  removed_node = {}
  for i in range(1) :
    removed_node[i] = -1
    while removed_node[i] == -1 :
      removed_node_i = random.randint(0, len(G.nodes()) - 1)
      if removed_node_i not in removed_node.values() :
        removed_node[i] = removed_node_i
  G.remove_nodes_from(removed_node.values())
  print '---removed node---'
  print removed_node.values()
  return G

# 負荷の高いノードを故障
def target(G, capacity) :
  removed_node = {}
  capacity = sorted(capacity.items(), key = lambda x: x[1], reverse = True)
  for i in range(1) :
    removed_node[i] = capacity[i][0]
  G.remove_nodes_from(removed_node.values())
  print '---removed node---'
  print removed_node.values()
  return G
