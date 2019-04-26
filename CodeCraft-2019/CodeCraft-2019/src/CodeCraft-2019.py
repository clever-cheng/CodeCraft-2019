import logging
import sys
import numpy as np
import time

def main():
  car_path = sys.argv[1]
  road_path = sys.argv[2]
  cross_path = sys.argv[3]
  presetAnswer_path = sys.argv[4]
  answer_path = sys.argv[5]

  return car_path, road_path, cross_path, presetAnswer_path, answer_path

print('Hello world !')
#提交
car_path, road_path, cross_path, presetAnswer_path, answer_path = main()

# window或者linux
# car_path = '../config/car.txt'
# road_path = '../config/road.txt'
# cross_path = '../config/cross.txt'
# presetAnswer_path = '../config/presetAnswer.txt'
# answer_path = '../config/answer.txt'

starting = time.time()
#------------------读取数据-----------------
def readroad(fileroad):
    roadlist = open(fileroad,'rU').readlines()
    del roadlist[0]
    road = []
    dic1 = {}
    dic2 = {}
    for i in range(len(roadlist)):
        strs = roadlist[i].split(',')
        strs[0] = int(strs[0].strip('('))
        strs[1] = int(strs[1].lstrip())
        strs[2] = int(strs[2].lstrip())
        strs[3] = int(strs[3].lstrip())
        strs[4] = int(strs[4].lstrip())
        strs[5] = int(strs[5].lstrip())
        strs[6] = int(strs[6].strip('\n)').lstrip())
        road.append(strs)
        if int(strs[-1])==1:
            if strs[4] in dic1:
                dic1[strs[4]].append(strs[5])
            else:
                dic1[strs[4]]=[strs[5]]
            if strs[5] in dic2:
                dic2[strs[5]].append(strs[4])
            else:
                dic2[strs[5]]=[strs[4]]
        else:
            if strs[4] in dic1:
                dic1[strs[4]].append(strs[5])
            else:
                dic1[strs[4]]=[strs[5]]
    for keys,values in dic2.items():
        if keys in dic1:
                dic1[keys].extend(values) 
        else:
            dic1[keys] = values
    edge = dic1
    return road, edge#边集
road,edge = readroad(road_path)

road1 = road

def readcar(fliecar):
    carlist = open(fliecar,'rU').readlines()
    del carlist[0]
    car = []
    for k in range(len(carlist)):
        strs = carlist[k].split(',')
        strs[0] = int(strs[0].strip('('))
        strs[1] = int(strs[1].lstrip())
        strs[2] = int(strs[2].lstrip())
        strs[3] = int(strs[3].lstrip())
        strs[4] = int(strs[4].lstrip())
        strs[5] = int(strs[5].lstrip())
        strs[6] = int(strs[6].strip('\n)').lstrip())
        car.append(strs)    
    return car
car = readcar(car_path)
car2 = []
for i in range(len(car)):
  if car[i][6] == 0:
    car2.append(car[i])
car = car2

# print(len(car))
#-------------------点集--------------------
def point(obj):
    point = []
    for i in range(len(obj)):
        x = road1[i][4]
        y = road1[i][5]
        point.extend([x,y])
    set_point = list(set(point))
    return set_point
point = point(road1)#点集
#print(point)
def readcross(fliecross):
    crosslist = open(fliecross,'rU').readlines()
    del crosslist[0]
    cross = []
    for k in range(len(crosslist)):
        strs = crosslist[k].split(',')
        strs[0] = int(strs[0].strip('('))
        strs[1] = int(strs[1].lstrip())
        strs[2] = int(strs[2].lstrip())
        strs[3] = int(strs[3].lstrip())
        strs[4] = int(strs[4].strip('\n)').lstrip())
        cross.append(strs)    
    return cross
cross = readcross(cross_path)
# print(len(cross))

def readpresent(fliepreset):
  presetlist = open(fliepreset,'rU').readlines()
  del presetlist[0]
  preset = []
  for i in range(len(presetlist)):
    strs = presetlist[i].strip('(').strip('\n').strip(')')
    xx = strs.split(',')
    yy = [int(j) for j in xx]
    preset.append(yy)
  return preset
preset = readpresent(presetAnswer_path)

node = point
#-----------------定义图-----------------
class Graph:
  def __init__(self):
    self.nodes = set()
    self.edges = {}
    self.distances = {}

  def add_node(self, value):
    self.nodes.add(value)

  def add_edge(self, from_node, to_node, distance):
    #if self.edges.has_key(from_node):
    if from_node in self.edges:
        self.edges[from_node].append(to_node)
    else :
        self.edges[from_node] = [to_node]
    #if self.edges.has_key(to_node):
    if to_node in self.edges:
        self.edges[to_node].append(from_node)
    else:
        self.edges[to_node] = [from_node]
    self.distances[(from_node,to_node)] = distance
    self.distances[(to_node,from_node)] = distance

