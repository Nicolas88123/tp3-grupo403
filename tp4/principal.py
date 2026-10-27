"""principal.py - Programa principal del TP4."""
from modelos import Afiliado, Tratamiento


# ---------------------------------------------------------------------------
# FUNCIONES PARA INTERPRETAR EL CÓDIGO ICD10 (formato X##.##)
# ---------------------------------------------------------------------------

def obtener_letra(icd):
    return icd[0]


def obtener_bloque(icd):
    return int(icd[1:3])


def obtener_numero_enfermedad(icd):
    return int(icd[4:])


def letra_entre(letra, desde, hasta):
    return desde <= letra <= hasta


# ---------------------------------------------------------------------------
# CÁLCULO DEL MONTO FINAL
# ---------------------------------------------------------------------------

def adicional_por_letra(letra):
    # A-L -> 25000 | M-Z (sin U) -> 40000 | U -> 100000
    if letra == "U":
        return 100000
    if letra_entre(letra, "A", "L"):
        return 25000
    return 40000


def subtotal_normal(monto_base, icd):
    return monto_base + 25000 + adicional_por_letra(obtener_letra(icd))


def porcentaje_extra_normal(monto_base, icd):
    return subtotal_normal(monto_base, icd) * obtener_numero_enfermedad(icd) / 100


def calculo_tp1(monto_base, icd):
    return subtotal_normal(monto_base, icd) + porcentaje_extra_normal(monto_base, icd)


def algoritmo_1(monto_base, icd, complejidad):
    letra = obtener_letra(icd)
    porcentaje_extra = 0
    suma_fija = 0
    if monto_base > 60000:
        porcentaje_extra = porcentaje_extra_normal(monto_base, icd)
        if complejidad == "A" and letra != "U":
            suma_fija = monto_base / 2
    return monto_base + porcentaje_extra + suma_fija


def algoritmo_2(monto_base, icd, complejidad):
    letra = obtener_letra(icd)
    if letra_entre(letra, "A", "P"):
        porcentaje_extra = porcentaje_extra_normal(monto_base, icd)
    else:
        if complejidad == "A":
            n = obtener_numero_enfermedad(icd) * 2
            porcentaje_extra = subtotal_normal(monto_base, icd) * n / 100
        else:
            porcentaje_extra = monto_base * 15 / 100
    return monto_base + porcentaje_extra


def algoritmo_3(monto_base, icd, complejidad):
    letra = obtener_letra(icd)
    monto_extra = 0
    if complejidad == "A":
        monto_extra = monto_base * 30 / 100
    if letra_entre(letra, "A", "L"):
        monto_extra += 20000
    elif letra_entre(letra, "M", "P"):
        monto_extra += 15000 + 5000 * obtener_bloque(icd)
    else:
        monto_extra += monto_base * 10 / 100
    if monto_extra > 60000:
        monto_extra = 60000
    return monto_base + monto_extra


def calcular_monto_final(trat):
    if trat.id_algoritmo == 1:
        return algoritmo_1(trat.monto_base, trat.icd, trat.complejidad)
    if trat.id_algoritmo == 2:
        return algoritmo_2(trat.monto_base, trat.icd, trat.complejidad)
    if trat.id_algoritmo == 3:
        return algoritmo_3(trat.monto_base, trat.icd, trat.complejidad)
    return calculo_tp1(trat.monto_base, trat.icd)


def porcentaje_cobertura(nivel, complejidad):
    if complejidad == "A":
        if nivel == 1:
            return 40
        if nivel == 2:
            return 60
        return 80
    if nivel == 1:
        return 50
    if nivel == 2:
        return 70
    return 90


# ---------------------------------------------------------------------------
# OPCIÓN 1: CARGA DE AFILIADOS CON INSERCIÓN ORDENADA
# ---------------------------------------------------------------------------

def insertar_ordenado(vector, nuevo):
    """
    Inserción ordenada por DNI (ascendente), sin sort():
    1) agrego el elemento al final (se crea un lugar libre),
    2) recorro hacia atrás desplazando una posición a la derecha
       a todos los que tengan DNI mayor que el nuevo,
    3) dejo el nuevo en el hueco que quedó.
    """
    vector.append(nuevo)
    i = len(vector) - 1
    while i > 0 and vector[i - 1].dni > nuevo.dni:
        vector[i] = vector[i - 1]
        i -= 1
    vector[i] = nuevo


def cargar_afiliados():
    """Lee coberturas.csv línea por línea y devuelve el vector ordenado por DNI."""
    vector = []
    archivo = open("coberturas.csv", "rt", encoding="utf-8")
    primera = True
    for linea in archivo:
        if primera:             # la primera línea (encabezado) se ignora
            primera = False
            continue
        linea = linea.strip()
        if linea == "":
            continue
        campos = linea.split(",")
        afiliado = Afiliado(int(campos[0]), int(campos[1]), int(campos[2]), float(campos[3]))
        insertar_ordenado(vector, afiliado)
    archivo.close()
    return vector


