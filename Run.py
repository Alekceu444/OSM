import csv
from collections import deque

import svgwrite
from lxml import etree
import time

tree = etree.parse('city.osm')
timeDey=0;
timeLevit=0;
timeACheb=0;
timeAEucl=0;
timeAManh=0;
# Строим список смежности
map = {}
maxlat = 0.0
minlon = 180.0
minlat = 90.0
maxlon = 0.0
mapCoord = {}
for node in tree.iterfind('/node'):
    mapCoord[node.get('id')] = list()
    mapCoord[node.get('id')].append(node.get('lat'))
    mapCoord[node.get('id')].append(node.get('lon'))
for node in tree.iterfind('/way/tag[@k="highway"]'):  # поиск элементов
    if (node.get('v') in ["motorway", "trunk", "primary", "secondary", "tertiary", "unclassified", ]):
        for nodes in node.iterfind('../tag'):
            if nodes.get('k') == 'oneway' and nodes.get('v') == 'yes':
                adder = nodes
                for nd in node.iterfind('../nd'):
                    if nd.get('ref') in mapCoord:
                        if float(mapCoord[nd.get('ref')][0]) > maxlat:
                            maxlat = float(mapCoord[nd.get('ref')][0])
                        if float(mapCoord[nd.get('ref')][0]) < minlat:
                            minlat = float(mapCoord[nd.get('ref')][0])
                        if float(mapCoord[nd.get('ref')][1]) > maxlon:
                            maxlon = float(mapCoord[nd.get('ref')][1])
                        if float(mapCoord[nd.get('ref')][1]) < minlon:
                            minlon = float(mapCoord[nd.get('ref')][1])
                        if adder == nodes:
                            adder = nd
                        else:
                            if adder.get('ref') in map:
                                map[adder.get('ref')].add(nd.get('ref'))
                                adder = nd
                            else:
                                map[adder.get('ref')] = set()
                                map[adder.get('ref')].add(nd.get('ref'))
                                adder = nd

            else:
                adder = nodes
                for nd in node.iterfind('../nd'):
                    if nd.get('ref') in mapCoord:
                        if float(mapCoord[nd.get('ref')][0]) > maxlat:
                            maxlat = float(mapCoord[nd.get('ref')][0])
                        if float(mapCoord[nd.get('ref')][0]) < minlat:
                            minlat = float(mapCoord[nd.get('ref')][0])
                        if float(mapCoord[nd.get('ref')][1]) > maxlon:
                            maxlon = float(mapCoord[nd.get('ref')][1])
                        if float(mapCoord[nd.get('ref')][1]) < minlon:
                            minlon = float(mapCoord[nd.get('ref')][1])
                        if adder == nodes:
                            adder = nd
                        else:
                            if (adder.get('ref') in map) and (nd.get('ref') in map):
                                map[adder.get('ref')].add(nd.get('ref'))
                                map[nd.get('ref')].add(adder.get('ref'))
                                adder = nd
                            elif (adder.get('ref') in map) and (nd.get('ref') not in map):
                                map[nd.get('ref')] = set()
                                map[adder.get('ref')].add(nd.get('ref'))
                                map[nd.get('ref')].add(adder.get('ref'))
                                adder = nd
                            elif (adder.get('ref') not in map) and (nd.get('ref') in map):
                                map[adder.get('ref')] = set()
                                map[adder.get('ref')].add(nd.get('ref'))
                                map[nd.get('ref')].add(adder.get('ref'))
                                adder = nd
                            elif (adder.get('ref') not in map) and (nd.get('ref') not in map):
                                map[adder.get('ref')] = set()
                                map[nd.get('ref')] = set()
                                map[adder.get('ref')].add(nd.get('ref'))
                                map[nd.get('ref')].add(adder.get('ref'))
                                adder = nd
##Вывод матрицы смежности
'''with open('listcsv.csv', 'w') as printer:
    out = csv.writer(printer)
    out.writerows(map.items())'''
