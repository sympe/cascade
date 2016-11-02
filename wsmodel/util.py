# coding: UTF-8
import networkx as nx

# GCのサイズを表示する
def show_gc_size(G) :
  giant_component = max(nx.connected_component_subgraphs(G), key=len)
  print '---giant component size---'
  print len(giant_component.nodes())
  return len(giant_component.nodes())

# シンクノードのまでの経路が何本存在するか表示する
def show_pathto_sink(G, sinknode) :
  has_path_num = 0
  for i in G.nodes() :
    if i == sinknode :
      continue
    if nx.has_path(G, i, sinknode) :
      has_path_num += 1
  print '---nodes which have path to sinknode---'
  print has_path_num
  return has_path_num