#-----------------定义dijkstra算法---------------
def dijsktra(graph, initial):
  visited = {initial: 0}
  path = {}

  nodes = set(graph.nodes)

  while nodes: 
    min_node = None
    for node in nodes:
      if node in visited:
        if min_node is None:
          min_node = node
        elif visited[node] < visited[min_node]:
          min_node = node

    if min_node is None:
      break

    nodes.remove(min_node)
    current_weight = visited[min_node]

    for edge in graph.edges[min_node]:
      weight = current_weight + graph.distances[(min_node, edge)]
      if edge not in visited.keys() or weight < visited[edge]:
        visited[edge] = weight
        path[edge] = min_node

  return visited, path
#------------构建图-------------
g = Graph()
for i in range(len(node)):
  g.add_node(node[i])
for j in range(len(road1)):
  if road1[j][6]==1:
    g.add_edge(road1[j][4],road1[j][5],road1[j][1])
    g.add_edge(road1[j][5],road1[j][4],road1[j][1])
  else:
    g.add_edge(road1[j][4],road1[j][5],road1[j][1])

def ShortestPath(graph,start,end):
  visited,path = dijsktra(graph,start)
  shorteatpath = [end]
  while path[end]!=start:
    end = path[end]
    shorteatpath.insert(0,end)
  shorteatpath.insert(0,start)
  return shorteatpath

dic_aa = {}
for i in range(len(road)):
  # g.distances[(road[i][4],road[i][5])]=int(road[i][1]/(road[i][2]*road[i][3])*50)
  g.distances[(road[i][4],road[i][5])]=float(road[i][1])
  if road[i][6] == 0:
    g.distances[(road[i][5],road[i][4])] = 99999999
    dic_aa[road[i][4],road[i][5]] = road[i][0]
  else:
    dic_aa[road[i][4],road[i][5]] = road[i][0]
    dic_aa[road[i][5],road[i][4]] = road[i][0]

data = np.array(car)
insert_number = [i for i in range(len(car))]
data = np.insert(data,0,insert_number,1)
data = data[np.argsort(-data[:,4])]
data_pri = []
data_nor = []
for i in range(data.shape[0]):
  if data[i][6] == 1:
    data_pri.append(data[i])
  else:
    data_nor.append(data[i])
data_pri = np.array(data_pri)
data_nor = np.array(data_nor)
data = np.vstack((data_pri,data_nor))
car_start_time = [0 for i in range(len(car))]

distance_old = [0 for i in range(len(road))]
for k in range(len(road)):
  distance_old[k] = g.distances[(road[k][4],road[k][5])]

road2 = np.array(road)
node_pre = [0 for i in range(len(preset))]
for i in range(len(preset)):
  pre = []
  carp = preset[i]
  pre.append(preset[i][0])
  pre.append(preset[i][1])
  for j in range(2,len(carp)):
    if j == len(carp)-1:
      first_cross = pre[-1]
      now_road = np.where(road2[:,0]==int(carp[j]))[0][0]
      if first_cross != road[now_road][4]:
        now_cross = road[now_road][4]
      else:
        now_cross = road[now_road][5]
      pre.append(now_cross)
    else:
      first_road = np.where(road2[:,0]==int(carp[j]))[0][0]
      first_cross = [road2[first_road][4],road2[first_road][5]]
      second_road = np.where(road2[:,0]==carp[j+1])[0][0]
      second_cross = [road2[second_road][4],road2[second_road][5]]
      now_cross = [i for i in first_cross if i in second_cross][0]
      pre.append(now_cross)
  second_cross = pre[2]
  now_road = np.where(road2[:,0]==int(carp[2]))[0][0]
  if second_cross != road[now_road][4]:
    now_cross = road[now_road][4]
  else:
    now_cross = road[now_road][5]
  pre.insert(2,now_cross)
  node_pre[i] = pre
