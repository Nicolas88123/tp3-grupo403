# principal.py
# Programa principal del TP3. Ac va el menu de opciones que pide el
# enunciado. Este archivo NO define la clase (eso esta en clase.py),
# aca solo estan las funciones que leen el archivo, arman la lista
# de tratamientos y calculan/muestran los resultados de cada opcion.

from clase import Tratamiento

# nombre del archivo de entrada. Tiene que estar SIEMPRE en la misma
# carpeta que este programa, y tiene que llamarse asi (tal cual lo
# pide el enunciado, sino el runner tira error)
NOMBRE_ARCHIVO = "tratamientos.csv"


# ==================================================================
# OPCION 1: Cargar Tratamientos
# ==================================================================

def crear_tratamiento_desde_linea(linea):
    # esta funcion recibe una linea de texto del csv (ya sin el salto
    # de linea) y devuelve un objeto Tratamiento armado con esos datos

    # separo la linea por comas, me queda una lista de 7 elementos
    # (todos en formato texto todavia)
    campos = linea.split(",")

    # ahora convierto cada campo al tipo de dato que corresponde,
    # respetando el orden que indica el enunciado:
    # dni, nombre, apellido, icd10, monto_base, complejidad, id_algoritmo
    dni = int(campos[0])
    nombre = campos[1]
    apellido = campos[2]
    icd10 = campos[3]
    monto_base = float(campos[4])
    complejidad = campos[5]
    id_algoritmo = int(campos[6])

    # con esos datos ya puedo construir el objeto Tratamiento
    nuevo_tratamiento = Tratamiento(dni, nombre, apellido, icd10, monto_base, complejidad, id_algoritmo)
    return nuevo_tratamiento


def cargar_tratamientos():
    # esta funcion abre el archivo tratamientos.csv, lo recorre linea
    # por linea, y va armando el vector (lista) de tratamientos

    tratamientos = []  # el vector donde voy a ir guardando cada tratamiento

    archivo = open(NOMBRE_ARCHIVO, "r", encoding="utf-8")

    # uso esta bandera para saber cuando estoy en la primera linea
    # (la del encabezado), que hay que ignorar
    es_la_primera_linea = True

    for linea in archivo:
        if es_la_primera_linea:
            # esta es la linea de encabezado (los nombres de columnas),
            # no la proceso, solo bajo la bandera para que las
            # siguientes vueltas del for entren al else
            es_la_primera_linea = False
            continue

        # saco el salto de linea (y espacios de mas) del final
        linea = linea.strip()

        # si por algun motivo la linea quedo vacia (por ejemplo la
        # ultima linea del archivo), la salteo
        if linea == "":
            continue

        # armo el objeto Tratamiento a partir del texto de la linea
        tratamiento = crear_tratamiento_desde_linea(linea)

        # ya que lo tengo cargado, le calculo el monto final de una vez
        # (asi no lo tengo que recalcular despues en la opcion 2)
        tratamiento.calcular_monto_final()

        # lo agrego al vector de tratamientos
        tratamientos.append(tratamiento)

    archivo.close()

    return tratamientos


def obtener_quinto_apellido_alta_complejidad(tratamientos):
    # recorro el vector de tratamientos en el mismo orden en que fueron
    # cargados (o sea, el orden del archivo) y cuento cuantos son de
    # alta complejidad. Cuando llego al quinto, guardo su apellido.

    contador_alta_complejidad = 0

    for tratamiento in tratamientos:
        if tratamiento.es_alta_complejidad():
            contador_alta_complejidad = contador_alta_complejidad + 1

            # si este es el numero 5, ya tengo lo que busco, devuelvo
            # el apellido y corto la funcion aca
            if contador_alta_complejidad == 5:
                return tratamiento.apellido

    # si termino de recorrer todo el vector y nunca llegue a 5,
    # devuelvo None para indicar que no habia suficientes
    return None


def mostrar_resultados_opcion_1(tratamientos):
    # r1.1: simplemente la cantidad de elementos del vector
    cantidad_cargados = len(tratamientos)

    # r1.2: el apellido del 5to tratamiento de alta complejidad
    quinto_apellido = obtener_quinto_apellido_alta_complejidad(tratamientos)

    print("r1.1:", cantidad_cargados)

    # si la funcion me devolvio None es porque no habia 5 tratamientos
    # de alta complejidad, entonces muestro el mensaje que pide el
    # enunciado en vez del apellido
    if quinto_apellido is None:
        print("r1.2: No hay suficientes tratamientos de alta complejidad.")
    else:
        print("r1.2:", quinto_apellido)


def opcion_cargar_tratamientos():
    # esta es la funcion "orquestadora" de la opcion 1 del menu:
    # carga los tratamientos del archivo y despues muestra los
    # resultados pedidos por el enunciado
    tratamientos = cargar_tratamientos()
    mostrar_resultados_opcion_1(tratamientos)

    # devuelvo el vector cargado para que el programa principal lo
    # guarde y lo pueda usar despues en la opcion 2
    return tratamientos


# ==================================================================
# OPCION 2: Mostrar Resultados
# ==================================================================

