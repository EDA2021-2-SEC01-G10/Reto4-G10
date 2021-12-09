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
    print("1- Iniciar Analizador")
    print("2- Cargar información de los aeropuertos")
    print('3- Req 1: Encontrar puntos de interconexión aérea')
    print('4- Req 2: Encontrar clústeres de tráfico aéreo')
    print('5- Req 3: Encontrar la ruta más corta entre ciudades')
    print('6- Req 4: Utilizar las millas de viajero')
    print('7- Req 5: Cuantificar el efecto de un aeropuerto cerrado')
    print('8- Req 6 (BONO): Comparar con servicio WEB externo')
    print('0- Salir')

def printsCargaDatos(cat):
    print("")
    print("El total de aeropuertos en el grafo dirigido son: "+str(gr.numVertices(cat["directed"])))
    print("")
    print("El total de aeropuertos en el grafo no dirigido son: "+ str(gr.numVertices(cat["directed"])))
    print("")
    print("El total de rutas en el grafo dirigido son: "+str(gr.numEdges(cat["directed"])))
    print("")
    print("El total de rutas en el grafo no dirigido son: "+ str(gr.numEdges(cat["undirected"])))
    print("")
    print("El total de ciudades cargadas son: "+ str(mp.size(cat["cities"])))
    print("────────────────────────────────────────────")
    print("El primer y ultimo aeropuerto, cargados en el grafo dirigido son:")
    print("")
    aeropuertos=cat["airportsLt"]
    first=lt.firstElement(aeropuertos)
    last=lt.lastElement(aeropuertos)
    print("|Nombre: " + first["Name"] + " |Ciudad: " + first["City"] + " |País: " + first["Country"] 
                            + " |Latitud: " + first["Latitude"] + " |Longitud: " + first["Longitude"]) 
    print("")                        
    print("|Nombre: " + last["Name"] + " |Ciudad: " + last["City"] + " |País: " + last["Country"] 
                            + " |Latitud: " + last["Latitude"] + " |Longitud: " + last["Longitude"])   
    print("")                         
    print("────────────────────────────────────────────")
    print("El primer y ultimo aeropuerto, cargados en el grafo no dirigido son:")    
    print("")
    print("|Nombre: " + first["Name"] + " |Ciudad: " + first["City"] + " |País: " + first["Country"] 
                            + " |Latitud: " + first["Latitude"] + " |Longitud: " + first["Longitude"]) 
    print("")                        
    print("|Nombre: " + last["Name"] + " |Ciudad: " + last["City"] + " |País: " + last["Country"] 
                            + " |Latitud: " + last["Latitude"] + " |Longitud: " + last["Longitude"])   
    print("")                         
    print("────────────────────────────────────────────")                         
    ciudades=cat["citiesLt"]
    firstCit=lt.firstElement(ciudades)
    lastCit=lt.lastElement(ciudades)   
    print("La primer y ultima ciudad cargadas son:") 
    print("")
    print("|Ciudad: " + firstCit["city_ascii"] + "|País: " + firstCit["country"] 
                            + " |Latitud: " + firstCit["lat"] + " |Longitud: " + firstCit["lng"]+" |Poblacion: " + firstCit["population"]) 
    print("")                        
    print("|Ciudad: " + lastCit["city_ascii"] + "|País: " + lastCit["country"] 
                            + " |Latitud: " + lastCit["lat"] + " |Longitud: " + lastCit["lng"]+" |Poblacion: " + lastCit["population"])                                                           
    print("") 
    
def masConectados(cat):
    listR=controller.masConectados(cat)
    return listR
