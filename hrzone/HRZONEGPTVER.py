#==============================zona de funciones=================================================
def maxhera(age):
    return 208 - 0.7 * age

def storagex():
    tamaño = int(input("Ingrese la cantidad de ejercicios realizados: "))
    return {f"ejercicio número {i+1}": int(input(f"Ingresa la frecuencia cardiaca para el ejercicio número {i+1}: ")) for i in range(tamaño)}

def calculate_zones(xr6, maxhera):
    resuldicc = {}
    resul = []
    zones = [
        (50, "Por debajo de la zona de trabajo (menos del '50%' de FCmáx)", "Por debajo de la zona de trabajo"),
        (60, "Z1 < 60% (Recuperación o Ritmo Suave)", "Z1"),
        (70, "Z2 < 70% (Resistencia Aeróbica)", "Z2"),
        (80, "Z3 < 80% (Tempo o Ritmo Moderado)", "Z3"),
        (90, "Z4 < 90% (Umbral Anaeróbico)", "Z4"),
        (100, "Z5 < 100% (Capacidad Anaeróbica o Esfuerzo Máximo)", "Z5")
    ]

    for x, (clave, valor) in enumerate(xr6.items(), start=1):
        porcent = (valor / maxhera) * 100
        for limit, zon, state in zones:
            if porcent < limit:
                break
        else:
            zon, state = "Por encima de la FCmáx (valor no válido)", "Por encima de la FCmáx"

        resuldicc[f"xr #{x}"] = state
        resul.append(f"el entrenamiento numero {x} se realizo en la zona {zon}")

    return resuldicc, resul

def print_results(resul):
    print("Resultados completos:\n")
    for j in resul:
        print(f"• {j}")

def ztwocalc(maxhera):
    fcztwo = maxhera * 0.7
    print(f"\nLa frecuencia cardiaca promedio para un entrenamiento en la zona 2 (Z2) es de {fcztwo:.2f} bpm")

def zonesort(resuldicc):
    zone_counts = {key: 0 for key in ["Por debajo de la zona de trabajo", "Z1", "Z2", "Z3", "Z4", "Z5"]}
    lstsze = len(resuldicc)

    for state in resuldicc.values():
        if state in zone_counts:
            zone_counts[state] += 1

    print(f"\nSe realizaron {lstsze} ejercicios")
    for zone, count in zone_counts.items():
        print(f"• {(count * 100) / lstsze:.2f}% ejercicios se realizaron en la zona {zone}")

#================zona de ejecución=====================================================
agedat = int(input("Introduce tu edad: "))
max_hera = maxhera(agedat)
print(f"Tu frecuencia cardiaca máxima estimada es {max_hera:.2f} bpm")

xr6 = storagex()
resuldicc, resul = calculate_zones(xr6, max_hera)

print_results(resul)
ztwocalc(max_hera)
zonesort(resuldicc)

#codigo escrito y testeado por github CoPilot#
