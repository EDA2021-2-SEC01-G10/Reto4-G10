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
from DISClib.ADT.graph import gr, indegree
from DISClib.Algorithms.Graphs import dijsktra as dij
from DISClib.Algorithms.Graphs import dfs
assert cf

"""
Se define la estructura de un catálogo de videos. El catálogo tendrá dos listas, una para los videos, otra para las categorias de
los mismos.
"""

# Construccion de modelos

def crearCatalogo():

    catalog = {"directed":None, "airports": None,}

    catalog["directed"] = gr.newGraph(datastructure="ADJ_LIST",
    directed = True,
    size=14000, 
    comparefunction=None)

    catalog["undirected"] = gr.newGraph(datastructure="ADJ_LIST",
    directed = False,
    size=14000, 
    comparefunction=None)

    catalog["airports"] = mp.newMap()
    catalog["cities"] = mp.newMap()
    catalog["lat_long"] = mp.newMap()

    return catalog
def addAirport(catalog, airport):

    iata = airport["IATA"]
    mp.put(catalog["airports"], iata, airport)

    if not gr.containsVertex(catalog["directed"], iata):
        gr.insertVertex(catalog["directed"], iata)

    ordemap = catalog["lat_long"]
    long = float(airport["Latitude"])
    lat = float(airport["Latitude"])
    exist_latitude = om.contains(ordemap, lat)

    if exist_latitude:
        dupla = om.get(ordemap, lat)
        orde2 = me.getValue(dupla)
        exist_latitude = om.contains(orde2, long)
        
        if exist_latitude:
            dupla2 = om.get(orde2, long)
            list1 = me.getValue(dupla2)

        else:
            list1 = lt.newList()

        lt.addLast(list1, airport)
        om.put(orde2, long, list1)

    else:
        orde2 = lt.newList()
        list1 = lt.newList()
        lt.addLast(list1, airport)
        om.put(orde2, long, list1)
        om.put(ordemap, lat, orde2)
    
    return catalog


# Funciones para agregar informacion al catalogo

# Funciones para creacion de datos

# Funciones de consulta

# Funciones utilizadas para comparar elementos dentro de una lista

# Funciones de ordenamiento
