# Función para calcular la frecuencia cardiaca máxima
def maxhera(age):
    global maxhera
    maxhera = 208 - 0.7 * age

# Solicitar la edad del usuario y ejecutar la funcion de fc máxima
agedat = int(input("Introduce tu edad: "))
maxhera(agedat)
# Calcular y mostrar la frecuencia cardiaca máxima estimada
print(f"Tu frecuencia cardiaca máxima estimada es {maxhera:.2f} bpm")

# Solicitar la frecuencia cardiaca durante el entrenamiento
hr = float(input("Introduce tu frecuencia cardiaca durante el entrenamiento (bpm): "))

# para poder dterminar las zonas primero debemos
# crear unos percentiles que correspondan a la 
# frecuencia cardiaca máxima que puede tomar la persona
# una vez hecho eso se multiplica este valor (equivalente al 1%) por
# la frecuencia cardiaca registrada durante el ejercicio, nos arrojara
# el porcentaje correspondiente 
porcent = (hr / maxhera) * 100

# el porcentaje es comparados con los porcentajes establecidos para las zonas
if porcent < 50:
    zon = "Por debajo de la zona de trabajo (menos del '50%' de FCmáx)"
elif porcent < 60:
    zon = "Z1 (Recuperación o Ritmo Suave)"
elif porcent < 70:
    zon = "Z2 (Resistencia Aeróbica)"
elif porcent < 80:
    zon = "Z3 (Tempo o Ritmo Moderado)"
elif porcent < 90:
    zon = "Z4 (Umbral Anaeróbico)"
elif porcent <= 100:
    zon = "Z5 (Capacidad Anaeróbica o Esfuerzo Máximo)"
else:
    zon = "Por encima de la FCmáx (valor no válido)"

print(f"Tu entrenamiento se realizó en la zon: {zon}")