'''#Строим матрицу смежности
with open('matrix.csv', 'w') as printer:
    out = csv.writer(printer)
    out.writerow([''] + list(map.keys()))
    for key in map:
        x=0
        arr=list()
        for kiy in map:
            if kiy in map[key]:
                arr.append(1)
            else:
                arr.append(0)
        out.writerow([key]+list(arr))'''
print('Введите координату по lat:')
x = int(input())
print('Введите координату по lon:')
y = int(input())
hospitals = {'Облбольница': [54.9797429, 82.9128925], 'Горбольница': [55.0707814, 82.9312259],
             'Больница №9': [54.94245, 83.1239848], 'Городская клиническая больница №11': [54.983283, 82.8236317],
             'Городская больница 3': [54.8482059, 82.9684241]}
hospid = list()
mapcrd2 = mapCoord.copy()
for i in mapCoord:
    if i not in map:
        del mapcrd2[i]
mapCoord.clear()
mapCoord = mapcrd2.copy()
del mapcrd2
for i in hospitals:
    check = 100.0
    res = 0
    for j in mapCoord:
        if ((float(mapCoord[j][0]) - hospitals[i][0]) ** 2 + (
                float(mapCoord[j][1]) - hospitals[i][1]) ** 2) ** 0.5 < check:
            res = j
            check = ((float(mapCoord[j][0]) - hospitals[i][0]) ** 2 + (
                    float(mapCoord[j][1]) - hospitals[i][1]) ** 2) ** 0.5
    hospid.append(res)
##Находит ближайшие вершины для заданых объектов
'''for i in hospitals:
    latmi=100.0
    lonmi=100.0
    check=100.0
    for j in mapCoord:
        if ((float(mapCoord[j][0])-hospitals[i][0])**2+(float(mapCoord[j][1])-hospitals[i][1])**2)**0.5<check:
            latmi=mapCoord[j][0]
            lonmi=mapCoord[j][1]
            check=((float(mapCoord[j][0])-hospitals[i][0])**2+(float(mapCoord[j][1])-hospitals[i][1])**2)**0.5
    hospitals[i][0]=float(latmi)
    hospitals[i][1]=float(lonmi)
print(hospitals)'''
##поиск ближайшей вершины для введенной точки
pointid = 0
check = 100.0
for j in mapCoord:
    if ((float(mapCoord[j][0]) - x) ** 2 + (float(mapCoord[j][1]) - y) ** 2) ** 0.5 < check:
        pointid = j
        check = ((float(mapCoord[j][0]) - x) ** 2 + (float(mapCoord[j][1]) - y) ** 2) ** 0.5


def distance(point1, point2):
    import math
    l = math.acos(math.sin(float(point1[0])) * math.sin(float(point2[0])) + math.cos(float(point1[0])) * math.cos(
        float(point2[0])) * math.cos(float(point1[1]) - float(point2[1])))
    return l * 6371


# Дейкстра
mapfin = {0: [pointid, 0, -1]}
mapDey = {pointid: 0}
lim = 0
k = 1
starttime=time.time()
while lim != len(mapfin):
    for i in map[mapfin[lim][0]]:
        dist = ((float(mapCoord[mapfin[lim][0]][0]) - float(mapCoord[i][0])) ** 2 + (
                float(mapCoord[mapfin[lim][0]][1]) - float(mapCoord[i][1])) ** 2) ** 0.5
        if i not in mapDey:
            mapDey[i] = k
            mapfin[k] = list()
            mapfin[k] = [i, mapfin[lim][1] + dist, mapfin[lim][0]]
            k += 1
        elif i in mapDey and mapfin[lim][1] + dist < mapfin[mapDey[i]][1]:
            mapfin[mapDey[i]] = [i, mapfin[lim][1] + dist, mapfin[lim][0]]
    lim += 1
mindistance = list()
l = 0
minnum = -1
for i in hospid:
    if i in mapDey:
        mindistance.append(mapfin[mapDey[i]][1])
        if mapfin[mapDey[i]][1] == min(mindistance):
            minnum = l
        l += 1
    else:
        mindistance.append(1000)
        l += 1
