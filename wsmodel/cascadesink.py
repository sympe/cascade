# coding: UTF-8
import networkx as nx
import matplotlib.pyplot as plt
import random
import sys
import rmnode
import util
import selectsink
import calcapacity

# シンクノードにフローがあるカスケード故障
class CascadeSink :

  def __init__(self) :
    initial_node_num = 100  #ノード数
    k = 4                   #エッジ数
    probability = 0.1       #エッジのつなぎかえ確率
    self.G = nx.watts_strogatz_graph(initial_node_num, k, probability)
    self.sinknode = 0
    self.alpha = 2.0      #耐久度のパラメータ
    self.rate = 1.0       #レートのパラメータ
    self.alpha_rate = 30  #耐久度をかけるノードの割合（負荷の多いノードにだけかける）
    self.capacity = {}

  def set_alpha(self, alpha=1.0) :
    self.alpha = alpha

  def set_rate(self, rate=1.0) :
    self.rate = rate

  def set_alpha_rate(self, alpha_rate=1.0) :
    self.alpha_rate = alpha_rate

  # シンクノード選択
  def select_sinknode(self) :
    self.sinknode = selectsink.bet(self.G) #betweenness最大
    # self.sinknode = selectsink.rand(self.G) #ランダム

  def calculate_capacity(self, flow = False) :
    if(flow) :
      capacity = calcapacity.calcapa(self.G, self.sinknode, self.rate, self.alpha, self.alpha_rate, flow)
      return capacity
    else :
      self.capacity = calcapacity.calcapa(self.G, self.sinknode, self.rate, self.alpha, self.alpha_rate, flow)

  # カスケード故障(削除されたノードが0になったら終了)
  def cascade_failure(self) :
    sinknode = self.sinknode
    capacity = self.capacity
    removed_node = [0]
    while len(removed_node) > 0 :
      # 全ノードのシンクノードに対する最短経路を再計算し、flowとする
      flow = self.calculate_capacity(True)
      # flowがcapacityを超えたら削除する
      removed_node = []
      graph_nodes = self.G.nodes()
      for i in graph_nodes :
        if i == self.sinknode :
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

    print self.sinknode
    # 全ノードのシンクノードに対する最短経路を求め、capacityとする
    # self.calculate_capacity()

    # 一定数のノードを削除する(はじめは１つで、sinknode以外を想定)
    # self.G = rmnode.rand(self.G, self.sinknode)          # ランダムな故障
    # self.G = rmnode.target(self.G, self.capacity)       # 負荷の高いノードを故障

    # カスケード故障(削除されたノードが0になったら終了)
    # self.cascade_failure()

    # GCのサイズを表示する
    # GC_size = util.show_gc_size(self.G)

    # シンクノードのまでの経路が何本存在するか表示する（トラフィック）
    # traffic = float(self.rate) * util.show_pathto_sink(self.G, self.sinknode)

    # ファイルに書きこみ
    # path = "../result/special_alpha/{}.csv".format(self.alpha_rate)
    # f = open(path, 'a')
    # f.write(str(300 - len(self.G.nodes())) + ',' + str(GC_size) + ',' + str(traffic) + "\n")
    # f.close()

    # path = "../result/count_betweenness/ws100.csv"
    # f = open(path, 'a')
    # f.write(str(self.sinknode) + "\n")
    # f.close()

    #描画
    # nx.draw_networkx(self.G, pos=nx.spring_layout(G, scale=3.0), node_size=50, with_labels=True)
    # plt.show()

def main() :
  # param = sys.argv
  # rate = param[1]
  # alpha_rate = param[1]
  ccsink = CascadeSink()
  # ccsink.set_alpha_rate(alpha_rate)
  ccsink.main()

if __name__ == '__main__' :
  main()