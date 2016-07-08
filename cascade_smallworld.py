# coding: UTF-8
import networkx as nx
import matplotlib.pyplot as plt
import random

# 1. スモール・ワールドグラフの作成
def make_smallworld_graph() :
  initial_node_num = 300  #ノード数
  k = 4                  #エッジ数
  probability = 0.1       #エッジのつなぎかえ確率
  G = nx.watts_strogatz_graph(initial_node_num, k, probability)
  return G

# 2. 初期の各ノードのbetweennessを計算し、capacityとする
def calculate_capacity(G) :
  capacity = nx.betweenness_centrality(G)
  alpha = 50.0  #耐久度のパラメータをかける
  for i in capacity.iterkeys() :
    capacity[i] *= alpha
  print '---capacity of nodes---'
  print capacity
  return capacity

# 3. 一定数のノードを削除する(はじめは１つ)
def remove_node_random(G) :
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
def remove_node_target(G, capacity) :
  removed_node = {}
  capacity = sorted(capacity.items(), key = lambda x: x[1], reverse = True)
  for i in range(1) :
    removed_node[i] = capacity[i][0]
  G.remove_nodes_from(removed_node.values())
  print '---removed node---'
  print removed_node.values()
  return G

# 4. カスケード故障(削除されたノードが0になったら終了)
def cascade_failure(G, capacity) :
  removed_node = [0] #最初にwhile文に入るために値をいれた
  while len(removed_node) > 0 :
    # betweennessを計算←flowとする
    flow = nx.betweenness_centrality(G)
    print '---flow of nodes---'
    print flow

    # flowがcapacityを超えたら削除する
    removed_node = []
    graph_nodes = G.nodes()
    for i in graph_nodes :
      if capacity[i] < flow[i] :
        G.remove_node(i)
        removed_node.append(i)
    print '---removed node---'
    if len(removed_node) > 0 :
      print 'cascade!'
    print removed_node

# 5. GCのサイズを表示する
def show_giant_component_size(G) :
  giant_component = max(nx.connected_component_subgraphs(G), key=len)
  print '---giant component size---'
  print len(giant_component.nodes())
  return len(giant_component.nodes())

def main() :
  # 1. スモールワールドグラフの作成
  G = make_smallworld_graph()

  # 2. 初期の各ノードのbetweennessを計算し、キャパシティとする
  capacity = calculate_capacity(G)

  # 3. 一定数のノードを削除する
  # G = remove_node_random(G)  # ランダムな故障
  G = remove_node_target(G, capacity)    # 負荷の高いノードを故障

  # 4. カスケード故障(削除されたノードが0になったら終了)
  cascade_failure(G, capacity)

  # 5. GCのサイズを表示する
  GC_size = show_giant_component_size(G)

  f = open('../result/300/all/target_alpha50.0.csv', 'a')
  f.write(str(300 - len(G.nodes())) + ',' + str(GC_size) + "\n")
  f.close()

  #描画
  # nx.draw_networkx(G, pos=nx.spring_layout(G, scale=3.0), node_size=50, with_labels=True)
  # plt.show()

if __name__ == '__main__' :
  main()