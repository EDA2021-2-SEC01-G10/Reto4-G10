"""
 * Copyright 2020, Departamento de sistemas y Computación,
 * Universidad de Los Andes
 *
 *
 * Desarrolado para el curso ISIS1225 - Estructuras de Datos y Algoritmos
 *
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along withthis program.  If not, see <http://www.gnu.org/licenses/>.
 *
 * Contribuciones:
 *
 * Dario Correal - Version inicial
 """


from math import asin, cos, radians, sin, sqrt
import config as cf
from DISClib.ADT import list as lt
from DISClib.ADT import map as mp
from DISClib.ADT import orderedmap as om
from DISClib.DataStructures import mapentry as me
from DISClib.Algorithms.Sorting import mergesort as ms
from DISClib.Algorithms.Sorting import shellsort as sa
from DISClib.ADT.graph import gr, indegree, vertices
from DISClib.Algorithms.Graphs import scc
from DISClib.Algorithms.Graphs import dijsktra as dij
from DISClib.Algorithms.Graphs import dfs
from DISClib.Algorithms.Graphs import prim
from DISClib.ADT import queue as qu
from DISClib.ADT import stack as st
import DISClib.Algorithms.Graphs.prim as pr
assert cf

"""
Se define la estructura de un catálogo de videos. El catálogo tendrá dos listas, una para los videos, otra para las categorias de
los mismos.
"""

# Construccion de modelos

def newAnalyzer():

    analyzer = {"airports":None ,"airportsLt":None,"airportsCity":None ,"rutas":None, "cities":None,"citiesLt":None,"directed":None, "undirected": None}   
    analyzer["airports"]=mp.newMap(comparefunction=None) 
    analyzer["cities"]=mp.newMap(comparefunction=None)
    analyzer["airportsCity"]=mp.newMap(comparefunction=None)
    analyzer["airportsLt"]=lt.newList(datastructure="ARRAY_LIST",cmpfunction=None)
    analyzer["citiesLt"]=lt.newList(datastructure="ARRAY_LIST",cmpfunction=None)
    analyzer["rutas"]=lt.newList(datastructure="ARRAY_LIST",cmpfunction=None)

    analyzer["directed"] = gr.newGraph(datastructure="ADJ_LIST",
                            directed = True,
                            size=10,
                            comparefunction=None)

    analyzer["undirected"] = gr.newGraph(datastructure="ADJ_LIST",
                                directed = False, 
                                size=10,
                                comparefunction=None)

    return analyzer

# Funciones para agregar informacion al catalogo

def addAirport(cat, airport):
    iata = airport["IATA"] 
    mp.put(cat["airports"], iata, airport)
    lt.addLast(cat["airportsLt"],airport)
    if not gr.containsVertex(cat["directed"], iata):
       gr.insertVertex(cat["directed"], iata)
       gr.insertVertex(cat["undirected"], iata) 

def addRout(cat,route):
    lt.addLast(cat["rutas"],route)

def addRouteDirected(cat, route):
    departure = route["Departure"]
    destination = route["Destination"]
    distance_km = float(route['distance_km'])
    gr.addEdge(cat["directed"], departure, destination,distance_km)
    

   
def addRouteUndirected(cat,route):
    departureUn = route["Departure"]
    destinationUn = route["Destination"]
    distance_kmUn = float(route['distance_km'])
    tuplaIn=(departureUn,destinationUn)
    tuplaInvert=(destinationUn,departureUn) 
    rutas=cat["rutas"]
    for rut in lt.iterator(rutas):
        departureRuta = rut["Departure"]
        destinationRuta = rut["Destination"]
        tupla=(departureRuta,destinationRuta)
        if tupla== tuplaInvert:
           if gr.getEdge(cat["undirected"], departureUn, destinationUn) == None:  
                gr.addEdge(cat["undirected"], departureUn, destinationUn,distance_kmUn)  
                break
             

def addCity(cat, city):
    id=city["id"]
    mp.put(cat["cities"],id,city)
    lt.addLast(cat["citiesLt"],city)

# Funciones de consulta
def masConectados(cat): 
    maxConexiones=lt.newList(datastructure="ARRAY_LIST",cmpfunction=cmpConexiones)
    graph=cat["directed"]
    vertices=gr.vertices(graph)
    for vertice in lt.iterator(vertices):
        entran=gr.outdegree(graph,vertice)
        salen=gr.indegree(graph,vertice)
        conexiones=entran+salen
        info=[conexiones,vertice]
        if conexiones >0: 
           lt.addLast(maxConexiones,info) 
    sa.sort(maxConexiones,cmpConexiones)      
    return maxConexiones     

