# coding: UTF-8
import networkx as nx
import matplotlib.pyplot as plt
import random

def main() :
  # 1. スモールワールドグラフの作成
  initial_node_num = 100  #ノード数
  k = 3                   #エッジ数
  probability = 0.1       #エッジのつなぎかえ確率
  G = nx.watts_strogatz_graph(initial_node_num, k, probability)
  initial_graph_nodes = G.nodes()

  # 2. シンクノード選択(betweenness最大のノードをシンクノードとする)
  initial_betweenness = nx.betweenness_centrality(G)
  sink_node = max((v,k) for k,v in initial_betweenness.iteritems())[1]
  print '---sink node---'
  print sink_node

  # 3. 全ノードのシンクノードに対する最短経路を求める←キャパシティとする
  capacity = {}
  for i in initial_graph_nodes :
    if i == sink_node :
      continue
    capacity[i] = 0
    for j in initial_graph_nodes :
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
    # capacity[i] *= (1.0 / initial_node_num)
  print '---capacity of nodes---'
  print capacity

  # 4. 一定数のノードを削除する(はじめは１つsink_node以外を想定)
  removed_node = sink_node
  while removed_node == sink_node :
    removed_node = random.randint(0, initial_node_num - 1)
    G.remove_node(removed_node)
  print '---removed node---'
  print removed_node

  # 削除されたノードが0になったら終了
  removed_node = [removed_node]
  while len(removed_node_num) > 0 :
    # 5. 全ノードのシンクノードに対する最短経路を再計算←flow
    graph_nodes = G.nodes()
    flow = {}
    for i in graph_nodes :
      flow[i] = 0
      for j in graph_nodes :
        if j == i or j == sink_node :
          continue
        try :
          shortest_paths = [p for p in nx.all_shortest_paths(G, source=j, target=sink_node)]
          shortest_path_num = len(shortest_paths)
          shortest_paths_with_j_num = 0
          for shortest_path in shortest_paths :
            if i in shortest_path :
              shortest_paths_with_j_num += 1
          flow[i] += (shortest_paths_with_j_num/shortest_path_num)
        except : #nx.all_shortest_pathsが0の場合例外が起きるのでpassする
          pass
    print '---flow of nodes---'
    print flow

    # 6. flowがcapacityを超えたら削除する
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

  #描画
  nx.draw_networkx(G, pos=nx.spring_layout(G, scale=5.0), node_size=50, with_labels=False)
  plt.show()

if __name__ == '__main__' :
  main()