distpoint=[55,83]
timeDey=time.time()-starttime;
print("Время дейкстра:",timeDey)
s=[55,83+mindistance[minnum]]
print("Time spend to arrive dey:",distance(distpoint,s)/40)
# создаем svg
const = 3000.0
scaleLat = (maxlat - minlat) / const
scaleLon = (maxlon - minlon) / const
svgGraph = svgwrite.Drawing('Graph.svg', size=(str(const) + 'px', str(const) + 'px'))
for dot in map:
    svgGraph.add(svgGraph.circle(
        (const - (maxlon - float(mapCoord[dot][1])) / scaleLon, (maxlat - float(mapCoord[dot][0])) / scaleLat), 2))
    for dot2 in map[dot]:
        svgGraph.add(svgGraph.circle(
            (const - (maxlon - float(mapCoord[dot2][1])) / scaleLon, (maxlat - float(mapCoord[dot2][0])) / scaleLat),
            2))
        svgGraph.add(svgGraph.line(
            (const - (maxlon - float(mapCoord[dot][1])) / scaleLon, (maxlat - float(mapCoord[dot][0])) / scaleLat),
            (const - (maxlon - float(mapCoord[dot2][1])) / scaleLon, (maxlat - float(mapCoord[dot2][0])) / scaleLat),
            stroke=svgwrite.rgb(0, 0, 0, '%')))
    svgGraph.add(svgGraph.circle(center=(
        const - (maxlon - float(mapCoord[pointid][1])) / scaleLon, (maxlat - float(mapCoord[pointid][0])) / scaleLat),
        r=15,
        stroke="green", stroke_width=10))
for i in range(len(hospid)):
    if i == minnum:
        svgGraph.add(svgGraph.circle(center=(
            const - (maxlon - float(mapCoord[hospid[i]][1])) / scaleLon,
            (maxlat - float(mapCoord[hospid[i]][0])) / scaleLat), r=15,
            stroke="blue", stroke_width=10))
        l = hospid[i]
        g = mapDey[l]
        while int(mapfin[g][2]) != -1:
            point = mapfin[g][2]
            svgGraph.add(svgGraph.polyline(
                ((const - (maxlon - float(mapCoord[point][1])) / scaleLon,
                  (maxlat - float(mapCoord[point][0])) / scaleLat),
                 (const - (maxlon - float(mapCoord[l][1])) / scaleLon,
                  (maxlat - float(mapCoord[l][0])) / scaleLat)),
                stroke="blue", stroke_width=10, fill='none'))
            l = point
            g = mapDey[l]
    else:
        svgGraph.add(svgGraph.circle(center=(
            const - (maxlon - float(mapCoord[hospid[i]][1])) / scaleLon,
            (maxlat - float(mapCoord[hospid[i]][0])) / scaleLat), r=15,
            stroke="red", stroke_width=10))
        l = hospid[i]
        g = mapDey[l]
        while int(mapfin[g][2]) != -1:
            point = mapfin[g][2]
            svgGraph.add(svgGraph.polyline((
                (const - (maxlon - float(mapCoord[point][1])) / scaleLon,
                 (maxlat - float(mapCoord[point][0])) / scaleLat),
                (const - (maxlon - float(mapCoord[l][1])) / scaleLon,
                 (maxlat - float(mapCoord[l][0])) / scaleLat)),
                stroke="red", stroke_width=5, fill='none'))
            l = point
            g = mapDey[l]
svgGraph.save()
# Левита
m2 = list()
m2.append(pointid)
l = 0
k = 0
while l != len(m2):
    for i in map[m2[l]]:
        if i not in m2:
            m2.append(i)
    l += 1
m2coord = {}
for i in m2:
    m2coord[i] = list()
    m2coord[i] = map[i].copy()

