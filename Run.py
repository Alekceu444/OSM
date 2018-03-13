import csv
import svgwrite
from lxml import etree
tree = etree.parse('city.osm')
#Строим список смежности
map={}
for node in tree.iterfind('/way/tag[@k="highway"]'): # поиск элементов
    if (node.get('v') not in ["path","pedestrian","footway","road","service","track","cycleway"]):
        for nodes in node.iterfind('../tag'):
            if nodes.get('k')=='oneway' and nodes.get('v')=='yes':
                adder=nodes
                for nd in node.iterfind('../nd'):
                    if adder==nodes:
                        adder=nd
                    else:
                        if adder.get('ref') in map:
                            map[adder.get('ref')].add(nd.get('ref'))
                            adder=nd
                        else:
                            map[adder.get('ref')]=set()
                            map[adder.get('ref')].add(nd.get('ref'))
                            adder=nd

            else:
                adder=nodes
                for nd in node.iterfind('../nd'):
                    if adder==nodes:
                        adder=nd
                    else:
                        if (adder.get('ref') in map) and (nd.get('ref') in map):
                            map[adder.get('ref')].add(nd.get('ref'))
                            map[nd.get('ref')].add(adder.get('ref'))
                            adder=nd
                        elif (adder.get('ref') in map) and (nd.get('ref') not in map):
                            map[nd.get('ref')]=set()
                            map[adder.get('ref')].add(nd.get('ref'))
                            map[nd.get('ref')].add(adder.get('ref'))
                            adder=nd
                        elif (adder.get('ref') not in map) and (nd.get('ref') in map):
                            map[adder.get('ref')]=set()
                            map[adder.get('ref')].add(nd.get('ref'))
                            map[nd.get('ref')].add(adder.get('ref'))
                            adder=nd
                        elif (adder.get('ref') not in map) and (nd.get('ref') not in map):
                            map[adder.get('ref')]=set()
                            map[nd.get('ref')]=set()
                            map[adder.get('ref')].add(nd.get('ref'))
                            map[nd.get('ref')].add(adder.get('ref'))
                            adder=nd
with open('listcsv.csv','w') as printer:
    out = csv.writer(printer)
    out.writerows(map.items())
#Строим матрицу смежности
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
        out.writerow([key]+list(arr))
#создаем svg
maxlat=0.0
minlon=180.0
minlat=90.0
maxlon=0.0
mapCoord={}
for node in tree.iterfind('/node'):
    mapCoord[node.get('id')]=list()
    mapCoord[node.get('id')].append(node.get('lat'))
    mapCoord[node.get('id')].append(node.get('lon'))
    if node.get('id') in map:
        if float(node.get('lat'))>maxlat:
            maxlat=float(node.get('lat'))
        if float(node.get('lat'))<minlat:
            minlat=float(node.get('lat'))
        if float(node.get('lon'))>maxlon:
            maxlon=float(node.get('lon'))
        if float(node.get('lon'))<minlon:
            minlon=float(node.get('lon'))
const=3000.0
scaleLat=(maxlat-minlat)/const
scaleLon=(maxlon-minlon)/const
svgGraph = svgwrite.Drawing('Graph.svg', size=(str(const)+'px', str(const)+'px'))
for dot in map:
    if dot not in mapCoord:
        continue
    svgGraph.add(svgGraph.circle((const-(maxlon-float(mapCoord[dot][1]))/scaleLon,(maxlat-float(mapCoord[dot][0]))/scaleLat), 2))
    for dot2 in map[dot]:
        if dot2 not in mapCoord:
            continue
        svgGraph.add(svgGraph.circle((const-(maxlon-float(mapCoord[dot2][1]))/scaleLon, (maxlat-float(mapCoord[dot2][0]))/scaleLat), 2))
        svgGraph.add(svgGraph.line((const-(maxlon-float(mapCoord[dot][1]))/scaleLon,(maxlat-float(mapCoord[dot][0]))/scaleLat),
                                   (const-(maxlon-float(mapCoord[dot2][1]))/scaleLon,(maxlat-float(mapCoord[dot2][0]))/scaleLat),
                                    stroke=svgwrite.rgb(0, 0, 0, '%')))
svgGraph.save()
