class Afiliado:
    def __init__(self, dni, obra_social, nivel, tope):
        self.dni = dni
        self.obra_social = obra_social
        self.nivel = nivel
        self.tope = tope

    def __str__(self):
        return "Afiliado(" + str(self.dni) + ", OS " + str(self.obra_social) + \
               ", nivel " + str(self.nivel) + ", tope " + str(self.tope) + ")"


class Tratamiento:
    def __init__(self, dni, nombre, apellido, icd, monto_base, complejidad, id_algoritmo):
        self.dni = dni
        self.nombre = nombre
        self.apellido = apellido
        self.icd = icd
        self.monto_base = monto_base
        self.complejidad = complejidad
        self.id_algoritmo = id_algoritmo

    def __str__(self):
        return "Tratamiento(" + str(self.dni) + ", " + self.nombre + " " + self.apellido + \
               ", " + self.icd + ", " + str(self.monto_base) + ", " + self.complejidad + \
               ", alg " + str(self.id_algoritmo) + ")"
