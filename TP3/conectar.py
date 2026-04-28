"""Logica, interfaz e interaccion de Agencia Conectar"""

import constantes
import auxiliar


def cargar_peliculas(info_peliculas: dict):
    """
    Pide al usuario que ingrese una o varias rutas
    llama a la funcion recursiva que encuentra los accesos a las rutas
    abre cada archivo y lee sus lineas
    por cada linea carga en un diccionario las peliculas y sus valores,
    si la pelicula esta repetida se ignora.

    PRE-COINDICIONES:
    -Recibe un diccionario.

    POST-COINDICIONES:
    -Devuelve el diccionario con la carga de las peliculas.
    """
    while True:
        ingreso = auxiliar.validar_entrada("Ingrese el archivo de películas a cargar: ")

        if ingreso is None:
            return info_peliculas

        rutas_finales = auxiliar.acceso_rutas(ingreso)

        if rutas_finales is None:
            continue

        break

    contador_pelis = 0
    for archivo in rutas_finales:
        with open(archivo, "r", encoding="utf-8") as csv:
            csv.readline()
            for linea in csv:
                contenido = linea.strip()
                valores = contenido.split(",")
                lista_talentos = valores[2].split(";")

                if valores[0] in info_peliculas:
                    print(f"{constantes.PELICULA_DUPLICADA} {valores[0]}")

                else:
                    contador_pelis += 1

                info_peliculas[valores[0]] = {
                    "precio": valores[1],
                    "talentos": lista_talentos,
                    "ventas": 0,
                }

    print(f"OK {contador_pelis}")
    return info_peliculas


def cargar_ventas(info_peliculas: dict):
    """
    Pide al usuario que ingrese una o varias rutas
    llama a la funcion recursiva que encuentra los accesos a las rutas
    abre cada archivo y lee sus lineas
    por cada linea carga en un diccionario las ventas y sus valores
    si la pelicula no esta cargada se ignora.

    PRE-COINDICIONES:
    -Recibe un diccionario

    POST-COINDICIONES:
    -Devuelve el diccionario con las ventas cargadas
    """
    while True:
        ingreso = auxiliar.validar_entrada("Ingrese el archivo de ventas a cargar: ")

        if ingreso is None:
            return info_peliculas

        rutas_finales = auxiliar.acceso_rutas(ingreso)

        if rutas_finales is None:
            continue

        break

    contador_ventas = 0
    for archivo in rutas_finales:
        with open(archivo, "r", encoding="utf-8") as csv:
            csv.readline()
            for linea in csv:
                contenido = linea.strip()
                valores = contenido.split(",")

                if valores[0] in info_peliculas:
                    info_peliculas[valores[0]]["ventas"] += int(valores[1])
                    contador_ventas += 1

                else:
                    print(f"{constantes.PELICULA_INEXISTENTE} {valores[0]}")

    print(f"OK {contador_ventas}")
    return info_peliculas


def listar_colab_directas(info_peliculas: dict):
    """
    Pide al usuario un talento y se valida
    se llama a la funcion auxiliar que devuelve la lista con los
    colaboradores directos, se ordena y se imprime la lista enumerada.

    PRE-COINDICIONES:
    -Recibe un diccionario

    """

    _, lista_colab = auxiliar.validar_talento(info_peliculas)

    if lista_colab is None:
        return

    if not lista_colab:
        print(constantes.COLABORADORES_DIRECTOS_INEXISTENTES)
        return

    lista_colab.sort()

    print(constantes.COLABORADORES_DIRECTOS)

    for i, talento in enumerate(lista_colab):
        print(f"{i+1}. {talento}")


