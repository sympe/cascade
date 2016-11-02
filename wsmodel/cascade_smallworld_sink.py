# coding: UTF-8
import networkx as nx
import matplotlib.pyplot as plt
from multiprocessing import Pool, Process, Pipe
import random
import sys

class MulHelper(object):
    def __init__(self, cls, mtd_name):
        self.cls = cls
        self.mtd_name = mtd_name

    def __call__(self, *args, **kwargs):
        return getattr(self.cls, self.mtd_name)(*args, **kwargs)

# シンクノードにフローがあるスモールワールドグラフでのカスケード故障
class cascade_smallworkd_sinknode :

  def __init__(self) :
    initial_node_num = 300  #ノード数
    k = 4                   #エッジ数
    probability = 0.1       #エッジのつなぎかえ確率
    self.G = nx.watts_strogatz_graph(initial_node_num, k, probability)
    self.sink_node = 0
    self.alpha = 1.0   #耐久度のパラメータ
    self.capacity = {}
    self.i = 0

  def set_alpha(self, alpha) :
    self.alpha = alpha

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
    if j == self.i or j == self.sink_node :
      return 0
    try :
      shortest_paths = [p for p in nx.all_shortest_paths(self.G, source=j, target=self.sink_node)]
      shortest_path_num = len(shortest_paths)
      shortest_paths_num_with_i = len([1 for shortest_path in shortest_paths if self.i in shortest_path])
      capacity_j = (shortest_paths_num_with_i*1.0/shortest_path_num*1.0)
      return capacity_j
    except : #nx.all_shortest_pathsが0の場合例外が起きるのでpassする
      return 0

  def calculate_capacity(self, flow = False) :
    G = self.G
    capacity = {}
    for self.i in G.nodes() :
      if self.i == self.sink_node :
        continue
      capacity[self.i] = sum(map(MulHelper(self, 'calculate_shortest_path'), G.nodes()))

    if(flow) :
      print '---flow of nodes---'
      print capacity
      return capacity
    else :
      for i in capacity.iterkeys() :
        capacity[i] = capacity[i]*float(self.alpha)
      print '---capacity of nodes---'
      print capacity
      self.capacity = capacity

  # 4. 一定数のノードを削除する(はじめは１つsink_node以外を想定)
  # ランダムな故障
  def remove_node_random(self) :
    capacity = self.capacity
    removed_node = {}
    for i in range(1) :
      removed_node[i] = self.sink_node
      while removed_node[i] == self.sink_node :
        removed_node_i = random.randint(0, len(self.G.nodes()) - 1)
        if removed_node_i not in removed_node.values() :
          removed_node[i] = removed_node_i
    self.G.remove_nodes_from(removed_node.values())
    print '---removed node---'
    print removed_node.values()

  # 負荷の高いノードを故障
  def remove_node_high_betweenness(self) :
    capacity = self.capacity
    removed_node = {}
    # capacity = sorted(initial_betweenness.items(), key = lambda x: x[1], reverse = True)
    capacity = sorted(capacity.items(), key = lambda x: x[1], reverse = True)
    for i in range(1) :
      removed_node[i] = capacity[i][0]
    self.G.remove_nodes_from(removed_node.values())
    print '---removed node---'
    print removed_node.values()

  # 5. カスケード故障(削除されたノードが0になったら終了)
  def cascade_failure(self) :
    sink_node = self.sink_node
    capacity = self.capacity
    removed_node = [0]
    while len(removed_node) > 0 :
      # 全ノードのシンクノードに対する最短経路を再計算し、flowとする
      flow = self.calculate_capacity(True)

      # flowがcapacityを超えたら削除する
      removed_node = []
      graph_nodes = self.G.nodes()
      for i in graph_nodes :
        if i == self.sink_node :
          continue
        if capacity[i] < flow[i] :
          self.G.remove_node(i)
          removed_node.append(i)
      print '---removed node---'
      if len(removed_node) > 0 :
        print 'cascade!'
      print removed_node

  # 6. GCのサイズを表示する
  def show_giant_component_size(self) :
    giant_component = max(nx.connected_component_subgraphs(self.G), key=len)
    print '---giant component size---'
    print len(giant_component.nodes())
    return len(giant_component.nodes())

  # 7. シンクノードのまでの経路が何本存在するか表示する
  def show_has_path_to_sinknode(self) :
    G = self.G
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
  param = sys.argv
  alpha = param[1]
  my_cls = cascade_smallworkd_sinknode()
  my_cls.set_alpha(alpha)

  # 2. シンクノード選択(betweenness最大のノードをシンクノードとする)
  my_cls.select_sinknode()
  # sink_node = select_sinknode_random(G)

  # 3. 全ノードのシンクノードに対する最短経路を求め、capacityとする
  my_cls.calculate_capacity()

  # 4. 一定数のノードを削除する(はじめは１つで、sink_node以外を想定)
  my_cls.remove_node_random()                # ランダムな故障
  # my_cls.remove_node_high_betweenness()       # 負荷の高いノードを故障

  # 5. カスケード故障(削除されたノードが0になったら終了)
  my_cls.cascade_failure()

  # 6. GCのサイズを表示する
  GC_size = my_cls.show_giant_component_size()

  # 7. シンクノードのまでの経路が何本存在するか表示する
  has_path_num = my_cls.show_has_path_to_sinknode()

  # 8. ファイルに書きこみ
  path = "../result/300/sink/random_alpha{0}.csv".format(alpha)
  f = open(path, 'a')
  f.write(str(300 - len(my_cls.G.nodes())) + ',' + str(GC_size) + ',' + str(has_path_num) + "\n")
  f.close()
  #描画
  # pos = nx.spring_layout(G, scale=50.0)
  # nx.draw_networkx_nodes(G, pos, node_size=50)
  # nx.draw_networkx_edges(G, pos, width=1)
  # nx.draw_networkx_labels(G, pos, font_size=8)
  # plt.show()

if __name__ == '__main__' :
  main()