def levit(m2, mapCoord, start):
    dist = {k: None for k in mapCoord.keys()}
    dist[start] = 0
    prev = {}
    queue = deque([start])
    id = {k: 0 for k in mapCoord.keys()}
    while queue:
        v = queue.popleft()
        id[v] = 1
        for successor in m2[v]:
            new_dist = float(dist[v]) + ((float(mapCoord[v][1]) - float(mapCoord[successor][1])) ** 2 + (
                    float(mapCoord[v][0]) - float(mapCoord[successor][0])) ** 2) ** 1 / 2
            if dist[successor] is None or new_dist < dist[successor]:
                dist[successor] = new_dist
                if id[successor] == 0:
                    queue.append(successor)
                elif id[successor] == 1:
                    queue.appendleft(successor)
                prev[successor] = v
                id[successor] = 1
    return dist, prev

starttime=time.time()
dist, prev = levit(m2coord, mapCoord, pointid)
lm = 0
m = 1000
for i in hospid:
    if dist[i] < m:
        lim = lm
        m = dist[i]
    lm = +1
timeLevit=time.time()-starttime
print("Время левита:",timeLevit)
s=[55,83+m]
print("Time spend to arrive levit:",distance(distpoint,s)/40)
# Рисуем
svgGraphLevit = svgwrite.Drawing('GraphLevit.svg', size=(str(const) + 'px', str(const) + 'px'))
for dot in map:
    svgGraphLevit.add(svgGraphLevit.circle(
        (const - (maxlon - float(mapCoord[dot][1])) / scaleLon, (maxlat - float(mapCoord[dot][0])) / scaleLat), 2))
    for dot2 in map[dot]:
        svgGraphLevit.add(svgGraphLevit.circle(
            (const - (maxlon - float(mapCoord[dot2][1])) / scaleLon, (maxlat - float(mapCoord[dot2][0])) / scaleLat),
            2))
        svgGraphLevit.add(svgGraphLevit.line(
            (const - (maxlon - float(mapCoord[dot][1])) / scaleLon, (maxlat - float(mapCoord[dot][0])) / scaleLat),
            (const - (maxlon - float(mapCoord[dot2][1])) / scaleLon, (maxlat - float(mapCoord[dot2][0])) / scaleLat),
            stroke=svgwrite.rgb(0, 0, 0, '%')))
    svgGraphLevit.add(svgGraphLevit.circle(center=(
        const - (maxlon - float(mapCoord[pointid][1])) / scaleLon, (maxlat - float(mapCoord[pointid][0])) / scaleLat),
        r=15,
        stroke="green", stroke_width=10))
for i in range(len(hospid)):
    if i == lim:
        svgGraphLevit.add(svgGraphLevit.circle(center=(
            const - (maxlon - float(mapCoord[hospid[i]][1])) / scaleLon,
            (maxlat - float(mapCoord[hospid[i]][0])) / scaleLat), r=15,
            stroke="blue", stroke_width=10))
        l = hospid[i]
        while prev[l] != pointid:
            point = prev[l]
            svgGraphLevit.add(svgGraphLevit.polyline(
                ((const - (maxlon - float(mapCoord[point][1])) / scaleLon,
                  (maxlat - float(mapCoord[point][0])) / scaleLat),
                 (const - (maxlon - float(mapCoord[l][1])) / scaleLon,
                  (maxlat - float(mapCoord[l][0])) / scaleLat)),
                stroke="blue", stroke_width=10, fill='none'))
            l = point
    else:
        svgGraphLevit.add(svgGraphLevit.circle(center=(
            const - (maxlon - float(mapCoord[hospid[i]][1])) / scaleLon,
            (maxlat - float(mapCoord[hospid[i]][0])) / scaleLat), r=15,
            stroke="red", stroke_width=10))
        l = hospid[i]
        while prev[l] != pointid:
            point = prev[l]
            svgGraphLevit.add(svgGraphLevit.polyline((
                (const - (maxlon - float(mapCoord[point][1])) / scaleLon,
                 (maxlat - float(mapCoord[point][0])) / scaleLat),
                (const - (maxlon - float(mapCoord[l][1])) / scaleLon,
                 (maxlat - float(mapCoord[l][0])) / scaleLat)),
                stroke="red", stroke_width=5, fill='none'))
            l = point
svgGraphLevit.save()


# A*
def euclidean(first, second):
    return ((float(first[0]) - float(second[0])) ** 2 + (float(first[1]) - float(second[1])) ** 2) ** (1 / 2)


