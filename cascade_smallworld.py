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

# 2. 初期の各ノードのbetweennessを計算し、capacityとする
def calculate_capacity(G) :
  capacity = nx.betweenness_centrality(G)
  print '---capacity of nodes---'
  print capacity
  return capacity

# 3. 一定数のノードを削除する(はじめは１つ)
def remove_node(G) :
  removed_node = random.randint(0, len(G.nodes()) - 1)
  G.remove_node(removed_node)
  print '---removed node---'
  print removed_node
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
    print removed_node

def main() :
  # 1. スモールワールドグラフの作成
  G = make_smallworld_graph()

  # 2. 初期の各ノードのbetweennessを計算し、キャパシティとする
  capacity = calculate_capacity(G)

  # 3. 一定数のノードを削除する
  G = remove_node(G)

  # 4. カスケード故障(削除されたノードが0になったら終了)
  cascade_failure(G, capacity)

  #描画
  # nx.draw_networkx(G, pos=nx.spring_layout(G, scale=3.0), node_size=50, with_labels=True)
  # plt.show()

if __name__ == '__main__' :
  main()