def printsReq1(ltMasConectados,cat):

    vertices=gr.numVertices(cat["directed"])
    maxConexiones=list(lt.iterator(ltMasConectados[1]))
    print("")
    print("Las mayores conexiones con sus respectivo aeropuerto son: ")
    print("")
    print("[Numero de conexiones , Aeropuerto(IATA)]")
    print("")
    for i in range(0,5):
        print(maxConexiones[i])
        print("")
    print("────────────────────────────────────────────")    
    print("El numero de aeropuertos interconectados es: "+ str(vertices))
    print("")
    print("────────────────────────────────────────────")
    ltConectados=list(lt.iterator(ltMasConectados[0]))
    print("El top 5 de los aeropuertos mas conectados es:")
    print("")
    for i in range(0,5): 
            print ("|IATA:"+ ltConectados[i]["IATA"]+ " |Nombre:"+ ltConectados[i]['Name'] + " |Ciudad: "+ ltConectados[i]['City'] +" |Pais: "+ ltConectados[i]["Country"])
            print("")

def calcularClusteres(cat,iata1,iata2):
    infoClusteres=controller.calcularClusteres(cat,iata1,iata2)
    return infoClusteres

def printsReq2(infoClusteres,iata1,iata2):
    print("")
    print("El número total de clústeres presentes en la red de transporte aéreo es :"+str(infoClusteres[0])) 
    conectados=infoClusteres[1]
    if conectados == True : 
       print("") 
       print("El aeropuerto "+iata1+" y el aeropuerto "+iata2+", se encuentran en el mismos clúster." )
       print("")
    else: 
          print("") 
          print("El aeropuerto "+iata1+" y el aeropuerto "+iata2+", no se encuentran en el mismos clúster." ) 
          print("")    

def listarOrigen(cat, origen):
    listOrigen=controller.listarOrigen(cat, origen)
    return listOrigen

def printMenuOrigen(listOrigen):
    print("")
    print("Las siguientes son las ciudades en nuestros datos que coinciden con la que usted desea seleccionar como origen:")
    ciudades=list(lt.iterator(listOrigen))
    for i in range(0,len(ciudades)):
        print("")
        print(str(i+1)+")Ciudad : "+ciudades[i]['city_ascii']+"|País: "+ciudades[i]['country']+"|Latitud: "+ciudades[i]['lat']+"|Longitud: "+ciudades[i]['lng'] )
        print("")

def listarDestino(cat,destino):
    listDestino=controller.listarDestino(cat,destino)
    return listDestino

def printMenuDestino(listDestino):
    print(" ")
    print("Las siguientes son las ciudades en nuestros datos que coinciden con la que usted desea seleccionar como destino:")
    ciudades=list(lt.iterator(listDestino))
    for i in range(0,len(ciudades)):
        print("")
        print(str(i+1)+")Ciudad : "+ciudades[i]['city_ascii']+"|País: "+ciudades[i]['country']+"|Latitud: "+ciudades[i]['lat']+"|Longitud: "+ciudades[i]['lng'] )
        print("")
def printsReq3(aeropuertoOrigen,aeropuertoDestino,distanciaVuelo):
    print("")
    print("El aeropuerto de salida es: "+aeropuertoOrigen[0])
    print("")
    print("El aeropuerto de llegada es: "+aeropuertoDestino[0])
    print("")
    print("La distancia del vuelo es: "+str(distanciaVuelo)+" Kilometros")
    print("")
    print("La distancia total de la ruta es: "+str(distanciaVuelo+aeropuertoOrigen[1]+aeropuertoDestino[1])+" Kilometros")
    
def efecto_ac(cat, aeropuerto):
    result = controller.efecto_ac(cat, aeropuerto)
    number = lt.removeFirst(result)
    list1 = lt.removeFirst(result)

    print("Número de Aeropuertos afectados: " + str(number))
    print("Primeros 3 Aeropiertos afectados: ")
   
    for y in range(0, 3):
        if lt.getElement(list1,y) != lt.getElement(list1,y-1):
            print('IATA: ' + lt.getElement(list1,y)['IATA'] + ', Nombre: ' + lt.getElement(list1,y)['Name']
            + ', Ciudad: ' + lt.getElement(list1,y)['City'] + ', País: ' + lt.getElement(list1,y)['Country']) 

