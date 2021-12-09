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


import config as cf
from DISClib.ADT import list as lt
from DISClib.ADT import map as mp
from DISClib.ADT import orderedmap as om
from DISClib.DataStructures import mapentry as me
from DISClib.Algorithms.Sorting import shellsort as sa
from DISClib.ADT.graph import gr, indegree, vertices
from DISClib.Algorithms.Graphs import scc
from DISClib.Algorithms.Graphs import dijsktra as dij
from DISClib.Algorithms.Graphs import dfs
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
    distance_km = route['distance_km']
    gr.addEdge(cat["directed"], departure, destination,distance_km)
    

   
def addRouteUndirected(cat,route):
    departureUn = route["Departure"]
    destinationUn = route["Destination"]
    distance_kmUn = route['distance_km']
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
    aeropuertoAscii=""
    nombre=ciudadOrigen["city_ascii"].lower()
    pais=ciudadOrigen["country"].lower()
    lat=ciudadOrigen["lat"]
    lon=ciudadOrigen["lng"]
    aeropuertos=cat["airportsLt"] 
    for aeropuerto in lt.iterator(aeropuertos):
        if aeropuerto["City"].lower() == nombre and aeropuerto["Country"].lower() == pais: 
           latitudAr= aeropuerto["Latitude"] 
           longitudAr=aeropuerto["Longitude"] 
           encontrado = False 
           while encontrado == False :
                 var=100
                 if lon <= longitudAr <= lon+var and lat <= latitudAr <= lat+var :
                    aeropuertoAscii=""
                    encontrado = True
                 else:   
                      encontrado = False
                      var+=100
                      
    return aeropuertoAscii          

# Funciones utilizadas para comparar elementos dentro de una lista
def cmpConexiones (vertice1,vertice2):
    return vertice1[0] > vertice2[0] 


