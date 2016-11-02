# coding: UTF-8
import networkx as nx
import random

# ランダムに削除
def rand(G, sinknode) :
  removed_node = -1
  while removed_node == -1 or removed_node == sinknode :
    removed_node = random.randint(0, len(G.nodes()) - 1)
  G.remove_node(removed_node)
  print '---removed node---'
  print removed_node
  return G

# 負荷の高いノードを故障
def target(G, capacity) :
  capacity = sorted(capacity.items(), key = lambda x: x[1], reverse = True)
  removed_node = capacity[0][0]
  G.remove_node(removed_node)
  print '---removed node---'
  print removed_node
  return G