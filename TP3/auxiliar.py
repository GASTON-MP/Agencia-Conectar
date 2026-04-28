"""Funciones auxiliares para Agencia Conectar"""

import os
import constantes


def validar_entrada(mensaje: str):
    """
    Pide al usuario un ingreso y si lo ingresado es '**' devuelve None,
    sino devuelve lo que ingreso

    PRE-COINDICIONES:
    -Recibe un string
    """
    ingreso = input(mensaje)
    if ingreso == "**":
        return None
    return ingreso


def acceso_rutas(ingreso: str):
    """
    La funcion crea un lista con las rutas y se validan
    se valida que exista la ruta
    se valida si es un directorio, si es un directorio se llama a directorio_a_ruta
    se valida que sea un archivo .csv

    PRE-COINDICIONES:
    -Recibe un string que son las rutas

    POST-COINDICIONES:
    -Devuelve una lista con las rutas
    """
    rutas_finales = []
    lista_rutas = ingreso.split(" ")
    for ruta in lista_rutas:
        if not os.path.exists(ruta):
            print(constantes.ERROR_IMPORTACION)
            return None
        if os.path.isdir(ruta):
            lista_directorios = directorio_a_ruta(ruta)
            rutas_finales.extend(lista_directorios)

        elif ruta.endswith(".csv"):
            rutas_finales.append(ruta)

        else:
            print(constantes.ERROR_IMPORTACION)
            return None

    return rutas_finales


def directorio_a_ruta(directorio: str):
    """
    La funcion crea una lista con los subdirectorios y archivos del directorio
    si encuentra una carpeta dentro del directorio se recorre recursivamente

    PRE-COINDICIONES:
    -Recibe un directorio

    POST-COINDICIONES:
    -Devuelve una lista con las rutas
    """
    lista_rutas = []
    lista_archivos = os.listdir(directorio)

    for archivo in lista_archivos:
        ruta = os.path.join(directorio, archivo)

        if os.path.isdir(ruta):
            lista_recursiva = directorio_a_ruta(ruta)
            lista_rutas.extend(lista_recursiva)

        else:
            lista_rutas.append(ruta)
    return lista_rutas


def reemplazar_tildes(ingreso: str):
    """
    Crea un diccionario con las vocales con tildes como claves y sin tildes los valores
    recorre y remplaza las que tienen tilde con las que no en el nombre

    PRE-COINDICIONES:
    -Recibe lo que ingreso el usuario (nombre)

    POST-COINDICIONES:
    -Devuelve el nombre sin tildes
    """
    reemplazos = {
        "á": "a",
        "é": "e",
        "í": "i",
        "ó": "o",
        "ú": "u",
        "Á": "A",
        "É": "E",
        "Í": "I",
        "Ó": "O",
        "Ú": "U",
    }

    sin_tildes = ingreso
    for c, s in reemplazos.items():
        sin_tildes = sin_tildes.replace(c, s)
    return sin_tildes


def nombres_iguales(nombre1: str, nombre2: str):
    """
    Compara los nombres
    """
    n1 = reemplazar_tildes(nombre1.strip().lower())
    n2 = reemplazar_tildes(nombre2.strip().lower())
    return n1 == n2


def validar_nombre(nombre: str):
    """
    Valida que el nombre no este vacio o no contenga caracteres invalidos

    PRE-COINDICIONES:
    -Recibe un string

    POST-COINDICIONES:
    -Devuelve un booleano
    """
    sin_espacio = nombre.replace(" ", "")
    if not sin_espacio.isalpha():
        print(constantes.ERROR_NOMBRE_TALENTO_INVALIDO)
        return False
    return True


