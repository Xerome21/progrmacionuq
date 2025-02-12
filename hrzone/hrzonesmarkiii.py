# Función para calcular la frecuencia cardiaca máxima
def maxhera(age):
    global maxhera
    maxhera = 208 - 0.7 * age

def storagex():
    global xr6
    # Solicitar el tamaño del diccionario
    tamaño = int(input("Ingrese la cantidad de ejercicios realizados: "))

# Crear un diccionario vacío
    xr6 = {}

# Llenar el diccionario con entradas proporcionadas por el usuario
    for i in range(tamaño):
        clave = f"ejercicio número {i+1}"
        valor = int(input(f"Ingresa la frecuencia cardiaca para el {clave}: "))
        xr6[clave] = valor

# Mostrar el diccionario creado



#===============================================================================

# Solicitar la edad del usuario y ejecutar la funcion de fc máxima
agedat = int(input("Introduce tu edad: "))
maxhera(agedat)
# Calcular y mostrar la frecuencia cardiaca máxima estimada
print(f"Tu frecuencia cardiaca máxima estimada es {maxhera:.2f} bpm")

storagex()


# Solicitar la frecuencia cardiaca durante el entrenamiento
        #hr = float(input("Introduce tu frecuencia cardiaca durante el entrenamiento (bpm): "))

# para poder dterminar las zonas primero debemos
# crear unos percentiles que correspondan a la 
# frecuencia cardiaca máxima que puede tomar la persona
# una vez hecho eso se multiplica este valor (equivalente al 1%) por
# la frecuencia cardiaca registrada durante el ejercicio, nos arrojara
# el porcentaje correspondiente 
def resultmatrix():
    global zon
    resul = []    
    x = 0


# el porcentaje es comparados con los porcentajes establecidos para las zonas


# Crear una lista vacía


# Llenar la lista con elementos ingresados por el usuario
    for i in xr6.values():
        porcent = ( i / maxhera) * 100  
              
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
        
        x = x + 1     
        elemento = f"el entrenamiento numero {x} se realizo en la zona {zon}"
        
        resul.append(elemento)

# Mostrar la lista creada
    print("Resultados completos:")
    print()
    for j in resul:
        print(f"• {j}")

    
resultmatrix()

#=====================================================================