def top(listMasConectados,cat): 
    top=lt.newList(datastructure="ARRAY_LIST")
    mapAeropuertos=cat["airports"]
    for vertice in lt.iterator(listMasConectados):
        iata=vertice[1]
        valor=mp.get(mapAeropuertos,iata)["value"]
        lt.addLast(top,valor)
    return top 

def calcularClusteres(cat,iata1,iata2):
    graph=cat["directed"]
    sccRet=scc.KosarajuSCC(graph)
    numeroClusteres=scc.connectedComponents(sccRet)
    compartenCluster=scc.stronglyConnected(sccRet,iata1,iata2)
    return (numeroClusteres,compartenCluster) 

def listarOrigen(cat, origen): 
    listOrigen=lt.newList(datastructure="ARRAY_LIST")
    ciudades=cat["citiesLt"]
    for ciudad in lt.iterator(ciudades):
        nombre=ciudad["city_ascii"]
        if nombre.lower() == origen:
           lt.addLast(listOrigen,ciudad)     
    return listOrigen

def listarDestino(cat,destino):
    listDestino=lt.newList(datastructure="ARRAY_LIST")
    ciudades=cat["citiesLt"]
    for ciudad in lt.iterator(ciudades):
        nombre=ciudad["city_ascii"]
        if nombre.lower() == destino:
           lt.addLast(listDestino,ciudad)     
    return listDestino   

def buscarAeropuertoOrigen(cat,ciudadOrigen):
    aeropuertoReturn=""
    distancias=mp.newMap()
    nombre=ciudadOrigen["city_ascii"].lower()
    pais=ciudadOrigen["country"].lower()
    lat=float(ciudadOrigen["lat"])
    lon=float(ciudadOrigen["lng"])
    aeropuertos=cat["airportsLt"] 
    for aeropuerto in lt.iterator(aeropuertos):
        if aeropuerto["City"].lower() == nombre and aeropuerto["Country"].lower() == pais: 
           iata=aeropuerto["IATA"] 
           latitudAr= float(aeropuerto["Latitude"] )
           longitudAr=float(aeropuerto["Longitude"]) 
           distancia=heversine(lat,lon,latitudAr,longitudAr)
           if not mp.contains(distancias,iata):
               mp.put(distancias,iata,distancia)
        elif aeropuerto["Country"].lower() == pais: 
             iata=aeropuerto["IATA"] 
             latitudAr= float(aeropuerto["Latitude"] )
             longitudAr=float(aeropuerto["Longitude"]) 
             distancia=heversine(lat,lon,latitudAr,longitudAr)
             if not mp.contains(distancias,iata):
                mp.put(distancias,iata,distancia)  
    disNums=mp.valueSet(distancias)
    lista=[]
    for num in lt.iterator(disNums):
        lista.append(num)
    distanciaMinima=min(lista)    
    diskeys=mp.keySet(distancias)
    for key in lt.iterator(diskeys):
        valor=mp.get(distancias,key)["value"]
        if valor == distanciaMinima:
           aeropuertoReturn=key                                       
    return (aeropuertoReturn,distanciaMinima)    

def buscarAeropuertoDestino(cat,ciudadDestino):
    aeropuertoReturn=""
    distancias=mp.newMap()
    nombre=ciudadDestino["city_ascii"].lower()
    pais=ciudadDestino["country"].lower()
    lat=float(ciudadDestino["lat"])
    lon=float(ciudadDestino["lng"])
    aeropuertos=cat["airportsLt"] 
    for aeropuerto in lt.iterator(aeropuertos):
        if aeropuerto["City"].lower() == nombre and aeropuerto["Country"].lower() == pais: 
           iata=aeropuerto["IATA"] 
           latitudAr= float(aeropuerto["Latitude"] )
           longitudAr=float(aeropuerto["Longitude"]) 
           distancia=heversine(lat,lon,latitudAr,longitudAr)
           if not mp.contains(distancias,iata):
               mp.put(distancias,iata,distancia)
        elif aeropuerto["Country"].lower() == pais: 
             iata=aeropuerto["IATA"] 
             latitudAr= float(aeropuerto["Latitude"] )
             longitudAr=float(aeropuerto["Longitude"]) 
             distancia=heversine(lat,lon,latitudAr,longitudAr)
             if not mp.contains(distancias,iata):
                mp.put(distancias,iata,distancia)  
                
    disNums=mp.valueSet(distancias)
    lista=[]
    for num in lt.iterator(disNums):
        lista.append(num)
    distanciaMinima=min(lista)    
    diskeys=mp.keySet(distancias)
    for key in lt.iterator(diskeys):
        valor=mp.get(distancias,key)["value"]
        if valor == distanciaMinima:
           aeropuertoReturn=key                                       
    return (aeropuertoReturn,distanciaMinima)    

def heversine(lat1,lon1,lat2,lon2):
    dlon = radians(lon2 - lon1) 
    dlat = radians(lat2 - lat1) 
    lat1=radians(lat1)
    lat2=radians(lat2)
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a)) 
    return c * 6371

