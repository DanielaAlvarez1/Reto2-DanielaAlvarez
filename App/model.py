﻿"""
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
from DISClib.DataStructures import mapentry as me
from DISClib.Algorithms.Sorting import shellsort as sa
from DISClib.Algorithms.Sorting import quicksort as qu
assert cf

"""
Se define la estructura de un catálogo de videos. El catálogo tendrá dos listas, una para los videos, otra para las categorias de
los mismos.
"""

# Construccion de modelos
def initCatalog():
    catalog = {"categorias": None,
                "videos_por_categoria": None,
                "videos_por_pais": None}

    catalog["categorias"]=lt.newList(datastructure='ARRAY_LIST')
    catalog["videos_por_categoria"]= mp.newMap(37,
                                            maptype='CHAINING',
                                            loadfactor=2.0,
                                            comparefunction=comparecategories)
    catalog["videos_por_pais"]= mp.newMap(13,
                                            maptype='CHAINING',
                                            loadfactor=2.0,
                                            comparefunction=comparecountry)

    return catalog

# Funciones para agregar informacion al catalogo
def addcategory(catalog, categoria):
    lt.addLast(catalog["categorias"], categoria)

def addvideo(catalog, video):
    addvideocat(catalog, video)
    addvideocountry(catalog, video)

def addvideocat(catalog, video):
    c = catalog['videos_por_categoria']
    categoria = nombrecategoria(catalog, video["category_id"])
    existecategoria = mp.contains(c, categoria)
    if existecategoria:
        entrada = mp.get(c, categoria)
        videos = me.getValue(entrada)
    else:
        videos = lt.newList(datastructure='ARRAY_LIST')
        mp.put(c, categoria, videos)
    lt.addLast(videos, video)

def addvideocountry(catalog, video):
    p = catalog['videos_por_pais']
    pais = video["country"].lower().replace(" ", "")
    existepais = mp.contains(p, pais)
    if existepais:
        entrada = mp.get(p, pais)
        videos = me.getValue(entrada)
    else:
        videos = lt.newList(datastructure='ARRAY_LIST')
        mp.put(p, pais, videos)
    lt.addLast(videos, video)

# Funciones de consulta
def nombrecategoria(catalog, idcategoria):
    categorias = catalog["categorias"]
    for i in range(lt.size(categorias)):
        a = lt.getElement(categorias,i)
        if idcategoria == a["id"]:
            nombre = a["name"].replace(" ", "")
            return nombre.lower()

def sizecategorias(catalog):
    return lt.size(catalog["categorias"])

#Funcion Req Lab 6
def videos_likes_categoria(catalog, nombrecategoria, numero):
    nombrecategoria = nombrecategoria.replace(" ", "").lower()
    categoria = mp.get(catalog['videos_por_categoria'], nombrecategoria)
    videos = me.getValue(categoria)
    videos_ordenados = sortVideos(videos, comparelikes)

    lista_respuesta=[]
    for i in range(1, numero + 1):
            video = lt.getElement(videos_ordenados, i)
            lista_respuesta.append(video)

    return lista_respuesta

# Funciones utilizadas para comparar elementos dentro de una lista
def comparelikes(video1, video2):
     if int(video1["likes"]) > int(video2["likes"]):
        return True
     else:
        return False 

def compareviews(video1, video2):
     if int(video1["views"]) > int(video2["views"]):
        return True
     else:
        return False 

def comparecategories(llave, categoria):
    entry = me.getKey(categoria)
    if (llave == entry):
        return 0
    elif (llave > entry):
        return 1
    else:
        return -1

def comparecountry(llave, pais):
    entry = me.getKey(pais)
    if (llave == entry):
        return 0
    elif (llave > entry):
        return 1
    else:
        return -1

# Funciones de ordenamiento
def sortVideos(lista, comparacion):
    sorted_list = qu.sort(lista, comparacion)
    return sorted_list

#funcion requerimiento 1
def videos_categoria_pais(catalog, nombrecategoria, pais, numero):
    nombrecategoria = nombrecategoria.replace(" ", "").lower()
    categoria = mp.get(catalog['videos_por_categoria'], nombrecategoria)
    videos = me.getValue(categoria)
    videos_ordenados = sortVideos(videos, compareviews)
    lista_videos = []

    for i in range(1, lt.size(videos_ordenados)):
        video = lt.getElement(videos_ordenados, i)
        if video["country"].lower() == pais.lower():
            if numero > 0:
                vid_t = {"Nombre del video": video["title"], "Trending date": video["trending_date"],
                        "Nombre del canal": video["channel_title"], "Fecha Publicación": video["publish_time"],
                        "Reproducciones": video["views"], "Likes": video["likes"], "Dislikes": video["dislikes"]}
                lista_videos.append(vid_t)
                numero-=1
            elif numero == 0:
                break
                    
    return lista_videos

#funcion requerimiento 2
def video_tendencia_pais(catalog, pais):
    pais = pais.replace(" ", "").lower()
    videos_pais = mp.get(catalog['videos_por_pais'], pais)
    videos = me.getValue(videos_pais)
    sortVideos(videos, comparelikes)
    return video_tendencia(videos)

#funcion requerimiento 3
def video_tendencia_categoria(catalog, categoria):
    categoria = categoria.replace(" ", "").lower()
    videos_categoria = mp.get(catalog['videos_por_categoria'], categoria)
    videos = me.getValue(videos_categoria)
    sortVideos(videos, comparelikes)
    return video_tendencia(videos)

#función para requerimiento 2 y 3
def video_tendencia(videos):
    videos_por_id = mp.newMap(lt.size(videos),
                             maptype='CHAINING',
                             loadfactor=2.0,
                             comparefunction=comparecategories)
    tendencia_videos = mp.newMap(lt.size(videos),
                             maptype='CHAINING',
                             loadfactor=2.0,
                             comparefunction=comparecategories)

    for i in range(1, lt.size(videos)):   
        video = lt.getElement(videos, i)
        if mp.contains(tendencia_videos, video["video_id"]):
            vid = mp.get(tendencia_videos, video["video_id"])
            dias_tendencia = me.getValue(vid) + 1
        else:
            dias_tendencia = 1
            mp.put(videos_por_id, video["video_id"], video)
        mp.put(tendencia_videos, video["video_id"], dias_tendencia)

    mas_dias = 0
    video = {}
    keys = mp.keySet(tendencia_videos)
    for i in lt.iterator(keys):
        pareja_dias = mp.get(tendencia_videos, i)
        num_dias = me.getValue(pareja_dias)
        if num_dias > mas_dias:
            mas_dias = num_dias
            vid = mp.get(videos_por_id, i)
            video = me.getValue(vid)

    video["Dias Tendencia"] = mas_dias
    return video

#funcion requerimiento 4
def videos_likes(catalog, pais, tag, numero):
    pais = pais.replace(" ", "").lower()
    videos_pais = mp.get(catalog['videos_por_pais'], pais)
    videos = me.getValue(videos_pais)
    videos_ordenados = sortVideos(videos, comparelikes)
    lista_videos = []

    for i in range(1, lt.size(videos)):
        video = lt.getElement(videos_ordenados, i)
        if tag in video["tags"]:
            if numero > 0:
                vid_t = {"Nombre del video": video["title"], "Nombre del canal": video["channel_title"],
                        "Fecha Publicación": video["publish_time"],"Reproducciones": video["views"], 
                        "Likes": video["likes"], "Dislikes": video["dislikes"], "Tags": video["tags"]}
                lista_videos.append(vid_t)
                numero-= 1
            elif numero == 0:
                break 

    return lista_videos