def listar_compatibles(info_peliculas):
    """
    Pide al usuario un talento y se valida
    se llama a la funcion auxiliar que devuelve una lista con los
    colaboradores directos. Se llama a la funcion que busca los compatibles
    y devuelve una lista.
    Se eliminan los colaboradores directos o el mismo talento de la lista compatibles
    se ordena la lista compatibles y se imprime la lista enumerada.

    PRE-COINDICIONES:
    -Recibe un diccionario
    """
    nombre, lista_directos = auxiliar.validar_talento(info_peliculas)

    if lista_directos is None:
        return

    compatibles = auxiliar.buscar_compatibles(info_peliculas, nombre, [])

    for directo in lista_directos:
        if directo in compatibles:
            compatibles.remove(directo)

    if nombre in compatibles:
        compatibles.remove(nombre)

    if not compatibles:
        print(constantes.TALENTOS_COMPATIBLES_INEXISTENTES)
        return

    compatibles.sort()

    print(constantes.TALENTOS_COMPATIBLES)
    for i, talento in enumerate(compatibles):
        print(f"{i+1}. {talento}")


def listar_incompatibles(info_peliculas):
    """
    Pide al usuario un talento y se valida
    se llama a la funcion que busca los compatibles y devuelve una lista compatibles
    se recorre para ver si el talento esta en la lista compatibles sino la agrega a incompatibles
    se ordena la lista incompatibles y se imprime la lista enumerada

    PRE-COINDICIONES:
    -Recibe un diccionario
    """
    incompatibles = []

    nombre, _ = auxiliar.validar_talento(info_peliculas)

    if nombre is None:
        return

    compatibles = auxiliar.buscar_compatibles(info_peliculas, nombre, [])

    for pelicula in info_peliculas:
        for talento in info_peliculas[pelicula]["talentos"]:
            if talento not in compatibles:
                incompatibles.append(talento)

    if not incompatibles:
        print(constantes.TALENTOS_INCOMPATIBLES_INEXISTENTES)
        return

    incompatibles = list(set(incompatibles))

    incompatibles.sort()

    print(constantes.TALENTOS_INCOMPATIBLES)
    for i, talento in enumerate(incompatibles):
        print(f"{i+1}. {talento}")


def exportar_mayor_recaudacion(info_peliculas):
    """
    Pide al usuario una ruta y se llama a funcion auxiliar para validarla
    se calcula lo que recaudo cada talento por cada pelicula que participo
    se carga las recaudaciones a un nuevo diccionario
    se ordenan las recaudaciones de manera descendiente
    a la ruta ingresada se crea un archivo .csv y se carga las recaudaciones de cada talento

    PRE-COINDICIONES:
    -Recibe un diccionario
    """
    while True:
        ruta = auxiliar.validar_entrada("Ingrese la ruta del archivo a guardar: ")

        if ruta is None:
            return
        if " " in ruta:
            print(constantes.ERROR_EXPORTACION)
            continue
        if not ruta.endswith(".csv"):
            print(constantes.ERROR_EXPORTACION)
            continue

        recaudacion = auxiliar.calculo_recaudacion(info_peliculas)

        recaudacion_ordenada = sorted(recaudacion.items(), key=auxiliar.ordenamiento)

        try:
            with open(ruta, "w", encoding="utf-8") as archivo:
                archivo.write("actor,recaudacion\n")

                archivo.writelines(
                    f"{talento},{total}\n" for talento, total in recaudacion_ordenada
                )

            print("OK")

        except FileNotFoundError:
            print(constantes.ERROR_EXPORTACION)
            continue

        break


def main():
    """
    Crea un diccionario que contendra la informacion de las peliculas
    Se pide al usuario una opcion entre las funcionalidades
    Depende lo que elija el usuario se llama a esa funcion
    Cuando quiera terminar el programa ingresa '7' para salir
    """
    info_peliculas = {}

    opciones = {
        "1": cargar_peliculas,
        "2": cargar_ventas,
        "3": listar_colab_directas,
        "4": listar_compatibles,
        "5": listar_incompatibles,
        "6": exportar_mayor_recaudacion,
    }

    while True:
        opcion = input(
            "1) Cargar películas\n"
            "2) Cargar información de ventas\n"
            "3) Listar colaboraciones directas\n"
            "4) Listar talentos compatibles\n"
            "5) Listar talentos incompatibles\n"
            "6) Exportar talentos con mayor recaudación\n"
            "7) Salir\n"
            ">>> "
        )

        if opcion == "7":
            return

        if opcion in opciones:
            opciones[opcion](info_peliculas)

        else:
            print(constantes.OPCION_INVALIDA)


if __name__ == "__main__":
    main()