# ---------------------------------------------------------------------------
# OPCIÓN 2: CARGA DE TRATAMIENTOS (mismo orden que el archivo)
# ---------------------------------------------------------------------------

def cargar_tratamientos():
    vector = []
    archivo = open("tratamientos.csv", "rt", encoding="utf-8")
    primera = True
    for linea in archivo:
        if primera:
            primera = False
            continue
        linea = linea.strip()
        if linea == "":
            continue
        c = linea.split(",")
        trat = Tratamiento(int(c[0]), c[1], c[2], c[3], float(c[4]), c[5], int(c[6]))
        vector.append(trat)
    archivo.close()
    return vector


# ---------------------------------------------------------------------------
# BÚSQUEDA BINARIA POR DNI
# ---------------------------------------------------------------------------

def buscar_afiliado(vector, dni):
    """
    Búsqueda binaria: devuelve el índice del afiliado con ese DNI,
    o -1 si no está. Funciona porque el vector está ordenado por DNI.
    """
    izq = 0
    der = len(vector) - 1
    while izq <= der:
        medio = (izq + der) // 2
        if vector[medio].dni == dni:
            return medio
        if dni < vector[medio].dni:
            der = medio - 1
        else:
            izq = medio + 1
    return -1


# ---------------------------------------------------------------------------
# OPCIÓN 3: RESULTADOS
# ---------------------------------------------------------------------------

def calcular_cobertura(trat, monto_final, afiliados):
    """
    Devuelve (monto_cubierto, tope_aplicado, indice_afiliado) para un tratamiento.
    Si el paciente no es afiliado: (0, False, -1).
    """
    pos = buscar_afiliado(afiliados, trat.dni)
    if pos == -1:
        return 0, False, -1

    afi = afiliados[pos]
    cubierto = monto_final * porcentaje_cobertura(afi.nivel, trat.complejidad) / 100
    tope_aplicado = False
    if cubierto > afi.tope:
        cubierto = afi.tope
        tope_aplicado = True
    return cubierto, tope_aplicado, pos


def mostrar_resultados(afiliados, tratamientos):
    total_cubierto = 0
    total_no_cubierto = 0
    cant_topes = 0
    cant_no_afiliados = 0

    # Un acumulador por obra social (índices 1..20; el 0 no se usa)
    cubierto_por_os = [0] * 21

    mayor_no_cubierto = -1
    dni_mayor_no_cubierto = 0

    for trat in tratamientos:
        final = calcular_monto_final(trat)
        cubierto, tope, pos = calcular_cobertura(trat, final, afiliados)
        no_cubierto = final - cubierto

        total_cubierto += cubierto
        total_no_cubierto += no_cubierto

        if tope:
            cant_topes += 1

        if pos == -1:
            cant_no_afiliados += 1
        else:
            cubierto_por_os[afiliados[pos].obra_social] += cubierto

        # '>' estricto: en caso de empate queda el primero encontrado
        if no_cubierto > mayor_no_cubierto:
            mayor_no_cubierto = no_cubierto
            dni_mayor_no_cubierto = trat.dni

    # Obra social que más cubrió: recorro de menor a mayor código con '>' estricto,
    # así en caso de empate gana el de menor código.
    mejor_os = 1
    mejor_monto = cubierto_por_os[1]
    for cod in range(2, 21):
        if cubierto_por_os[cod] > mejor_monto:
            mejor_monto = cubierto_por_os[cod]
            mejor_os = cod

    print("r3.1:", round(total_cubierto, 2))
    print("r3.2:", round(total_no_cubierto, 2))
    print("r3.3:", cant_topes)
    print("r3.4:", cant_no_afiliados)
    print("r3.5:", mejor_os)
    print("r3.6:", dni_mayor_no_cubierto)


# ---------------------------------------------------------------------------
# MENÚ
# ---------------------------------------------------------------------------

def mostrar_menu():
    print("1. Cargar afiliados")
    print("2. Cargar tratamientos")
    print("3. Mostrar resultados")
    print("0. Salir")


def principal():
    afiliados = []
    tratamientos = []
    afiliados_cargados = False
    tratamientos_cargados = False

    opcion = -1
    while opcion != 0:
        mostrar_menu()
        opcion = int(input("Ingrese opción: "))

        if opcion == 1:
            afiliados = cargar_afiliados()      # se regenera desde cero
            afiliados_cargados = True
        elif opcion == 2:
            tratamientos = cargar_tratamientos()  # se regenera desde cero
            tratamientos_cargados = True
        elif opcion == 3:
            if afiliados_cargados and tratamientos_cargados:
                mostrar_resultados(afiliados, tratamientos)
            else:
                print("Error: primero debe cargar los afiliados (1) y los tratamientos (2).")


if __name__ == "__main__":
    principal()