def manhattan(first, second):
    return abs(float(first[0]) - float(second[0])) + abs(float(first[1]) - float(second[1]))


def chebyshev(first, second):
    return max(abs(float(first[0]) - float(second[0])), abs(float(first[0]) - float(second[0])))


def a(start, end, list, mapCoord, heuristic='euclidean'):
    heurFunc = euclidean
    if heuristic == 'chebyshev':
        heurFunc = chebyshev
    elif heuristic == 'manhattan':
        heurFunc = manhattan
    open = []
    closed = []
    g = 0
    f = heurFunc(mapCoord[start], mapCoord[end])
    from heapq import heappush, heappop
    heappush(open, (f, g, [start]))
    while open:
        heap = heappop(open)
        p = heap[-1]
        g = heap[1]
        x = p[-1]

        if x in closed:
            continue

        if x == end:
            return f, p

        closed.append(x)

        if not list.get(x):
            continue

        for successor in list[x]:
            newg = g + euclidean(mapCoord[successor], mapCoord[x])
            newf = newg + heurFunc(mapCoord[successor], mapCoord[end])

            newPath = p[:]
            newPath.append(successor)

            heappush(open, (newf, newg, newPath))

    return {k: 100000 for k in mapCoord.keys()}, {}

#Manhattan
minrange = 1000
h = []
l = 0
lim = -1
starttime=time.time()
for i in hospid:
    f, aj = a(pointid, i, m2coord, mapCoord,'manhattan')
    h = h + aj
    if f < minrange:
        lim = l
        minrange = f
    l += 1
timeAManh=time.time()-starttime
print("Время A* манхет:", timeAManh)
s=[55,83+minrange]
print("Time spend to arrive Amanh:",distance(distpoint,s)/40)
# Рисуем
svgGraphAManh = svgwrite.Drawing('GraphAManh.svg', size=(str(const) + 'px', str(const) + 'px'))
for dot in map:
    svgGraphAManh.add(svgGraphAManh.circle(
        (const - (maxlon - float(mapCoord[dot][1])) / scaleLon, (maxlat - float(mapCoord[dot][0])) / scaleLat), 2))
    for dot2 in map[dot]:
        svgGraphAManh.add(svgGraphAManh.circle(
            (const - (maxlon - float(mapCoord[dot2][1])) / scaleLon, (maxlat - float(mapCoord[dot2][0])) / scaleLat),
            2))
        svgGraphAManh.add(svgGraphAManh.line(
            (const - (maxlon - float(mapCoord[dot][1])) / scaleLon, (maxlat - float(mapCoord[dot][0])) / scaleLat),
            (const - (maxlon - float(mapCoord[dot2][1])) / scaleLon, (maxlat - float(mapCoord[dot2][0])) / scaleLat),
            stroke=svgwrite.rgb(0, 0, 0, '%')))
    svgGraphAManh.add(svgGraphAManh.circle(center=(
        const - (maxlon - float(mapCoord[pointid][1])) / scaleLon, (maxlat - float(mapCoord[pointid][0])) / scaleLat),
        r=15,
        stroke="green", stroke_width=10))
k = 0
for i in range(len(hospid)):
    if i == lim:
        svgGraphAManh.add(svgGraphAManh.circle(center=(
            const - (maxlon - float(mapCoord[hospid[i]][1])) / scaleLon,
            (maxlat - float(mapCoord[hospid[i]][0])) / scaleLat), r=15,
            stroke="blue", stroke_width=10))
        l = pointid
        while h[k] != hospid[i]:
            point = h[k]
            svgGraphAManh.add(svgGraphAManh.polyline(
                ((const - (maxlon - float(mapCoord[point][1])) / scaleLon,
                  (maxlat - float(mapCoord[point][0])) / scaleLat),
                 (const - (maxlon - float(mapCoord[l][1])) / scaleLon,
                  (maxlat - float(mapCoord[l][0])) / scaleLat)),
                stroke="blue", stroke_width=10, fill='none'))
            l = point
            k += 1
        k += 1
    else:
        svgGraphAManh.add(svgGraphAManh.circle(center=(
            const - (maxlon - float(mapCoord[hospid[i]][1])) / scaleLon,
            (maxlat - float(mapCoord[hospid[i]][0])) / scaleLat), r=15,
            stroke="red", stroke_width=10))
        l = pointid
        while h[k] != hospid[i]:
            point = h[k]
            svgGraphAManh.add(svgGraphAManh.polyline((
                (const - (maxlon - float(mapCoord[point][1])) / scaleLon,
                 (maxlat - float(mapCoord[point][0])) / scaleLat),
                (const - (maxlon - float(mapCoord[l][1])) / scaleLon,
                 (maxlat - float(mapCoord[l][0])) / scaleLat)),
                stroke="red", stroke_width=5, fill='none'))
            l = point
            k += 1
        k += 1
