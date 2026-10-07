import clase
import os


def _alt_complejidad(com):
    # cambiamos lo de alta complejidad del tp2
    # TP3 Alta complejidad 'A'
    return com.strip().upper() == "A"
    # de vuelve true o false si cumple la condición

def _por_nor(ic10):
    if "." in ic10:
        par = ic10.split(".")  # crea una lista de dos indices [0,1]
        if len(par) > 1 and par[1] != "":
            # Revisamos que TODOS sean dígitos
            for c in par[1]:
                if not ('0' <= c <= '9'):  # --> comparamos con caracteres
                    return 0
            return int(par[1])
    return 0


# TP1/TP2 AGREGADO: Obtener bloque numérico ICD10 para algoritmo 3
def _bloque(ic10):
    if "." in ic10:
        _str = ic10.split(".")[0][1:]
        if _str != "":
            for c in _str:
                if not ('0' <= c <= '9'):
                    return 0
            return int(_str)
    return 0


# TP3 AGREGADO: Algoritmo ID 1
def _1(t_bas, ic10, _alt):
    _fij = 0.0
    if t_bas <= 60000:
        _ext = 0
    # verificamos que efectivamente monto base sea mayor a 60mil
    if t_bas > 60000:
        # porcentaje extra es igual al calculo normal
        _ext = _por_nor(ic10)
        if _alt and ic10[0].upper() != "U":
            _fij = t_bas / 2.0

    _ext = t_bas * (_ext / 100.0) + _fij
    return t_bas + _ext


# TP3 Tabla de algoritmo de calculo monto final 2| cuando icd10 esta entre A y P Algoritmo ID 2
def _2(t_bas, ic10, _alt):
    let = ic10[0].upper()
    if "A" <= let <= "P":
        _ext = _por_nor(ic10)
    else:
        if _alt:
            _ext = _por_nor(ic10) * 2
        else:
            _ext = 15

    return t_bas + t_bas * (_ext / 100.0)


# TP3 AGREGADO: Algoritmo ID 3
def _3(t_bas, ic10, _alt):
    _ext = 0.0
    if _alt:
        _ext += t_bas * 0.30

    let = ic10[0].upper()
    if "A" <= let <= "L":
        _ext += 20000.0
    elif "M" <= let <= "P":
        blque = _bloque(ic10)
        _ext += 15000.0 + (5000.0 * blque)
    else:
        _ext += t_bas * 0.10

    if _ext > 60000:
        _ext = 60000.0

    return t_bas + _ext


# TP1/TP2 lo que nos faltaba algoritmo normal (calculo original del TP1yTP2 con adicionales fijos)
def _normal_tp1(t_bas, ic10, comp):
    #_alt = _alt_complejidad(comp)
    let = ic10[0].upper()
    # Regla del TP1: base + 25000 fijos + monto según la letra
    _letra = 25000
    # TP1: Adicionales fijos segun grupo de letras
    if "A" <= let <= "L":
        _letra += 25000.0
    elif let == "U":
        _letra += 100000.0
    else:  # M a Z excluyendo U
        _letra += 40000.0

    _base_con_letra = t_bas + _letra
    po_centaje = _por_nor(ic10)
    _total = (_base_con_letra / 100.0) * po_centaje
    su_total = _base_con_letra + _total
    #TP1 Si es Alta Complejidad 'A' se suma el adicional por letra nuevamente ESTO LO QUITE 
    #if _alt:
     #   su_total += _letra
    return su_total

# TP3 Monto final
def _mnt_fin(t_bas, ic10, comp, _alg):
    _alt = _alt_complejidad(comp)

    if _alg == 1:
        mnt = _1(t_bas, ic10, _alt)
    elif _alg == 2:
        mnt = _2(t_bas, ic10, _alt)
    elif _alg == 3:
        mnt = _3(t_bas, ic10, _alt)
    else:
        # TP1/TP2 AGREGADO: Cálculo normal usando las reglas del TP1
        mnt = _normal_tp1(t_bas, ic10, comp)

    return round(mnt, 2)


# opcion 1
def opion1():

    vec = []
    _alt_com = 0
    _ape = "No hay suficientes tratamientos de alta complejidad."

    # validacion de la existencia del archivo
    _archivo = "tratamientos.csv"
    if not os.path.exists(_archivo):
        print(f"Error: El archivo {_archivo} no fue encontrado.")
        return vec  # o se sale de la funcion

    arc = open("tratamientos.csv", "r")

    # TP3 AGREGADO cabecera
    enc = arc.readline()

    for lin in arc:
        lin = lin.strip()
        if len(lin) == 0:
            continue

        par = lin.split(",")
        if len(par) >= 7:
            dni = int(par[0].strip())
            nom = par[1].strip()
            ape = par[2].strip()
            ic10 = par[3].strip()
            t_bas = float(par[4].strip())

            comp = par[5].strip()
            _alg = int(par[6].strip())  # TP3 AGREGADO
            # R2
            # si el tratamiento del CSV es de alta complejidad A
            if _alt_complejidad(comp):
                # Si es de alta complejidad cuenta + 1
                _alt_com += 1
                # Si es justo el quinto tratamiento de alta complejidad que encontramos:
                if _alt_com == 5:
                    # Guardamos el apellido del paciente para el resultado r1.2
                    _ape = ape

            # TP3 AGREGADO: Objeto Tratamiento ruway
            obj = clase.Tratamiento(dni, nom, ape, ic10, t_bas, comp, _alg)
            obj.mnt_final = _mnt_fin(t_bas, ic10, comp, _alg)

            vec.append(obj)

    arc.close()

    print("r1.1:", len(vec))
    print("r1.2:", _ape)

    return vec


def opion2(vec):
    if len(vec) == 0:
        return

    # r.2.1: Diferencia promedio
    _dif = 0.0
    for obj in vec:
        _dif += (obj.mnt_final - obj.mnt_base)
    r2_1 = round(_dif / len(vec), 2)

    # r.2.2 y r.2.3: Letra más frecuente
    lt_ras = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    _let = [0] * 26

    for obj in vec:
        let = obj.icd10[0].upper()
        # Buscamos la posición de la letra en la cadena
        pos = 0
        while pos < 26 and lt_ras[pos] != let:
            pos += 1
        if pos < 26:  # letra válida
            _let[pos] += 1

    _can = -1
    _max = -1
    for i in range(26):
        if _let[i] > _can:
            _can = _let[i]
            _max = i

    # Recuperamos la letra directamente desde la cadena
    r2_2 = lt_ras[_max]
    r2_3 = _can

    # r.2.4: DNI del mayor monto final entre alta complejidad
    _mnt = -1
    _mayor = None

    for obj in vec:
        if _alt_complejidad(obj.complejidad):
            if obj.mnt_final > _mnt:
                _mnt = obj.mnt_final
                _mayor = obj.dni

    r2_4 = _mayor

    print("r.2.1:", r2_1)
    print("r.2.2:", r2_2)
    print("r.2.3:", r2_3)
    print("r.2.4:", r2_4)


def _men():
    print("1 - Cargar tratamientos")
    print("2 - Mostrar resultados")
    print("0 - Salir")


def prncipal():
    _tra = []
    opion = -1

    while opion != 0:
        _men()
        _ing = int(input("Ingrese opción: "))

        if _ing == 0:
            break
        elif _ing == 1:
            _tra = opion1()
        elif _ing == 2:
            opion2(_tra)


if __name__ == "__main__":
    prncipal()