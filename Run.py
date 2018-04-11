import csv
from collections import deque

import svgwrite
from lxml import etree
import sys

tree = etree.parse('city.osm')
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
with open('listcsv.csv', 'w') as printer:
    out = csv.writer(printer)
    out.writerows(map.items())
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
    l = math.acos(math.sin(float(point1[0])) * math.sin(-1 * float(point2[0])) + math.cos(float(point1[0])) * math.cos(
        -1 * float(point2[0])) * math.cos(abs(float(point1[1]) - float(point2[1]))))
    return l * 6371


# Дейкстра
mapfin = {0: [pointid, 0, -1]}
mapDey = {pointid: 0}
lim = 0
k = 1
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
m0 = {0: [pointid, 0, -1]}
m11 = list()
m12 = list()
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


dist, prev = levit(m2coord, mapCoord, pointid)
lm = 0
m = 1000
for i in hospid:
    if dist[i] < m:
        lim = lm
        m = dist[i]
    lm = +1
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

#A*

# Рисуем
svgGraphA = svgwrite.Drawing('GraphA.svg', size=(str(const) + 'px', str(const) + 'px'))
for dot in map:
    svgGraphA.add(svgGraphA.circle(
        (const - (maxlon - float(mapCoord[dot][1])) / scaleLon, (maxlat - float(mapCoord[dot][0])) / scaleLat), 2))
    for dot2 in map[dot]:
        svgGraphA.add(svgGraphA.circle(
            (const - (maxlon - float(mapCoord[dot2][1])) / scaleLon, (maxlat - float(mapCoord[dot2][0])) / scaleLat),
            2))
        svgGraphA.add(svgGraphA.line(
            (const - (maxlon - float(mapCoord[dot][1])) / scaleLon, (maxlat - float(mapCoord[dot][0])) / scaleLat),
            (const - (maxlon - float(mapCoord[dot2][1])) / scaleLon, (maxlat - float(mapCoord[dot2][0])) / scaleLat),
            stroke=svgwrite.rgb(0, 0, 0, '%')))
    svgGraphA.add(svgGraphA.circle(center=(
        const - (maxlon - float(mapCoord[pointid][1])) / scaleLon, (maxlat - float(mapCoord[pointid][0])) / scaleLat),
        r=15,
        stroke="green", stroke_width=10))
for i in range(len(hospid)):
    if i == lim:
        svgGraphLevit.add(svgGraphA.circle(center=(
            const - (maxlon - float(mapCoord[hospid[i]][1])) / scaleLon,
            (maxlat - float(mapCoord[hospid[i]][0])) / scaleLat), r=15,
            stroke="blue", stroke_width=10))
        l = hospid[i]
        while prev[l] != pointid:
            point = prev[l]
            svgGraphA.add(svgGraphA.polyline(
                ((const - (maxlon - float(mapCoord[point][1])) / scaleLon,
                  (maxlat - float(mapCoord[point][0])) / scaleLat),
                 (const - (maxlon - float(mapCoord[l][1])) / scaleLon,
                  (maxlat - float(mapCoord[l][0])) / scaleLat)),
                stroke="blue", stroke_width=10, fill='none'))
            l = point
    else:
        svgGraphA.add(svgGraphA.circle(center=(
            const - (maxlon - float(mapCoord[hospid[i]][1])) / scaleLon,
            (maxlat - float(mapCoord[hospid[i]][0])) / scaleLat), r=15,
            stroke="red", stroke_width=10))
        l = hospid[i]
        while prev[l] != pointid:
            point = prev[l]
            svgGraphA.add(svgGraphA.polyline((
                (const - (maxlon - float(mapCoord[point][1])) / scaleLon,
                 (maxlat - float(mapCoord[point][0])) / scaleLat),
                (const - (maxlon - float(mapCoord[l][1])) / scaleLon,
                 (maxlat - float(mapCoord[l][0])) / scaleLat)),
                stroke="red", stroke_width=5, fill='none'))
            l = point
svgGraphA.save()
