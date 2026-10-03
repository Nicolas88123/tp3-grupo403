class Tratamiento:
    def __init__(self, dni, nom, ape, icd10, mnt_bas, comp, ide_alg):
        self.dni = dni
        self.nombre = nom
        self.apellido = ape
        self.icd10 = icd10
        self.mnt_base = mnt_bas #monto base
        self.complejidad = comp
        self.identifi_algoritmo = ide_alg
        self.mnt_final = 0.0 #monto final

    def __str__(self):
        r = "{:<13}".format("Dni: " + str(self.dni))
        r += "{:<26}".format("Paciente: " + self.nombre + " " + self.apellido)
        r += "{:<20}".format("ICD10: " + self.icd10)
        r += "{:<20}".format("Monto Base: " + str(self.mnt_base))
        r += "{:<16}".format("Complejidad: " + self.complejidad)
        r += "{:<16}".format("Algoritmo: " + str(self.identifi_algoritmo))
        r += "{:<26}".format("Monto Final: " + str(self.mnt_final))
        return r