def colaboradores_directos(info_peliculas: dict, nombre: str):
    """
    Se extiende la lista de colaboraciones con la lista de talentos de cada pelicula
    elimina el propio talento de la lista y los talento duplicados

    PRE-COINDICIONES:
    -Recibe un diccionario
    -Recibe un string

    POST-COINDICIONES:
    -Devuelve una lista
    """
    lista_colab = []

    for pelicula in info_peliculas:
        lista_talentos = info_peliculas[pelicula]["talentos"]

        for talento in lista_talentos:
            if nombres_iguales(talento, nombre):
                lista_colab.extend(lista_talentos)

    if not lista_colab:
        return None

    nueva_lista = []
    for t in lista_colab:
        if not nombres_iguales(t, nombre):
            nueva_lista.append(t)

    lista_colab = list(set(nueva_lista))

    return lista_colab


def encontrar_talento(info_peliculas: dict, nombre: str):
    """
    Encuentra el talento que coincida con el nombre
    """
    for pelicula in info_peliculas.values():
        for talento in pelicula["talentos"]:
            nombre_talento = reemplazar_tildes(talento.strip().lower())
            if nombre == nombre_talento:
                lista_colab = colaboradores_directos(info_peliculas, talento)
                return talento, lista_colab

    return None, None


def validar_talento(info_peliculas: dict):
    """
    Pide al usuario un talento, lo capitaliza
    se evalua que sea un string este bien escrito
    se evaluan las tildes en el talento

    PRE-COINDICIONES:
    -Recibe un diccionario

    POST-COINDICIONES:
    -Devuelve un nombre y la lista con colaboraciones directas
    """
    while True:
        ingreso = validar_entrada("Ingrese el nombre de un talento: ")

        if ingreso is None:
            return None, None

        if not validar_nombre(ingreso.title()):
            continue

        nombre_ingresado = reemplazar_tildes(ingreso.strip().lower())

        talento, lista_colab = encontrar_talento(info_peliculas, nombre_ingresado)

        if not talento:
            print(constantes.ERROR_TALENTO_NO_ENCONTRADO)
            continue

        return talento, lista_colab


def buscar_compatibles(info_peliculas, talento, compatibles):
    """
    Busca los talentos compatibles con el talento ingresado
    se agrega el talento a la lista compatibles
    se agrega a la lista_colab la lista de los talentos de cada pelicula
    se eliminan los duplicados
    para cada colaboracion si no esta en compatibles se llama a la recursividad

    PRE-COINDICIONES:
    -Recibe un diccionario
    -Recibe un talento
    -Recibe una lista vacia

    POST-COINDICIONES:
    -Devuelve una lista con los compatibles y directos
    """
    if talento in compatibles:
        return compatibles

    compatibles.append(talento)

    lista_colab = []
    for pelicula in info_peliculas:
        if talento in info_peliculas[pelicula]["talentos"]:
            lista_colab.extend(info_peliculas[pelicula]["talentos"])

    lista_colab = list(set(lista_colab))

    for colab in lista_colab:
        if colab not in compatibles:
            buscar_compatibles(info_peliculas, colab, compatibles)

    return list(set(compatibles))


def ordenamiento(valores: tuple):
    """
    Devuelve el orden descendente para el total
    y el orden alfabetico
    """
    talento = valores[0]
    total = valores[1]
    return (-total, talento)


def calculo_recaudacion(info_peliculas: dict):
    """
    La funcion calcula el precio de la pelicula por la cantidad de ventas de entradas
    y agrega en un nuevo diccionario los valores

    PRE-COINDICIONES:
    -Recibe un diccionario

    POST-COINDICIONES:
    -Devuelve un diccionario
    """
    recaudacion = {}

    for pelicula in info_peliculas:
        total_pelicula = int(info_peliculas[pelicula]["ventas"]) * int(
            info_peliculas[pelicula]["precio"]
        )
        info_peliculas[pelicula]["total"] = total_pelicula

        for talento in info_peliculas[pelicula]["talentos"]:
            if talento not in recaudacion:
                recaudacion[talento] = 0
            recaudacion[talento] += total_pelicula

    return recaudacion