def calcular_diferencia_promedio(tratamientos):
    # r2.1: promedio de (monto_final - monto_base) de todos los
    # tratamientos del vector

    suma_de_diferencias = 0
    cantidad_de_tratamientos = 0

    for tratamiento in tratamientos:
        diferencia = tratamiento.monto_final - tratamiento.monto_base
        suma_de_diferencias = suma_de_diferencias + diferencia
        cantidad_de_tratamientos = cantidad_de_tratamientos + 1

    # si el vector estuviera vacio, evito la division por cero
    if cantidad_de_tratamientos == 0:
        return 0

    promedio = suma_de_diferencias / cantidad_de_tratamientos
    return promedio


def contar_tratamientos_por_letra(tratamientos):
    # como no podemos usar diccionarios, cuento la cantidad de
    # tratamientos por cada letra del icd10 usando un vector de 26
    # posiciones (una por cada letra del abecedario). La posicion 0
    # corresponde a la letra "A", la posicion 1 a la "B", y asi
    # sucesivamente hasta la posicion 25 que es la "Z".

    contadores = [0] * 26  # arranco todos los contadores en 0

    for tratamiento in tratamientos:
        letra = tratamiento.obtener_letra_icd10()

        # calculo el indice que le corresponde a esa letra dentro del
        # vector de contadores, usando el codigo ascii de la letra
        # (ord) y restandole el codigo ascii de la "A"
        indice = ord(letra) - ord("A")

        # controlo que el indice este dentro del rango del vector
        # (por las dudas de que venga algun caracter raro)
        if indice >= 0 and indice < 26:
            contadores[indice] = contadores[indice] + 1

    return contadores


def obtener_letra_mas_frecuente(contadores):
    # r2.2 y r2.3: recorro el vector de 26 contadores buscando "a
    # mano" cual es el mayor (no uso la funcion max() porque el
    # enunciado pide programar nosotros las busquedas)

    indice_del_mayor = 0  # arranco suponiendo que el mayor es la "A"

    for indice in range(1, 26):
        if contadores[indice] > contadores[indice_del_mayor]:
            indice_del_mayor = indice

    # una vez que tengo el indice del mayor, reconstruyo la letra
    # (el proceso inverso al de la funcion anterior)
    letra_mas_frecuente = chr(ord("A") + indice_del_mayor)
    cantidad_de_esa_letra = contadores[indice_del_mayor]

    return letra_mas_frecuente, cantidad_de_esa_letra


def obtener_dni_mayor_monto_alta_complejidad(tratamientos):
    # r2.4: recorro el vector buscando, entre los tratamientos de
    # alta complejidad, cual tiene el mayor monto_final, y me quedo
    # con el dni de ese tratamiento

    dni_del_mayor = None
    mayor_monto_encontrado = -1  # arranco con un valor imposible (negativo)

    for tratamiento in tratamientos:
        if tratamiento.es_alta_complejidad():
            if tratamiento.monto_final > mayor_monto_encontrado:
                mayor_monto_encontrado = tratamiento.monto_final
                dni_del_mayor = tratamiento.dni

    return dni_del_mayor


def mostrar_resultados_opcion_2(tratamientos):
    # calculo cada uno de los 4 resultados que pide el enunciado

    diferencia_promedio = calcular_diferencia_promedio(tratamientos)
    contadores_por_letra = contar_tratamientos_por_letra(tratamientos)
    letra_mas_frecuente, cantidad_letra_mas_frecuente = obtener_letra_mas_frecuente(contadores_por_letra)
    dni_mayor_monto = obtener_dni_mayor_monto_alta_complejidad(tratamientos)

    # y los muestro en el orden pedido, con los dos puntos como
    # separador entre el texto y el valor
    print("r2.1:", round(diferencia_promedio, 2))
    print("r2.2:", letra_mas_frecuente)
    print("r2.3:", cantidad_letra_mas_frecuente)
    print("r2.4:", dni_mayor_monto)


def opcion_mostrar_resultados(tratamientos):
    # funcion orquestadora de la opcion 2 del menu
    mostrar_resultados_opcion_2(tratamientos)


# ==================================================================
# MENU PRINCIPAL
# ==================================================================

def mostrar_menu():
    # muestro las opciones disponibles. El texto de cada opcion es
    # libre, lo unico que el enunciado exige textual es el cartel
    # "Ingrese opción:" que va despues, al pedir el input()
    print("1) Cargar Tratamientos")
    print("2) Mostrar Resultados")
    print("0) Salir")


def main():
    # vector de tratamientos, arranca vacio hasta que el usuario elija
    # la opcion 1 y se cargue desde el archivo
    tratamientos = []

    # variable de control del ciclo del menu. La inicializo en
    # cualquier valor distinto de 0 para que entre al while por lo
    # menos una vez
    opcion = -1

    while opcion != 0:
        mostrar_menu()

        # esta es la UNICA carga por teclado permitida en todo el
        # programa: el numero de opcion elegida
        opcion = int(input("Ingrese opción: "))

        if opcion == 1:
            tratamientos = opcion_cargar_tratamientos()
        elif opcion == 2:
            opcion_mostrar_resultados(tratamientos)
        elif opcion == 0:
            # no hago nada especial aca, el while corta solo porque
            # la condicion opcion != 0 pasa a ser False
            pass
        else:
            print("Opción inválida")


# esto hace que main() se ejecute solo cuando este archivo se corre
# directamente (y no cuando se importa desde otro modulo)
if __name__ == "__main__":
    main()