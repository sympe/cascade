# -*- coding: utf-8 -*-
import networkx as nx
import matplotlib.pyplot as plt
import numpy
import random
import math
import sys
import rmnode
import util
import calcapacity
import makesensornet

# シンクノードにフローがあるカスケード故障
class CascadeSink :

  def __init__(self) :
    self.G = nx.Graph()
    self.sinknode = 0
    self.alpha = 1.0   #耐久度のパラメータ
    self.rate = 1.0    #レートのパラメータ
    self.capacity = {}

  def set_alpha(self, alpha=1.0) :
    self.alpha = alpha

  def calculate_capacity(self, flow = False) :
    if(flow) :
      capacity = calcapacity.calcapa(self.G, self.sinknode, self.rate, self.alpha, flow)
      return capacity
    else :
      self.capacity = calcapacity.calcapa(self.G, self.sinknode, self.rate, self.alpha, flow)

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
    # センサネットワーク生成
    self.G = makesensornet.make_sensor_network()

    # 全ノードのシンクノードに対する最短経路を求め、capacityとする
    self.calculate_capacity()

    # 一定数のノードを削除する(はじめは１つで、sinknode以外を想定)
    # self.G = rmnode.rand(self.G, self.sinknode)          # ランダムな故障
    self.G = rmnode.target(self.G, self.capacity)       # 負荷の高いノードを故障

    # カスケード故障(削除されたノードが0になったら終了)
    self.cascade_failure()

    # GCのサイズを表示する
    GC_size = util.show_gc_size(self.G)

    # シンクノードのまでの経路が何本存在するか表示する（トラフィック）
    traffic = util.show_pathto_sink(self.G, self.sinknode)

    # ファイルに書きこみ
    path = "../result/sensor/01/target/alpha{}.csv".format(self.alpha)
    f = open(path, 'a')
    f.write(str(100 - len(self.G.nodes())) + ',' + str(GC_size) + ',' + str(traffic) + "\n")
    f.close()

    #描画
    # plt.show()

def main() :
  param = sys.argv
  alpha = param[1]
  ccsink = CascadeSink()
  ccsink.set_alpha(alpha)
  ccsink.main()

if __name__ == '__main__' :
  main()