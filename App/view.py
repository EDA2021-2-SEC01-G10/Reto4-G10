"""
 * Copyright 2020, Departamento de sistemas y Computación, Universidad
 * de Los Andes
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
 """

from math import tan
import config as cf
import sys
import controller
from DISClib.ADT import list as lt
from DISClib.ADT import map as mp
from DISClib.DataStructures import mapentry as me
from DISClib.ADT import stack as st
from DISClib.Algorithms.Sorting import shellsort as sa
from DISClib.ADT import orderedmap as om
from DISClib.ADT.graph import gr
import DISClib.Algorithms.Graphs.prim as pr
assert cf


"""
La vista se encarga de la interacción con el usuario
Presenta el menu de opciones y por cada seleccion
se hace la solicitud al controlador para ejecutar la
operación solicitada
"""

def printMenu():
    print("Bienvenido")
    print("1- Cargar información en el catálogo")
    print('2- Crear catalogo')
    print('3- Req 1: Encontrar puntos de interconexión aérea')
    print('4- Req 2: Encontrar clústeres de tráfico aéreo')
    print('5- Req 3: Encontrar la ruta más corta entre ciudades')
    print('6- Req 4: Utilizar las millas de viajero')
    print('7- Req 5: Cuantificar el efecto de un aeropuerto cerrado')
    print('8- Req 6 (BONO): Comparar con servicio WEB externo')
    print('0- Salir')

def cargarDatos(catalog):
    return controller.cargarDatos(catalog)

catalog = None

"""
Menu principal
"""
while True:
    printMenu()
    inputs = input('Seleccione una opción para continuar\n')
    if int(inputs[0]) == 1:
        print("Cargando información de los archivos ....")
        catalog = controller.iniciarCatalogo()

    elif int(inputs[0]) == 2:
        print("Creando catalogo...")
        cargarDatos(catalog)
        keys = mp.keySet(catalog["airports"])
        keys_c = mp.keySet(catalog["cities"])

        first_element = lt.firstElement(keys)
        last_element = lt.lastElement(keys_c)
        first_element_c = lt.firstElement(keys)
        last_element_c = lt.lastElement(keys_c)

        first = mp.get(catalog["airports"], first_element)
        last = mp.get(catalog["airports"], last_element)
        first_c = mp.get(catalog["cities"], first_element_c)
        last_c = mp.get(catalog["cities"], last_element_c)

        value = me.getValue(first)
        value_last = me.getValue(first)
        value_c = me.getValue(first_c)
        value_clast = me.getValue(first_c)

        tad = "Total Aeropuertos: " + str(gr.numVertices(catalog["directed"])) 
        trd = "Total de rutas: " + str(gr.numEdges(catalog["directed"]))
        tand = "Total Aeropuertos: " + str(gr.numVertices(catalog["undirected"])) 
        trnd = "Total de rutas: " + str(gr.numEdges(catalog["undirected"]))
        

        print("Grafo Dirigido: " + tad + trd +   " Grago No Dirigido: " + tand + trnd )
        print("  Información del primer Aeropuerto cargado: ")
        print("Nombre: " + value["Name"] + " Ciudad: " + value["City"] + " País: " + value["Country"] 
                            + " Latitud: " + value["Latitude"] + " Longitud: " + value["Longitude"])
        print("Información último Aeropuerto cargado: ")
        print("Nombre: " + value_last["Name"] + " Ciudad: " + value_last["City"] + " País: " + value_last["Country"] 
                            + " Latitud: " + value_last["Latitude"] + " Longitud: " + value_last["Longitude"])
        
        print("  Información de la primera ciudad cargada: ")
        print("Nombre: " + value_c["city_ascii"] + " Latitud: " + value_c["lat"] + " Longitud: " + value_c["lng"] 
                                                                    + " Población: " + value_c["population"])
        print("  Información de la última ciudad cargada: ")
        print("Nombre: " + value_clast["city_ascii"] + " Latitud: " + value_clast["lat"] + " Longitud: " + value_clast["lng"] 
                                                                    + " Población: " + value_clast["population"])
        pass

    elif int(inputs[0]) == 3:
        print("Req 1")
        pass

    elif int(inputs[0]) == 4:
        print("Req 2")
        pass

    elif int(inputs[0]) == 5:
        print("Req 3")
        pass

    elif int(inputs[0]) == 6:
        print("Req 4")
        pass

    elif int(inputs[0]) == 7:
        print("Req 5")
        pass

    elif int(inputs[0]) == 8:
        print("Req 6 (BONO)")
        pass


    else:
        sys.exit(0)
sys.exit(0)
