import clase

def es_alt_complejidad(com):
    # cambiamos lo de alta complejidad del tp2 
    # TP3 Alta complejidad 'A'
    return com.strip().upper() == "A"
    #de vuelve true o false si cumple la condición


def cal_por_nor(icd10):
    if "." in icd10:
        par = icd10.split(".")
        if len(par) > 1 and par[1].isdigit():
            return int(par[1])
    return 0


# TP3 AGREGADO: Algoritmo ID 1
def alg_1(mnt_bas, icd10, es_alt):
    sum_fij = 0.0
    if mnt_bas <= 60000:
        por_ext = 0
    else:
        por_ext = cal_por_nor(icd10)
        if es_alt and icd10[0].upper() != "U":
            sum_fij = mnt_bas / 2.0

    mnt_ext = (mnt_bas * por_ext / 100.0) + sum_fij
    return mnt_bas + mnt_ext


# TP3 AGREGADO: Algoritmo ID 2
def alg_2(mnt_bas, icd10, es_alt):
    let = icd10[0].upper()
    if "A" <= let <= "P":
        por_ext = cal_por_nor(icd10)
    else:
        if es_alt:
            por_ext = cal_por_nor(icd10) * 2
        else:
            por_ext = 15

    return mnt_bas + (mnt_bas * por_ext / 100.0)


# TP3 AGREGADO: Algoritmo ID 3
def alg_3(mnt_bas, icd10, es_alt):
    mnt_ext = 0.0
    if es_alt:
        mnt_ext += mnt_bas * 0.30

    let = icd10[0].upper()
    if "A" <= let <= "L":
        mnt_ext += 20000.0
    elif "M" <= let <= "P":
        mnt_ext += 15000.0 + 5000.0
    else:
        mnt_ext += mnt_bas * 0.10

    if mnt_ext > 60000:
        mnt_ext = 60000.0

    return mnt_bas + mnt_ext


# TP3 Monto final
def cal_mnt_fin(mnt_bas, icd10, comp, ide_alg):
    es_alt = es_alt_complejidad(comp)

    if ide_alg == 1:
        mnt = alg_1(mnt_bas, icd10, es_alt)
    elif ide_alg == 2:
        mnt = alg_2(mnt_bas, icd10, es_alt)
    elif ide_alg == 3:
        mnt = alg_3(mnt_bas, icd10, es_alt)
    else:
        por = cal_por_nor(icd10)
        mnt = mnt_bas + (mnt_bas * por / 100.0)

    return round(mnt, 2)


#opcion 1
def opcion1():
    vec = []
    can_alt_com = 0
    qui_ape = "No hay suficientes tratamientos de alta complejidad."

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
            icd10 = par[3].strip()
            mnt_bas = float(par[4].strip())
            
            comp = par[5].strip()
            ide_alg = int(par[6].strip())  # TP3 AGREGADO
            # R2
            #si el tratamiento del CSV es de alta complejidad A
            if es_alt_complejidad(comp):
                #Si es de alta complejidad cuenta + 1
                can_alt_com += 1
                # Si es justo el quinto tratamiento de alta complejidad que encontramos:
                if can_alt_com == 5:
                    #Guardamos el apellido del paciente para el resultado r1.2
                    qui_ape = ape

            # TP3 AGREGADO: Objeto Tratamiento ruway
            obj = clase.Tratamiento(dni, nom, ape, icd10, mnt_bas, comp, ide_alg)
            obj.mnt_final = cal_mnt_fin(mnt_bas, icd10, comp, ide_alg)

            vec.append(obj)

    arc.close()

    print("r1.1:", len(vec))
    print("r1.2:", qui_ape)

    return vec


def opcion2(vec):
    if len(vec) == 0:
        return

    # r.2.1: Diferencia promedio
    sum_dif = 0.0
    for obj in vec:
        sum_dif += (obj.mnt_final - obj.mnt_base)
    r2_1 = round(sum_dif / len(vec), 2)

    # r.2.2 y r.2.3: Letra tratamiento
    con_let = [0] * 26
    for obj in vec:
        let = obj.icd10[0].upper()
        if "A" <= let <= "Z":
            idx = ord(let) - ord("A")
            con_let[idx] += 1

    max_can = -1
    idx_max = -1
    for i in range(26):
        if con_let[i] > max_can:
            max_can = con_let[i]
            idx_max = i

    r2_2 = chr(ord("A") + idx_max)
    r2_3 = max_can

    may_mnt = -1.0
    dni_may = None

    # Recorremos cada objeto Tratamiento en el vector
    for obj in vec:
        #verificamos solo los tratamientos que son de alta complejidad A
        if es_alt_complejidad(obj.complejidad):
            # Buscamos el mayor monto final entre ellos
            if obj.mnt_final > may_mnt:
                may_mnt = obj.mnt_final
                dni_may = obj.dni

    # Guardamos el DNI encontrado para el resultado r2.4
    r2_4 = dni_may

    print("r.2.1:", r2_1)
    print("r.2.2:", r2_2)
    print("r.2.3:", r2_3)
    print("r.2.4:", r2_4)


def mos_men():
    print("===== SISTEMA DE GESTION DE TRATAMIENTOS =====")
    print("1 - Cargar tratamientos")
    print("2 - Mostrar resultados")
    print("0 - Salir")


def principal():
    vec_tra = []
    opcion = -1

    while opcion != 0:
        mos_men()
        opcion_ing = input("Ingrese opción:")

        # verificamos si lo que ingresso el usuario por teclado es la opción "0" "1" o "2"
        if opcion_ing == "0" or opcion_ing == "1" or opcion_ing == "2":
            # Si es una de esas opciones convierte el texto string a número entero (int)
            opcion = int(opcion_ing)
        else:
            continue
        if opcion == 1:
            vec_tra = opcion1()
        elif opcion == 2:
            opcion2(vec_tra)


if __name__ == "__main__":
    principal()

