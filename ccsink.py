# coding: UTF-8
import networkx as nx
import matplotlib.pyplot as plt
from multiprocessing import Pool, Process, Pipe
import random
import sys
import rmnode
import util
import selectsink

# シンクノードにフローがあるカスケード故障
class CascadeSink :

  def __init__(self) :
    initial_node_num = 100  #ノード数
    k = 4                   #エッジ数
    probability = 0.1       #エッジのつなぎかえ確率
    self.G = nx.watts_strogatz_graph(initial_node_num, k, probability)
    self.sink_node = 0
    self.alpha = 1.0   #耐久度のパラメータ
    self.capacity = {}
    self.i = 0

  def set_alpha(self, alpha=1.0) :
    self.alpha = alpha

  # シンクノード選択
  def select_sinknode(self) :
    self.sink_node = selectsink.bet(self.G) #betweenness最大
    # self.sink_node = selectsink.rand(self.G) #ランダム

  # 全ノードのシンクノードに対する最短経路を求め、capacityとする
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
      capacity[self.i] = sum(map(self.calculate_shortest_path, G.nodes()))

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

  # カスケード故障(削除されたノードが0になったら終了)
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

  def main(self) :
    # シンクノード選択
    self.select_sinknode()

    # 全ノードのシンクノードに対する最短経路を求め、capacityとする
    self.calculate_capacity()

    # 一定数のノードを削除する(はじめは１つで、sink_node以外を想定)
    self.G = rmnode.rand(self.G)                # ランダムな故障
    # self.G = rmnode.target(self.G, self.capacity)       # 負荷の高いノードを故障

    # カスケード故障(削除されたノードが0になったら終了)
    self.cascade_failure()

    # GCのサイズを表示する
    GC_size = util.show_gc_size(self.G)

    # シンクノードのまでの経路が何本存在するか表示する
    has_path_num = util.show_pathto_sink(self.G, self.sink_node)

    # ファイルに書きこみ
    # path = "../result/300/sink/random_alpha{0}.csv".format(alpha)
    # f = open(path, 'a')
    # f.write(str(300 - len(self.G.nodes())) + ',' + str(GC_size) + ',' + str(has_path_num) + "\n")
    # f.close()

    #描画
    # nx.draw_networkx(self.G, pos=nx.spring_layout(G, scale=3.0), node_size=50, with_labels=True)
    # plt.show()

def main() :
  param = sys.argv
  # alpha = param[1]

  ccsink = CascadeSink()
  # ccsink.set_alpha(alpha)
  ccsink.set_alpha()
  ccsink.main()

if __name__ == '__main__' :
  main()