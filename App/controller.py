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
 """
from DISClib.ADT import list as lt
import config as cf
import model
import csv


"""
El controlador se encarga de mediar entre la vista y el modelo.
"""
# Inicialización 

def inicializar():
    cat = model.newAnalyzer()
    return cat


# Funciones para la carga de datos
def cargarDatos(cat):    
    cargarAeropuertos(cat)
    cargarRutas(cat)
    cargarRutasUndirected(cat)
    cargarCiudades(cat)
    
def cargarAeropuertos(cat):
    airportsfile = cf.data_dir + 'Skylines/airports-utf8-small.csv'
    input_file = csv.DictReader(open(airportsfile, encoding='utf-8'))
    for aeropuerto in input_file:
        model.addAirport(cat, aeropuerto)

def cargarRutas(cat):
    rutesfile = cf.data_dir + 'Skylines/routes-utf8-small.csv'
    input_file = csv.DictReader(open(rutesfile, encoding='utf-8'))
    for ruta in input_file:
        model.addRout(cat,ruta)
        model.addRouteDirected(cat,ruta) 

def cargarRutasUndirected(cat): 
        rutas=cat["rutas"]
        for ruta in lt.iterator(rutas):      
            model.addRouteUndirected(cat,ruta) 

def cargarCiudades(cat):
    citiesfile = cf.data_dir + 'Skylines/worldcities-utf8.csv'
    input_file = csv.DictReader(open(citiesfile, encoding='utf-8')) 
    for city in input_file: 
        model.addCity(cat,city) 
    

# Funciones de ordenamiento

# Funciones de consulta sobre el catálogo
def masConectados(cat): 
    listMasConectados=model.masConectados(cat)
    top=model.top(listMasConectados,cat)
    return (top,listMasConectados)

def calcularClusteres(cat,iata1,iata2):
    infoClusteres=model.calcularClusteres(cat,iata1,iata2) 
    return infoClusteres     

def listarOrigen(cat, origen):
    listOrigen=model.listarOrigen(cat, origen)
    return listOrigen

def listarDestino(cat,destino):
    listDestino=model.listarDestino(cat,destino)    
    return listDestino

def buscarAeropuertoOrigen(cat,ciudadOrigen): 
    aeropuerto=model.buscarAeropuertoOrigen(cat,ciudadOrigen)
    return aeropuerto  

def efecto_ac(cat, aeropuerto):
    return model.efecto_ac(cat, aeropuerto)