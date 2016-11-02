# -*- coding: utf-8 -*-
# ショートカットを含むセンサネットワークを作成する
import networkx as nx
import numpy
import random
import math

def make_sensor_network() :
  # 各パラメータ指定
  node_num = 100   #ノード数
  field_length = 316       #フィールド長(ルート100000)
  communication_range = 50 #通信範囲
  p = 0.0155                 #ショートカット発生確率
  phi = 15                  #角度指定
  x = 0
  y = 0
  m1 = 0
  m2 = 0
  # sink_has_neighbor_flag = False

  # while sink_has_neighbor_flag == False :
  G = nx.Graph()  # グラフオブジェクトを作成
  pos = {}        # 位置オブジェクト作成
  # シンクノード配置(ノード番号0をシンクノードとする)
  G.add_node(0)
  pos[0] = numpy.array([x, y])

  # シンクノード以外の座標をランダムに指定して配置
  for node in range(1, node_num) :
    G.add_node(node)
    x = numpy.random.randint(field_length)
    y = numpy.random.randint(field_length)
    pos[node] = numpy.array([x, y])

  # 距離が50以内のノードにエッジを張る
  for i in range(0, node_num - 1) :
    for j in G.nodes() :
      if j == i :
        continue
      distance = numpy.linalg.norm(pos[i] - pos[j])
      if distance <= communication_range  :
        G.add_edge(i,j,color='black',weight=0.5)

  # # シンクノードにパスがあるかチェック
  # if len(G.neighbors(0)) > 0 :
  #   sink_has_neighbor_flag = True

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
      pair_node = numpy.random.randint(node_num)
      if pos[endopoint_node][0] == pos[pair_node][0]: continue
      m2 = (pos[endopoint_node][1] - pos[pair_node][1])*1.0 / (pos[endopoint_node][0] - pos[pair_node][0])
      if m2 < 0: continue
      tan_thita = (m2 - m1) / (1 + m1 * m2)
      distance = numpy.linalg.norm(pos[endopoint_node] - pos[pair_node])
      if distance >= 100 and distance <= 500 and abs(tan_thita) < abs(math.tan(phi)):
        add_flag = True
        # hsensor_num.add(endopoint_node)
        # hsensor_num.add(pair_node)
    G.add_edge(endopoint_node, pair_node, color='blue',weight=1)

  # edges = G.edges()
  # edge_colors = [G[u][v]['color'] for u,v in edges]
  # weights = [G[u][v]['weight'] for u,v in edges]
  # nx.draw_networkx(G, pos, node_size=10, with_labels=False, edge_color=edge_colors, width=weights)

  return G