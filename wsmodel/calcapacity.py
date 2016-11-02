# coding: UTF-8
import networkx as nx

i = 0
sinknode = 0
G = nx.Graph()

# 全ノードのシンクノードに対する最短経路を求める
def calc_shortestpath(j) :
  if j == i or j == sinknode :
    return 0
  try :
    shortest_paths = [p for p in nx.all_shortest_paths(G, source=j, target=sinknode)]
    shortest_path_num = len(shortest_paths)
    shortest_paths_num_with_i = len([1 for shortest_path in shortest_paths if i in shortest_path])
    capacity_j = (shortest_paths_num_with_i*1.0/shortest_path_num*1.0)
    return capacity_j
  except : #nx.all_shortest_pathsが0の場合例外が起きるのでpassする
    return 0

# 全ノードのキャパシティを求める
def calcapa(i_G, sink_node, rate, alpha, alpha_rate, flow = False) :
  capacity = {}
  global i
  global sinknode
  global G
  sinknode = sink_node
  G = i_G
  special_alpha = 10.0
  for i in G.nodes() :
    if i == sinknode :
      continue
    capacity[i] = sum(map(calc_shortestpath, G.nodes()))

  if(flow) :
    print '---flow of nodes---'
    for i in capacity.iterkeys() :
      capacity[i] = capacity[i]*float(rate)
    print capacity
    return capacity
  else :
    sorted_capacity = sorted(capacity.items(), key = lambda x: x[1], reverse = True)
    for i in range(int(alpha_rate)) :
      capacity[sorted_capacity[i][0]] = capacity[sorted_capacity[i][0]] * float(special_alpha)
    for i in capacity.iterkeys() :
      capacity[i] *= float(alpha)
    print '---capacity of nodes---'
    print capacity
    return capacity
