# coding: UTF-8
import networkx as nx
import matplotlib.pyplot as plt
import random

# 1. スモール・ワールドグラフの作成
def make_smallworld_graph() :
  initial_node_num = 100  #ノード数
  k = 4                   #エッジ数
  probability = 0.1       #エッジのつなぎかえ確率
  G = nx.watts_strogatz_graph(initial_node_num, k, probability)
  return G

# 2. シンクノード選択(betweenness最大のノードをシンクノードとする)
initial_betweenness = {}
def select_sinknode(G) :
  global initial_betweenness
  initial_betweenness = nx.betweenness_centrality(G)
  sink_node = max((v,k) for k,v in initial_betweenness.iteritems())[1]
  print '---sink node---'
  print sink_node
  return sink_node

# 3. 全ノードのシンクノードに対する最短経路を求め、capacityとする
def calculate_capacity(G, sink_node, flow = False) :
  capacity = {}
  for i in G.nodes() :
    if i == sink_node :
      continue
    capacity[i] = 0
    for j in G.nodes() :
      if j == i or j == sink_node :
        continue
      try :
        shortest_paths = [p for p in nx.all_shortest_paths(G, source=j, target=sink_node)]
        shortest_path_num = len(shortest_paths)
        shortest_paths_num_with_j = 0
        for shortest_path in shortest_paths :
          if i in shortest_path :
            shortest_paths_num_with_j += 1
        capacity[i] += (shortest_paths_num_with_j/shortest_path_num)
      except : #nx.all_shortest_pathsが0の場合例外が起きるのでpassする
        pass
    # normalized
    # capacity[i] *= (1.0 / len(G.nodes()))
  if(flow) :
    print '---flow of nodes---'
    print capacity
  else :
    alpha = 10.0   #耐久度のパラメータ
    for i in capacity.iterkeys() :
      capacity[i] *= alpha
    print '---capacity of nodes---'
    print capacity
  return capacity

# 4. 一定数のノードを削除する(はじめは１つsink_node以外を想定)
# ランダムな故障
def remove_node_random(G, sink_node) :
  removed_node = {}
  for i in range(1) :
    removed_node[i] = sink_node
    while removed_node[i] == sink_node :
      removed_node_i = random.randint(0, len(G.nodes()) - 1)
      if removed_node_i not in removed_node.values() :
        removed_node[i] = removed_node_i
  G.remove_nodes_from(removed_node.values())
  print '---removed node---'
  print removed_node.values()
  return G

# 負荷の高いノードを故障
def remove_node_high_betweenness(G, capacity) :
  removed_node = {}
  # capacity = sorted(initial_betweenness.items(), key = lambda x: x[1], reverse = True)
  capacity = sorted(capacity.items(), key = lambda x: x[1], reverse = True)
  for i in range(1) :
    removed_node[i] = capacity[i][0]
  G.remove_nodes_from(removed_node.values())
  print '---removed node---'
  print removed_node.values()
  return G

# 隣接するノードを攻撃
def remove_node_neighbors(G, sink_node, capacity) :
  neighbors = G.neighbors(sink_node)
  neighbors_capacity = {}
  for i in neighbors :
    neighbors_capacity[i] = capacity[i]
  capacity = sorted(neighbors_capacity.items(), key = lambda x: x[1], reverse = True)
  removed_node = {}
  for i in range(1) :
    removed_node[i] = capacity[i][0]
  G.remove_nodes_from(removed_node.values())
  print '---removed node---'
  print removed_node.values()
  return G

# 5. カスケード故障(削除されたノードが0になったら終了)
def cascade_failure(G, sink_node, capacity) :
  removed_node = [0]
  while len(removed_node) > 0 :
    # 全ノードのシンクノードに対する最短経路を再計算し、flowとする
    flow = calculate_capacity(G, sink_node, True)

    # flowがcapacityを超えたら削除する
    removed_node = []
    graph_nodes = G.nodes()
    for i in graph_nodes :
      if i == sink_node :
        continue
      if capacity[i] < flow[i] :
        G.remove_node(i)
        removed_node.append(i)
    print '---removed node---'
    if len(removed_node) > 0 :
      print 'cascade!'
    print removed_node

# 6. GCのサイズを表示する
def show_giant_component_size(G) :
  giant_component = max(nx.connected_component_subgraphs(G), key=len)
  print '---giant component size---'
  print len(giant_component.nodes())

# 7. シンクノードのまでの経路が何本存在するか表示する
def show_has_path_to_sinknode(G, sink_node) :
  has_path_num = 0
  for i in G.nodes() :
    if i == sink_node :
      continue
    if nx.has_path(G, i, sink_node) :
      has_path_num += 1
  print '---nodes which have path to sinknode---'
  print has_path_num


def main() :
  # 1. スモールワールドグラフの作成
  G = make_smallworld_graph()

  # 2. シンクノード選択(betweenness最大のノードをシンクノードとする)
  sink_node = select_sinknode(G)

  # 3. 全ノードのシンクノードに対する最短経路を求め、capacityとする
  capacity = calculate_capacity(G, sink_node)

  # 4. 一定数のノードを削除する(はじめは１つで、sink_node以外を想定)
  # G = remove_node_random(G, sink_node)                # ランダムな故障
  G = remove_node_high_betweenness(G, capacity)       # 負荷の高いノードを故障
  # G =  remove_node_neighbors(G, sink_node, capacity)  # 隣接するノードを攻撃

  # 5. カスケード故障(削除されたノードが0になったら終了)
  cascade_failure(G, sink_node, capacity)

  # 6. GCのサイズを表示する
  show_giant_component_size(G)

  # 7. シンクノードのまでの経路が何本存在するか表示する
  show_has_path_to_sinknode(G, sink_node)

  #描画
  # pos = nx.spring_layout(G, scale=50.0)
  # nx.draw_networkx_nodes(G, pos, node_size=50)
  # nx.draw_networkx_edges(G, pos, width=1)
  # nx.draw_networkx_labels(G, pos, font_size=8)
  # plt.show()

if __name__ == '__main__' :
  main()