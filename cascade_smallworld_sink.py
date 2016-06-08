# coding: UTF-8
import networkx as nx
import matplotlib.pyplot as plt
import random

# 1. スモール・ワールドグラフの作成
def make_smallworld_graph() :
  initial_node_num = 100  #ノード数
  k = 3                   #エッジ数
  probability = 0.1       #エッジのつなぎかえ確率
  G = nx.watts_strogatz_graph(initial_node_num, k, probability)
  return G

# 2. シンクノード選択(betweenness最大のノードをシンクノードとする)
def select_sinknode(G) :
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
    print '---capacity of nodes---'
    print capacity
  return capacity

# 4. 一定数のノードを削除する(はじめは１つsink_node以外を想定)
def remove_node(G, sink_node) :
  removed_node = sink_node
  while removed_node == sink_node :
    removed_node = random.randint(0, len(G.nodes()) - 1)
    G.remove_node(removed_node)
  print '---removed node---'
  print removed_node
  return G

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
    print removed_node

def main() :
  # 1. スモールワールドグラフの作成
  G = make_smallworld_graph()

  # 2. シンクノード選択(betweenness最大のノードをシンクノードとする)
  sink_node = select_sinknode(G)

  # 3. 全ノードのシンクノードに対する最短経路を求め、capacityとする
  capacity = calculate_capacity(G, sink_node)

  # 4. 一定数のノードを削除する(はじめは１つsink_node以外を想定)
  G = remove_node(G, sink_node)

  # 5. カスケード故障(削除されたノードが0になったら終了)
  cascade_failure(G, sink_node, capacity)

  #描画
  # nx.draw_networkx(G, pos=nx.spring_layout(G, scale=5.0), node_size=50, with_labels=False)
  # plt.show()

if __name__ == '__main__' :
  main()