svgGraphAManh.save()

#Euclide
minrange = 1000
h = []
l = 0
lim = -1
starttime=time.time()
for i in hospid:
    f, aj = a(pointid, i, m2coord, mapCoord)
    h = h + aj
    if f < minrange:
        lim = l
        minrange = f
    l += 1
timeAEucl=time.time()-starttime
print("Время A* евкл:", timeAEucl)
s=[55,83+minrange]
print("Time spend to arrive AEucl:",distance(distpoint,s)/40)
# Рисуем
svgGraphAEucl = svgwrite.Drawing('GraphAEucl.svg', size=(str(const) + 'px', str(const) + 'px'))
for dot in map:
    svgGraphAEucl.add(svgGraphAEucl.circle(
        (const - (maxlon - float(mapCoord[dot][1])) / scaleLon, (maxlat - float(mapCoord[dot][0])) / scaleLat), 2))
    for dot2 in map[dot]:
        svgGraphAEucl.add(svgGraphAEucl.circle(
            (const - (maxlon - float(mapCoord[dot2][1])) / scaleLon, (maxlat - float(mapCoord[dot2][0])) / scaleLat),
            2))
        svgGraphAEucl.add(svgGraphAEucl.line(
            (const - (maxlon - float(mapCoord[dot][1])) / scaleLon, (maxlat - float(mapCoord[dot][0])) / scaleLat),
            (const - (maxlon - float(mapCoord[dot2][1])) / scaleLon, (maxlat - float(mapCoord[dot2][0])) / scaleLat),
            stroke=svgwrite.rgb(0, 0, 0, '%')))
    svgGraphAEucl.add(svgGraphAEucl.circle(center=(
        const - (maxlon - float(mapCoord[pointid][1])) / scaleLon, (maxlat - float(mapCoord[pointid][0])) / scaleLat),
        r=15,
        stroke="green", stroke_width=10))
k = 0
for i in range(len(hospid)):
    if i == lim:
        svgGraphAEucl.add(svgGraphAEucl.circle(center=(
            const - (maxlon - float(mapCoord[hospid[i]][1])) / scaleLon,
            (maxlat - float(mapCoord[hospid[i]][0])) / scaleLat), r=15,
            stroke="blue", stroke_width=10))
        l = pointid
        while h[k] != hospid[i]:
            point = h[k]
            svgGraphAEucl.add(svgGraphAEucl.polyline(
                ((const - (maxlon - float(mapCoord[point][1])) / scaleLon,
                  (maxlat - float(mapCoord[point][0])) / scaleLat),
                 (const - (maxlon - float(mapCoord[l][1])) / scaleLon,
                  (maxlat - float(mapCoord[l][0])) / scaleLat)),
                stroke="blue", stroke_width=10, fill='none'))
            l = point
            k += 1
        k += 1
    else:
        svgGraphAEucl.add(svgGraphAEucl.circle(center=(
            const - (maxlon - float(mapCoord[hospid[i]][1])) / scaleLon,
            (maxlat - float(mapCoord[hospid[i]][0])) / scaleLat), r=15,
            stroke="red", stroke_width=10))
        l = pointid
        while h[k] != hospid[i]:
            point = h[k]
            svgGraphAEucl.add(svgGraphAEucl.polyline((
                (const - (maxlon - float(mapCoord[point][1])) / scaleLon,
                 (maxlat - float(mapCoord[point][0])) / scaleLat),
                (const - (maxlon - float(mapCoord[l][1])) / scaleLon,
                 (maxlat - float(mapCoord[l][0])) / scaleLat)),
                stroke="red", stroke_width=5, fill='none'))
            l = point
            k += 1
        k += 1