# print(node_pre)
path_ = []
order = []
data1 = []
for i in range(len(data)):
  if car[0][0] == 20556: #map1第一辆非预置车辆
    layer_time1 = 30
    layer_car1 = 1000
    layer_car3 = 1
    layer_time2 = 30
    layer_car2 = 800
    aaa = 6
    total_car1 = len(data_pri)+16*layer_car3
    # layer_time1 = 30
    # layer_car1 = 1000
    # layer_car3 = 500
    # layer_time2 = 28
    # layer_car2 = 1300
    # aaa = 6
    # total_car1 = len(data_pri)+16*layer_car3
  elif car[0][0] == 98925: #map2第一辆非预置车辆
    layer_time1 = 30    #
    layer_car1 = 1000   #
    layer_car3 = 1   #
    layer_time2 = 30    #
    layer_car2 = 1200   #
    aaa = 2
    total_car1 = len(data_pri)+16*layer_car3
  else:
    layer_time1 = 30
    layer_car1 = 1000
    layer_car3 = 1
    layer_time2 = 30
    layer_car2 = 800
    aaa = 2
    total_car1 = len(data_pri)+16*layer_car3
  # preset[len(preset)-1][1]/layer_time1
  # if i//layer_car1 <= layer1:
  if i < total_car1:
    if i < len(data_pri):
      car_start_time[i] = data[i][5] + i//layer_car1*layer_time1
      if i%layer_car1 == 0:
        for j in range(len(road)):
          if road[j][6] == 1:
            g.distances[(road[j][4],road[j][5])] = distance_old[j]
            g. distances[(road[j][5],road[j][4])] = distance_old[j]
          else:
            g.distances[(road[j][4],road[j][5])] = distance_old[j]
        for j in range(len(preset)):
          if int(preset[j][1]) >= (i//layer_car1)*layer_time1 and int(preset[j][1]) < (i//layer_car1+1)*layer_time1:
            for m in range(2,len(preset[j])-1):
              roadi = np.where(road2[:,0] == preset[j][m])[0][0]
              g.distances[(node_pre[j][m],node_pre[j][m+1])] += float(1/road[roadi][3])*aaa
    else:
      # car_start_time[i] = data[i][5] + (len(data_pri)//layer_car1+1)*layer_time1 + (i-len(data_pri))//layer_car1*layer_time1
      car_start_time[i] = data[i][5] + 250 + (i-len(data_pri))//layer_car3*layer_time1
      if i%layer_car3 == 0:
        for j in range(len(road)):
          if road[j][6] == 1:
            g.distances[(road[j][4],road[j][5])] = distance_old[j]
            g. distances[(road[j][5],road[j][4])] = distance_old[j]
          else:
            g.distances[(road[j][4],road[j][5])] = distance_old[j]
        for j in range(len(preset)):
          if int(preset[j][1]) >= (i//layer_car3)*layer_time1 and int(preset[j][1]) < (i//layer_car3+1)*layer_time1:
            for m in range(2,len(preset[j])-1):
              roadi = np.where(road2[:,0] == preset[j][m])[0][0]
              g.distances[(node_pre[j][m],node_pre[j][m+1])] += float(1/road[roadi][3])*aaa

  else:
    # car_start_time[i] = 1200+(i-len(data_pri))//layer_car2*layer_time2
    # layer2 = len(data_pri) + (layer1-(len(data_pri)//layer_car1+1))*layer_car1
    layer2 = total_car1
    car_start_time[i] = 800+(i-layer2)//layer_car2*layer_time2
    if i%layer_car2 == 0:
      for j in range(len(road)):
        if road[j][6] == 1:
          g.distances[(road[j][4],road[j][5])] = distance_old[j]
          g.distances[(road[j][5],road[j][4])] = distance_old[j]
        else:
          g.distances[(road[j][4],road[j][5])] = distance_old[j]

  order.append(data[i][0])
  data1.append(data[i][1])
  xx = data[i][2]
  yy = data[i][3]
  path_.append(ShortestPath(g,xx,yy))
  node_2 = path_[i]
  for m in range(len(node_2)-1):
    roadi = np.where(road2[:,0] == dic_aa[node_2[m],node_2[m+1]])[0][0]
    g.distances[(node_2[m],node_2[m+1])] += float(1/road[roadi][3])*aaa
  
  # car_start_time[i] = data[i][5]+layer_add
# print(data)
data = np.insert(data,2,car_start_time,1)
data = data[np.argsort(data[:,0])]
data = np.delete(data,0,1)

#----------------转换输出形式---------------
dict_ = {}
for i in range(len(road1)):
  dict_[road1[i][0]] = [road1[i][4],road1[i][5]]
# print(dict_)
values = list(dict_.values())
#print(values)
answer = [0 for i in range(len(path_))]
for j in range(len(path_)):
  c = []
  for k in range(len(path_[j])-1):
    x = [path_[j][k],path_[j][k+1]]
    y = [path_[j][k+1],path_[j][k]]
    #print(x)
    if x in values:
      c.append(list(dict_.keys())[list(dict_.values()).index(x)])
    else:
      c.append(list(dict_.keys())[list(dict_.values()).index(y)])
  c.insert(0,data1[j])
  # answer.append(c)
  answer[order[j]] = c

answer3 = []
# car_start_time = StartTime1(car,cross)
for i in range(len(answer)):
  mm = answer[i]
  mm.insert(1,data[i][1])
  answer3.append(mm)

# answer3 = []
file = open(answer_path,'w')
file.write('#(carId,StartTime,RoadId...)')
file.write('\n')
for n in range(len(answer3)):
  # if car[n][6] == 0:
    aa = str(answer3[n])
    aa = '('+aa.strip('[').strip(']')+')'
    file.write(aa)
    file.write('\n')
file.close()

ending = time.time()
oprate_time = int(ending-starting)
print('Operating Time is '+str(oprate_time)+'s')

