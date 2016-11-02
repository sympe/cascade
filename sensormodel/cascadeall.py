# -*- coding: utf-8 -*-
# ショートカットを含むセンサネットワークを作成する
import networkx as nx
import matplotlib.pyplot as plt
import numpy
import random
import math

def make_sensor_network() :
  # 各パラメータ指定
  initial_node_num = 300   #ノード数
  field_length = 250       #フィールド長(1000*1000)
  communication_range = 25 #通信範囲
  p = 0.015                 #ショートカット発生確率
  phi = 15                  #角度指定

  # 位置パラメータの初期化
  pos = {}
  x = 0
  y = 0
  m1 = 0
  m2 = 0

  sink_has_neighbor_flag = False

  while sink_has_neighbor_flag == False :
    # グラフオブジェクトを作成．
    G = nx.Graph()
    # シンクノード配置(ノード番号0をシンクノードとする)
    G.add_node(0)
    pos[0] = numpy.array([x, y])

    # シンクノード以外の座標をランダムに指定して配置
    for node in range(1, initial_node_num) :
      G.add_node(node)
      x = numpy.random.randint(field_length)
      y = numpy.random.randint(field_length)
      pos[node] = numpy.array([x, y])

    # 距離が50以内のノードにエッジを張る
    for i in range(0, initial_node_num - 1) :
      for j in G.nodes() :
        if j == i :
          continue
        distance = numpy.linalg.norm(pos[i] - pos[j])
        if distance <= communication_range  :
          G.add_edge(i,j,color='black',weight=0.5)

    # シンクノードにパスがあるかチェック
    if len(G.neighbors(0)) > 0 :
      sink_has_neighbor_flag = True

  # shortest_paths_to_sink =  nx.single_source_shortest_path_length(G, 0)
  # average_shortest_paths_to_sink = sum(shortest_paths_to_sink.values()) * 1.0 / (len(shortest_paths_to_sink.values()) - 1)
  # average_clustering = nx.average_clustering(G)

  # ショートカット作成
  sampling = int(len(G.edges()) * p)
  sampling_edges = random.sample(G.edges(), sampling)
  # hsensor_num = set()
  for sampling_edge in sampling_edges :
    endopoint_node = random.choice(sampling_edge)
    if pos[endopoint_node][0] == 0 :
      m1 = 1000
    else :
      m1 = pos[endopoint_node][1] * 1.0 / pos[endopoint_node][0]
    add_flag = False
    while add_flag == False :
      pair_node = numpy.random.randint(initial_node_num)
      if pos[endopoint_node][0] == pos[pair_node][0]: continue
      m2 = (pos[endopoint_node][1] - pos[pair_node][1])*1.0 / (pos[endopoint_node][0] - pos[pair_node][0])
      if m2 < 0: continue
      tan_thita = (m2 - m1) / (1 + m1 * m2)
      distance = numpy.linalg.norm(pos[endopoint_node] - pos[pair_node])
      if distance >= 50 and distance <= 125 and abs(tan_thita) < abs(math.tan(phi)):
        add_flag = True
        # hsensor_num.add(endopoint_node)
        # hsensor_num.add(pair_node)
    G.add_edge(endopoint_node, pair_node, color='blue',weight=1)

  # shortest_paths_to_sink =  nx.single_source_shortest_path_length(G,0)
  # average_shortest_paths_to_sink_shortcut = sum(shortest_paths_to_sink.values()) * 1.0 / (len(shortest_paths_to_sink.values()) - 1)
  # average_clustering_shortcut = nx.average_clustering(G)
  # ratio_shortest_paths = average_shortest_paths_to_sink_shortcut / average_shortest_paths_to_sink
  # ratio_clustering = average_clustering_shortcut / average_clustering
  # print len(hsensor_num)

  # ファイルに書きこみ
  # path = "../result/tram/ratio0008.csv"
  # f = open(path, 'a')
  # f.write(str(ratio_shortest_paths) + ' ' + str(ratio_clustering) + "\n")
  # f.close()

  # グラフオブジェクト（点と辺）に座標を関連付けて描画、ショートカットには色付け
  edges = G.edges()
  edge_colors = [G[u][v]['color'] for u,v in edges]
  weights = [G[u][v]['weight'] for u,v in edges]
  nx.draw_networkx(G, pos, node_size=10, with_labels=False, edge_color=edge_colors, width=weights)

  return G

# 2. 初期の各ノードのbetweennessを計算し、キャパシティとする
def calculate_capacity(G) :
  capacity = nx.betweenness_centrality(G)
  alpha = 5.0  #耐久度のパラメータをかける
  for i in capacity.iterkeys() :
    capacity[i] *= alpha
  print '---capacity of nodes---'
  print capacity
  return capacity

# 3. ランダムに1つ削除
def remove_rand(G) :
  # removed_node = {}
  # for i in range(1) :
  removed_node = -1
  while removed_node == -1 or removed_node == 0 :
    removed_node = random.randint(0, len(G.nodes()) - 1)
  G.remove_node(removed_node)
  print '---removed node---'
  print removed_node
  return G

# 3. 負荷の高いノードを故障
def remove_target(G, capacity) :
  removed_node = {}
  capacity = sorted(capacity.items(), key = lambda x: x[1], reverse = True)
  # for i in range(1) :
  removed_node = capacity[0][0]
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
  # 1. センサネットワークの生成
  G = make_sensor_network()

  # 2. 初期の各ノードのbetweennessを計算し、キャパシティとする
  capacity = calculate_capacity(G)
  #
  # # 3. ランダムにノードを1つ削除する
  # G = remove_rand(G)
  G = remove_target(G, capacity)
  #
  # # 4. カスケード故障(削除されたノードが0になったら終了)
  cascade_failure(G, capacity)
  #
  # # 5. GCのサイズを表示する
  GC_size = show_giant_component_size(G)

  f = open('../result/sensor/tram01/all/target_alpha5.csv', 'a')
  f.write(str(300 - len(G.nodes())) + ',' + str(GC_size) + "\n")
  f.close()

  # 表示
  # plt.show()
  # plt.savefig("graph.pdf")

if __name__ == '__main__' :
  main()