svgGraphAEucl.save()


#Chebyshev
minrange = 1000
h = []
l = 0
lim = -1
starttime=time.time()
for i in hospid:
    f, aj = a(pointid, i, m2coord, mapCoord)
    h = h + aj
    if f < minrange:
        lim = l
        minrange = f
    l += 1
timeACheb=time.time()-starttime
print("Время A* чебыш:", timeACheb)
s=[55,83+minrange]
print("Time spend to arrive ACheb:",distance(distpoint,s)/40)
# Рисуем
svgGraphACheb = svgwrite.Drawing('GraphACheb.svg', size=(str(const) + 'px', str(const) + 'px'))
for dot in map:
    svgGraphACheb.add(svgGraphACheb.circle(
        (const - (maxlon - float(mapCoord[dot][1])) / scaleLon, (maxlat - float(mapCoord[dot][0])) / scaleLat), 2))
    for dot2 in map[dot]:
        svgGraphACheb.add(svgGraphACheb.circle(
            (const - (maxlon - float(mapCoord[dot2][1])) / scaleLon, (maxlat - float(mapCoord[dot2][0])) / scaleLat),
            2))
        svgGraphACheb.add(svgGraphACheb.line(
            (const - (maxlon - float(mapCoord[dot][1])) / scaleLon, (maxlat - float(mapCoord[dot][0])) / scaleLat),
            (const - (maxlon - float(mapCoord[dot2][1])) / scaleLon, (maxlat - float(mapCoord[dot2][0])) / scaleLat),
            stroke=svgwrite.rgb(0, 0, 0, '%')))
    svgGraphACheb.add(svgGraphACheb.circle(center=(
        const - (maxlon - float(mapCoord[pointid][1])) / scaleLon, (maxlat - float(mapCoord[pointid][0])) / scaleLat),
        r=15,
        stroke="green", stroke_width=10))
k = 0
for i in range(len(hospid)):
    if i == lim:
        svgGraphACheb.add(svgGraphACheb.circle(center=(
            const - (maxlon - float(mapCoord[hospid[i]][1])) / scaleLon,
            (maxlat - float(mapCoord[hospid[i]][0])) / scaleLat), r=15,
            stroke="blue", stroke_width=10))
        l = pointid
        while h[k] != hospid[i]:
            point = h[k]
            svgGraphACheb.add(svgGraphACheb.polyline(
                ((const - (maxlon - float(mapCoord[point][1])) / scaleLon,
                  (maxlat - float(mapCoord[point][0])) / scaleLat),
                 (const - (maxlon - float(mapCoord[l][1])) / scaleLon,
                  (maxlat - float(mapCoord[l][0])) / scaleLat)),
                stroke="blue", stroke_width=10, fill='none'))
            l = point
            k += 1
        k += 1
    else:
        svgGraphACheb.add(svgGraphACheb.circle(center=(
            const - (maxlon - float(mapCoord[hospid[i]][1])) / scaleLon,
            (maxlat - float(mapCoord[hospid[i]][0])) / scaleLat), r=15,
            stroke="red", stroke_width=10))
        l = pointid
        while h[k] != hospid[i]:
            point = h[k]
            svgGraphACheb.add(svgGraphACheb.polyline((
                (const - (maxlon - float(mapCoord[point][1])) / scaleLon,
                 (maxlat - float(mapCoord[point][0])) / scaleLat),
                (const - (maxlon - float(mapCoord[l][1])) / scaleLon,
                 (maxlat - float(mapCoord[l][0])) / scaleLat)),
                stroke="red", stroke_width=5, fill='none'))
            l = point
            k += 1
        k += 1
svgGraphACheb.save()