def printreq4(cat):

    origin = input("Ingrese la ciudad de origen: ")
    miles = float(input("Ingrese su cantidad de Millas: "))
    km = miles * 1.60
    final, costo, cantidad, iata = controller.millas_viajero(cat, origin)
    peso = 0 

    print("Aeropuerto de Origen: " + mp.get(cat["airports"], iata)["value"]["Name"] 
            + " de la ciudad de " + mp.get(cat["airports"], iata)["value"]["City"] + ", " 
                + mp.get(cat["airports"], iata)["value"]["Country"])
    
    print("Numero de Aeropuertos Posibles: " + str(cantidad))
   
    print("Maxima distancia posible entre aeropuertos en km: " + str(round(costo, 2)))
    
    print("Millas del pasajero en Km: " + str(round(km, 2)))

    print("Detalles Recorrido más Largo")
  
    while not st.isEmpty(final):
        A = st.pop(final)
        B = st.top(final)
        edge = gr.getEdge(cat["undirected"], A, B)

        print(edge["vertexA"] + "--->" + edge["vertexB"] 
                    + " costo: " + str(edge["weight"]))
        peso += edge["weight"]

        if st.size(final) == 1:
            break

    print("Distancia del Recorrido más Largo: " + str(round(peso, 2)))

    if km < peso:
        total = peso - km
        millas_finanles = round((total / 1.60), 2)
        print("Hacen falta: " + str(millas_finanles) + " millas para completar el viaje")

    else:

        total = km - peso
        millas_finanles = round((total / 1.60), 2)
        print("Al pasajero le quedan: " + str(millas_finanles) + " millas")

    return None 

cat = None
"""
Menu principal
"""
while True:
    printMenu()
    inputs = input('Seleccione una opción para continuar\n')
    if int(inputs[0]) == 1:
        print("\nInicializando....")
        cat = controller.inicializar()

    elif int(inputs[0]) == 2:
         print("Cargando información de los archivos ....")
         controller.cargarDatos(cat)
         printsCargaDatos(cat)

    elif int(inputs[0]) == 3:
         ltMasConectados=masConectados(cat)
         printsReq1(ltMasConectados,cat)

    elif int(inputs[0]) == 4:
         iata1= input("Ingrese el codigo IATA del primer aeropuerto: " )
         iata2= input("Ingrese el codigo IATA del segundo aeropuerto: " )
         infoClusteres=calcularClusteres(cat,iata1,iata2)
         printsReq2(infoClusteres,iata1,iata2)

    elif int(inputs[0]) == 5:
         origenI=input("Ingrese el nombre de la ciudad de origen: ")
         destinoI=input("Ingrese el nombre de la ciudad de destino: ")        
         origen=(origenI.lower()).strip()
         destino=(destinoI.lower()).strip()
         listOrigen=listarOrigen(cat,origen)
         printMenuOrigen(listOrigen)
         print("")
         ciudadOrigenInput=int(input("Ingrese el digito de la ciudad de origen correspondiente :"))
         ciudadOrigen=list(lt.iterator(listOrigen))[ciudadOrigenInput-1]
         listDestino=listarDestino(cat,destino)
         printMenuDestino(listDestino)
         print("")
         ciudadDestinoInput=int(input("Ingrese el digito de la ciudad de destino correspondiente :"))
         ciudadDestino=list(lt.iterator(listDestino))[ciudadDestinoInput-1]
         aeropuertoOrigen=controller.buscarAeropuertoOrigen(cat,ciudadOrigen)
         aeropuertoDestino=controller.buscarAeropuertoDestino(cat,ciudadDestino)
         origen=aeropuertoOrigen[0]
         destino=aeropuertoDestino[0]
         distanciaVuelo=controller.distanciaVuelo(cat,origen,destino)
         printsReq3(aeropuertoOrigen,aeropuertoDestino,distanciaVuelo)

    elif int(inputs[0]) == 6:
        printreq4(cat)
        pass

    elif int(inputs[0]) == 7:
        aeropuerto = input("Código IATA del aeropuerto fuera de funcionamiento:  ")
        efecto_ac(cat, aeropuerto)

    elif int(inputs[0]) == 8:
        print("Req 6 (BONO)")
        pass


    else:
        sys.exit(0)
sys.exit(0)
