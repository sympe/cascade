# coding: UTF-8
import networkx as nx
import matplotlib.pyplot as plt
from multiprocessing import Pool
import random

# シンクノードにフローがあるスモールワールドグラフでのカスケード故障
class cascade_smallworkd_sinknode :

  def __init__(self) :
    initial_node_num = 100  #ノード数
    k = 4                   #エッジ数
    probability = 0.1       #エッジのつなぎかえ確率
    self.G = nx.watts_strogatz_graph(initial_node_num, k, probability)
    self.sink_node = 0
    self.alpha = 5.0   #耐久度のパラメータ

  # 2. シンクノード選択(betweenness最大のノードをシンクノードとする)
  def select_sinknode(self) :
    G = self.G
    initial_betweenness = {}
    initial_betweenness = nx.betweenness_centrality(G)
    self.sink_node = max((v,k) for k,v in initial_betweenness.iteritems())[1]
    print '---sink node---'
    print self.sink_node

  # 3. ランダムにシンクノード選択
  def select_sinknode_random(self) :
    G = self.G
    sink_node = random.randint(0, len(G.nodes()) - 1)
    print '---sink node---'
    print sink_node
    return sink_node

  # 3. 全ノードのシンクノードに対する最短経路を求め、capacityとする
  def calculate_shortest_path(self, j) :
    if j == i or j == sink_node :
      return 0
    try :
      shortest_paths = [p for p in nx.all_shortest_paths(G, source=j, target=sink_node)]
      shortest_path_num = len(shortest_paths)
      # shortest_paths_num_with_j = 0
      # for shortest_path in shortest_paths :
      #   if i in shortest_path :
      #     shortest_paths_num_with_j += 1
      shortest_paths_num_with_i = len([1 for shortest_path in shortest_paths if i in shortest_path])
      capacity_j = (shortest_paths_num_with_i*1.0/shortest_path_num*1.0)
      return capacity_j
    except : #nx.all_shortest_pathsが0の場合例外が起きるのでpassする
      return 0

  def calculate_capacity(self, flow = False) :
    G = self.G
    capacity = {}
    for i in G.nodes() :
      if i == self.sink_node :
        continue
      capacity[i] = 0
      # capacity[i] = sum(map(self.calculate_shortest_path, G.nodes()))
      for j in G.nodes() :
        if j == i or j == self.sink_node :
          continue
        try :
          shortest_paths = [p for p in nx.all_shortest_paths(G, source=j, target=self.sink_node)]
          shortest_path_num = len(shortest_paths)
          shortest_paths_num_with_i = len([1 for shortest_path in shortest_paths if i in shortest_path])
          capacity[i] += (shortest_paths_num_with_i*1.0/shortest_path_num*1.0)
        except : #nx.all_shortest_pathsが0の場合例外が起きるのでpassする
          pass

    if(flow) :
      print '---flow of nodes---'
      print capacity
    else :
      for i in capacity.iterkeys() :
        capacity[i] *= self.alpha
      print '---capacity of nodes---'
      print capacity
    return capacity

  # 4. 一定数のノードを削除する(はじめは１つsink_node以外を想定)
  # ランダムな故障
  def remove_node_random(self, G, sink_node) :
    removed_node = {}
    for i in range(1) :
      removed_node[i] = self.sink_node
      while removed_node[i] == self.sink_node :
        removed_node_i = random.randint(0, len(G.nodes()) - 1)
        if removed_node_i not in removed_node.values() :
          removed_node[i] = removed_node_i
    G.remove_nodes_from(removed_node.values())
    print '---removed node---'
    print removed_node.values()
    return G

  # 負荷の高いノードを故障
  def remove_node_high_betweenness(self, G, capacity) :
    removed_node = {}
    # capacity = sorted(initial_betweenness.items(), key = lambda x: x[1], reverse = True)
    capacity = sorted(capacity.items(), key = lambda x: x[1], reverse = True)
    for i in range(1) :
      removed_node[i] = capacity[i][0]
    G.remove_nodes_from(removed_node.values())
    print '---removed node---'
    print removed_node.values()
    return G

  # 5. カスケード故障(削除されたノードが0になったら終了)
  def cascade_failure(self, G, sink_node, capacity) :
    removed_node = [0]
    while len(removed_node) > 0 :
      # 全ノードのシンクノードに対する最短経路を再計算し、flowとする
      flow = self.calculate_capacity(True)

      # flowがcapacityを超えたら削除する
      removed_node = []
      graph_nodes = G.nodes()
      for i in graph_nodes :
        if i == self.sink_node :
          continue
        if capacity[i] < flow[i] :
          G.remove_node(i)
          removed_node.append(i)
      print '---removed node---'
      if len(removed_node) > 0 :
        print 'cascade!'
      print removed_node

  # 6. GCのサイズを表示する
  def show_giant_component_size(self, G) :
    giant_component = max(nx.connected_component_subgraphs(G), key=len)
    print '---giant component size---'
    print len(giant_component.nodes())
    return len(giant_component.nodes())

  # 7. シンクノードのまでの経路が何本存在するか表示する
  def show_has_path_to_sinknode(self, G, sink_node) :
    has_path_num = 0
    for i in G.nodes() :
      if i == self.sink_node :
        continue
      if nx.has_path(G, i, self.sink_node) :
        has_path_num += 1
    print '---nodes which have path to sinknode---'
    print has_path_num
    return has_path_num

def main() :
  my_class = cascade_smallworkd_sinknode()

  # 2. シンクノード選択(betweenness最大のノードをシンクノードとする)
  my_class.select_sinknode()
  # sink_node = select_sinknode_random(G)

  # 3. 全ノードのシンクノードに対する最短経路を求め、capacityとする
  capacity = my_class.calculate_capacity()

  # 4. 一定数のノードを削除する(はじめは１つで、sink_node以外を想定)
  # G = remove_node_random(G, sink_node)                # ランダムな故障
  G = my_class.remove_node_high_betweenness(my_class.G, capacity)       # 負荷の高いノードを故障

  # 5. カスケード故障(削除されたノードが0になったら終了)
  my_class.cascade_failure(my_class.G, my_class.sink_node, capacity)

  # 6. GCのサイズを表示する
  GC_size = my_class.show_giant_component_size(my_class.G)

  # 7. シンクノードのまでの経路が何本存在するか表示する
  has_path_num = my_class.show_has_path_to_sinknode(my_class.G, my_class.sink_node)

  # 8. ファイルに書きこみ
  # f = open('../result/limit_alpha/alpha10.csv', 'a')
  # f.write(str(100 - len(G.nodes())) + ',' + str(GC_size) + ',' + str(has_path_num) + "\n")
  # f.close()
  #描画
  # pos = nx.spring_layout(G, scale=50.0)
  # nx.draw_networkx_nodes(G, pos, node_size=50)
  # nx.draw_networkx_edges(G, pos, width=1)
  # nx.draw_networkx_labels(G, pos, font_size=8)
  # plt.show()

if __name__ == '__main__' :
  main()