def distanciaVuelo(cat,origen,destino):
    grafo=cat["directed"]
    s=dij.Dijkstra(grafo,origen)
    dis=dij.distTo(s,destino)
    return dis    
    
# Funciones utilizadas para comparar elementos dentro de una lista
def cmpConexiones (vertice1,vertice2):
    return vertice1[0] > vertice2[0] 


def efecto_ac(cat, aeropuerto):

    graph = cat["directed"]
    iatas = gr.adjacents(graph, aeropuerto)
    airports = cat["airports"]
    result = lt.newList()

    lt.addLast(result, lt.size(iatas))
    list1 = lt.newList()

    for x in lt.iterator(iatas):
        dupla = mp.get(airports, x)
        airport = me.getValue(dupla)
        lt.addLast(list1, airport)

    lt.addLast(result, list1)
    return result

def millas_viajero(cat, origen):

    listOrigen=lt.newList(datastructure="ARRAY_LIST")
    undirected = cat["undirected"]
    cities = cat["citiesLt"]
    cities_origin = None
    for city in lt.iterator(cities):
        nombre=city["city_ascii"].lower()
        if nombre == origen.lower():
           lt.addLast(listOrigen,city)   

    cities_origin=listOrigen       
    

    if lt.size(cities_origin) > 1:
        ID1 = mismas_ciudades(cities_origin)
        city1 = mp.get(cat["citiesLt"], ID1)["value"]

    else:
        ID1 = lt.firstElement(cities_origin)["id"]
        city1 = mp.get(cat["airportsLt"], ID1)["value"]
    
    airport1 = aeropuertos_cercanos(cat, city1)["IATA"]

    search = prim.PrimMST(undirected)
    prim.edgesMST(undirected, search)
    path = search['mst']
    nodos = lt.newList()
    large = 0
    final = None
    peso = prim.weightMST(undirected, search)

    while not qu.isEmpty(path):
        edge = qu.dequeue(path)
        lt.addLast(nodos, edge["vertexB"])
    
    cantidad = lt.size(nodos)

    h = dfs.DepthFirstSearch(undirected, airport1)
    for x in lt.iterator(nodos):

        if dfs.hasPathTo(h, x):
            p = dfs.pathTo(h, x)

            if st.size(p) > large:
                large = st.size(p)
                final = p
    return final, peso, cantidad, airport1


def mismas_ciudades(list1):

    print("Origenes probables: ")
    x=list(lt.iterator(list1))
    for i in range(0,len(x)):
        print("")
        print(str(i+1)+")ID: " + x[i]['id'] + " Nombre: " + x[i]["city_ascii"] + " Latitud: " + x[i]["lat"] + " Longitud: " + x[i]["lng"] 
                                                                    + " Pais: " + x[i]["country"] + " Subregion: " + x[i]['admin_name'])                            
    id1 = input('Escoja la ciudad de origen deseada (ingrese el ID de la ciudad): ')
    ciudad=list(lt.iterator(list1))[id-1]
    return ciudad 

def aeropuertos_cercanos(analyzer, ciudad):

    airports = lt.newList()
    airport1 = om.values(analyzer['latlng'],(float(ciudad["lat"]) - 1), (float(ciudad["lat"]) + 1))

    for x in lt.iterator(airport1):

        lists = om.values(x, (float(ciudad["lng"]) - 1), (float(ciudad["lng"]) + 1))

        for y in lt.iterator(lists):
            size = lt.size(y)
            z = 0

            while z < size:
                i = lt.removeLast(y)
                lt.addLast(airports,i)
                z += 1
                
    distance1 = lt.newList()

    for x in lt.iterator(airports):
        latitud = float(x['Latitude'])
        longitud = float(x['Longitude'])
        d1 = distancia_en_c(float(ciudad["lng"]),(float(ciudad["lat"])),longitud,latitud)
        lt.addLast(distance1,d1)

    ms.sort(distance1, ordena)

    dist1 = lt.firstElement(distance1)

    for a1 in lt.iterator(airports):

        lat1 = float(a1['Latitude'])
        lon1 = float(a1['Longitude'])
        d1 = distancia_en_c(float(ciudad["lng"]),(float(ciudad["lat"])),lon1,lat1)

        if d1 == dist1:
            air1 = a1
            break

    return air1


def distancia_en_c(lon1, lat1, lon2, lat2):

    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

    lon_t = lon2 - lon1 
    lat_t = lat2 - lat1 

    a = sin(lat_t/2)**2 + cos(lat1) * cos(lat2) * sin(lon_t/2)**2
    c = 2 * asin(sqrt(a)) 
    dist = c * 6371

    return  dist

def ordena(x, y):
    if (x > y):
        return 0
    return -1