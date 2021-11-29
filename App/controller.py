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

import config as cf
import model
import csv


"""
El controlador se encarga de mediar entre la vista y el modelo.
"""
def iniciarCatalogo():
    catalog = model.crearCatalogo()
    return catalog
# Inicialización del Catálogo de libros

def cargarDatos(catalog):
    
    cargarAeropuertos(catalog)
    cargarRutas(catalog)
    cargarCiudades(catalog)
    cargarRutasNoDirigido(catalog)

    return catalog

# Funciones para la carga de datos

def cargarAeropuertos(catalog):

    skylinesfile = cf.data_dir + 'Skylines/airports_full.csv'
    input_file = csv.DictReader(open(skylinesfile, encoding='utf-8'))
### Aeropuetos ###
    for x in input_file:
        model.addAirport(catalog, x)

def cargarRutas(catalog):

    booksfile = cf.data_dir + 'Skylines/routes_full.csv'
    input_file = csv.DictReader(open(booksfile, encoding='utf-8'))
### Rutas ###
    for x in input_file:
        model.addRoute(catalog, x)

def cargarCiudades(catalog):
    skylinesfile = cf.data_dir + 'Skylines/airports_full.csv'
    input_file = csv.DictReader(open(skylinesfile, encoding='utf-8'))
### Ciudades ###
    for x in input_file:
        model.addAirport(catalog, x)

def cargarRutasNoDirigido(catalog):

    skylinesfile = cf.data_dir + 'Skylines/airports_full.csv'
    input_file = csv.DictReader(open(skylinesfile, encoding='utf-8'))
### Rutas ###
    for x in input_file:
        model.addAirport(catalog, x)   



# Funciones de ordenamiento

# Funciones de consulta sobre el catálogo
