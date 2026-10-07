# clase.py
# Acá defino la clase Tratamiento. Cada objeto de esta clase representa
# una linea del archivo tratamientos.csv, con todos sus datos, y ademas
# tiene los metodos que calculan el monto final segun el algoritmo que
# le corresponda (los que estan en la tabla del enunciado del TP3, mas
# el calculo "normal" que viene de la logica del TP2 para cuando el
# ID de algoritmo no es ninguno de los que estan en la tabla).

class Tratamiento:

    # ------------------------------------------------------------
    # Constructor: recibe los 7 datos que vienen en cada linea del
    # csv (ya parseados, es decir, con los tipos de datos correctos:
    # dni entero, monto_base flotante, id_algoritmo entero, etc) y
    # los guarda como atributos del objeto.
    # ------------------------------------------------------------
    def __init__(self, dni, nombre, apellido, icd10, monto_base, complejidad, id_algoritmo):
        self.dni = dni                      # numero de documento del paciente
        self.nombre = nombre                # nombre del paciente
        self.apellido = apellido            # apellido del paciente
        self.icd10 = icd10                  # codigo ICD10 del diagnostico, por ej "B83.5"
        self.monto_base = monto_base        # monto base/minimo a pagar (viene del csv)
        self.complejidad = complejidad      # "A" = alta complejidad, "R" = regular
        self.id_algoritmo = id_algoritmo    # numero de algoritmo a usar para el calculo

        # el monto final todavia no se calculo, lo dejo en 0 y se
        # completa despues llamando al metodo calcular_monto_final()
        self.monto_final = 0.0

    # ------------------------------------------------------------
    # Metodos "chiquitos" de ayuda, para no repetir codigo en cada
    # algoritmo. Todos trabajan sobre el codigo ICD10 del propio
    # objeto (self.icd10).
    # ------------------------------------------------------------

    def es_alta_complejidad(self):
        # devuelve True o False segun si el campo complejidad es "A"
        return self.complejidad == "A"

    def obtener_letra_icd10(self):
        # la letra del ICD10 es siempre el primer caracter del codigo
        # ej: "B83.5" -> "B"
        return self.icd10[0]

    def obtener_bloque_icd10(self):
        # el "bloque" son los digitos que estan entre la letra y el
        # punto. ej: "M15.2" -> bloque = 15
        # primero busco en que posicion esta el punto...
        posicion_del_punto = self.icd10.find(".")
        # ...y despues tomo la subcadena desde la posicion 1 (salteando
        # la letra) hasta el punto, y la convierto a entero
        bloque_como_texto = self.icd10[1:posicion_del_punto]
        return int(bloque_como_texto)

    def obtener_numero_decimal_icd10(self):
        # este es el numero que esta a la derecha del punto.
        # ej: "I10.6" -> devuelve 6
        posicion_del_punto = self.icd10.find(".")
        numero_como_texto = self.icd10[posicion_del_punto + 1:]
        return int(numero_como_texto)

    def letra_entre(self, letra_desde, letra_hasta):
        # chequea si la letra del icd10 esta en un rango alfabetico,
        # por ejemplo letra_entre("A","P") para saber si esta entre
        # la A y la P (incluidas las dos)
        letra = self.obtener_letra_icd10()
        return letra_desde <= letra <= letra_hasta

    # ------------------------------------------------------------
    # Calculo "normal" (esto es lo que en el enunciado del TP3 se
    # llama "en forma normal" o "de acuerdo a lo indicado en el TP2").
    #
    # OJO: en el TP2 el monto normal se calculaba sumando primero un
    # adicional fijo segun la letra del ICD10 (A-L / M-Z sin la U / U),
    # que venia definido en una linea especial del archivo de texto
    # (la linea que empezaba con "#"). En el TP3 esa linea especial
    # NO existe (el csv no la trae), por lo tanto para este TP el
    # "calculo normal" lo dejamos usando UNICAMENTE el monto base que
    # trae el csv, mas el porcentaje segun el numero a la derecha del
    # punto del ICD10 (que es lo unico de la formula del TP2 que se
    # puede seguir calculando con los datos que da el TP3).
    # ------------------------------------------------------------

    def calculo_normal_porcentaje_extra(self):
        # el porcentaje a aplicar es el numero que esta a la derecha
        # del punto del codigo icd10 (por ejemplo, para "F05.9" el
        # porcentaje es 9, o sea 9%)
        porcentaje = self.obtener_numero_decimal_icd10()
        # aplico ese porcentaje sobre el monto base
        porcentaje_extra = self.monto_base * porcentaje / 100
        return porcentaje_extra

    def calculo_normal_monto_final(self):
        # este es el calculo completo "a la TP2", se usa cuando el
        # id_algoritmo del tratamiento no figura en la tabla (o sea,
        # no es ni 1, ni 2, ni 3)
        porcentaje_extra = self.calculo_normal_porcentaje_extra()
        monto_final = self.monto_base + porcentaje_extra

        # en el TP2, si el tratamiento era de alta complejidad se le
        # sumaba un recargo del 5% en concepto de "seguro de vida"
        if self.es_alta_complejidad():
            monto_final = monto_final * 1.05

        return monto_final

    # ------------------------------------------------------------
    # A partir de aca, los 3 algoritmos que pide la tabla del
    # enunciado del TP3 (ID 1, ID 2 e ID 3)
    # ------------------------------------------------------------

    def algoritmo_1(self):
        # Algoritmo ID 1
        # Si el monto base es menor o igual a 60000 no hay porcentaje
        # extra ni suma fija, el monto final queda igual al monto base.
        if self.monto_base <= 60000:
            porcentaje_extra = 0
            suma_fija = 0
        else:
            # si el monto base supera los 60000, calculo el porcentaje
            # extra de la forma normal (la explicada arriba)
            porcentaje_extra = self.calculo_normal_porcentaje_extra()

            letra = self.obtener_letra_icd10()

            # la suma fija (mitad del monto base original) solo se
            # suma si el tratamiento es de alta complejidad Y ademas
            # la letra del icd10 no es "U". En cualquier otro caso la
            # suma fija queda en 0 (asi lo aclara la tabla del enunciado)
            if self.es_alta_complejidad() and letra != "U":
                suma_fija = self.monto_base / 2
            else:
                suma_fija = 0

        # formula final del algoritmo 1
        monto_final = self.monto_base + porcentaje_extra + suma_fija
        return monto_final

    def algoritmo_2(self):
        # Algoritmo ID 2

        # Caso 1: la letra del icd10 esta entre la A y la P (las dos
        # incluidas). En este caso no importa si es alta complejidad
        # o no, se usa el porcentaje extra "normal"
        if self.letra_entre("A", "P"):
            porcentaje_extra = self.calculo_normal_porcentaje_extra()
        else:
            # Caso 2: la letra NO esta entre A y P
            if self.es_alta_complejidad():
                # si es de alta complejidad, se duplica el numero que
                # esta a la derecha del punto del icd10 y ESE numero
                # duplicado es el porcentaje a aplicar
                numero_derecha_del_punto = self.obtener_numero_decimal_icd10()
                numero_duplicado = numero_derecha_del_punto * 2
                porcentaje_extra = self.monto_base * numero_duplicado / 100
            else:
                # si NO es de alta complejidad, el porcentaje extra es
                # directamente un 15% fijo del monto base
                porcentaje_extra = self.monto_base * 0.15

        # formula final del algoritmo 2 (este algoritmo no usa suma fija)
        monto_final = self.monto_base + porcentaje_extra
        return monto_final

    def algoritmo_3(self):
        # Algoritmo ID 3

        # primero calculo el monto_extra que depende de la complejidad
        if self.es_alta_complejidad():
            # si es de alta complejidad, arranco con un 30% del monto base
            monto_extra = self.monto_base * 0.30
        else:
            # si no es de alta complejidad, arranco de 0
            monto_extra = 0

        # ahora, sin importar la complejidad, le sumo algo mas al
        # monto_extra segun en que rango cae la letra del icd10
        letra = self.obtener_letra_icd10()

        if "A" <= letra <= "L":
            # letra entre A y L -> se suma un monto fijo de 20000
            monto_extra = monto_extra + 20000
        elif "M" <= letra <= "P":
            # letra entre M y P -> se suma 15000 mas 5000 por cada
            # unidad del "bloque" del icd10 (los numeros entre la
            # letra y el punto)
            bloque = self.obtener_bloque_icd10()
            monto_extra = monto_extra + 15000 + 5000 * bloque
        else:
            # cualquier otra letra (fuera de A-P) -> se suma un 10%
            # del monto base
            monto_extra = monto_extra + self.monto_base * 0.10

        # si el monto_extra termina superando los 60000, se limita
        # (se "capea") a 60000 como maximo
        if monto_extra > 60000:
            monto_extra = 60000

        # formula final del algoritmo 3
        monto_final = self.monto_base + monto_extra
        return monto_final

    # ------------------------------------------------------------
    # Este es el metodo "despachador": mira el id_algoritmo del
    # tratamiento y decide a que metodo llamar. El resultado se
    # guarda en self.monto_final para no tener que recalcularlo
    # cada vez que se necesite.
    # ------------------------------------------------------------
    def calcular_monto_final(self):
        if self.id_algoritmo == 1:
            self.monto_final = self.algoritmo_1()
        elif self.id_algoritmo == 2:
            self.monto_final = self.algoritmo_2()
        elif self.id_algoritmo == 3:
            self.monto_final = self.algoritmo_3()
        else:
            # cualquier otro id de algoritmo que no sea 1, 2 o 3 usa
            # el calculo normal (heredado del TP2)
            self.monto_final = self.calculo_normal_monto_final()

        return self.monto_final


# Esto es solo para poder probar el modulo de forma individual, sin
# tener que correr todo el programa principal. Si este archivo se
# ejecuta directamente (y no se importa desde otro modulo), arma un
# tratamiento de prueba y muestra su monto final por consola.
if __name__ == "__main__":
    tratamiento_de_prueba = Tratamiento(1, "Juan", "Perez", "F05.9", 10000, "R", 99)
    tratamiento_de_prueba.calcular_monto_final()
    print(tratamiento_de_prueba.monto_final)