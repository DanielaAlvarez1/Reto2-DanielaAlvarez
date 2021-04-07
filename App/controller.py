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

import time
import tracemalloc
import config as cf
import model
import csv


"""
El controlador se encarga de mediar entre la vista y el modelo.
"""

# Inicialización del Catálogo de libros
def initCatalog():
    catalog = model.initCatalog()
    return catalog

# Funciones para la carga de datos
def cargarinfocatalogo(catalog):
    delta_time = -1.0
    delta_memory = -1.0

    tracemalloc.start()
    start_time = getTime()
    start_memory = getMemory()

    cargarcategorias(catalog)
    cargardatos(catalog)

    stop_memory = getMemory()
    stop_time = getTime()
    tracemalloc.stop()

    delta_time = stop_time - start_time
    delta_memory = deltaMemory(start_memory, stop_memory)

    return delta_time, delta_memory

def cargardatos(catalog):
    vfile = cf.data_dir + 'videos/videos-large.csv'
    input_file = csv.DictReader(open(vfile, encoding='utf-8'))
    for video in input_file:
        tags = video["tags"].split("|")
        video["tags"] = tags
        model.addvideo(catalog, video)

def cargarcategorias(catalog):
    cfile = cf.data_dir + 'videos/category-id.csv'
    input_file = csv.DictReader(open(cfile, encoding='utf-8'), delimiter = "\t")
    for categoria in input_file:
        model.addcategory(catalog, categoria)

# Funciones de consulta sobre el catálogo
def sizecategorias(catalog):
    return model.sizecategorias(catalog)

# Funciones consulta tiempo y memoria
def getTime():
    return float(time.perf_counter()*1000)


def getMemory():
    return tracemalloc.take_snapshot()


def deltaMemory(start_memory, stop_memory):
    memory_diff = stop_memory.compare_to(start_memory, "filename")
    delta_memory = 0.0

    for stat in memory_diff:
        delta_memory = delta_memory + stat.size_diff

    delta_memory = delta_memory/1024.0
    return delta_memory


#Funcion Req Lab 6
def videos_likes_categoria(catalog, categoria, numero):
    v = model.videos_likes_categoria(catalog, categoria, numero)
    return v

# Funcion requerimiento 1
def videos_categoria_pais(catalog, categoria, pais, numero):
    return model.videos_categoria_pais(catalog, categoria, pais, numero)

#funcion requerimiento 2
def video_trending(catalog,pais):
    return model.video_tendencia_pais2(catalog,pais)

#funcion requerimiento 3
def video_categoria(catalog,categoria):
    return model.video_tendencia_categoria(catalog,categoria)

#funcion requerimiento 4
def videos_likes(catalog, pais, tag, numero):
    return model.videos_likes(catalog, pais, tag, numero)
