#==============================zona de funciones=================================================
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


# para poder dterminar las zonas primero debemos
# crear unos percentiles que correspondan a la 
# frecuencia cardiaca máxima que puede tomar la persona
# una vez hecho eso se multiplica este valor (equivalente al 1%) por
# la frecuencia cardiaca registrada durante el ejercicio, nos arrojara
# el porcentaje correspondiente 
def resultmatrix():
    global zon
    global resuldicc
    resul = []
    resuldicc = {}
    x = 0
    state = str




    print()

    for i in xr6.values():
        porcent = ( i / maxhera) * 100  
              
        if porcent < 50:
            zon = "Por debajo de la zona de trabajo (menos del '50%' de FCmáx)"
            state = "Por debajo de la zona de trabajo"
        elif porcent < 60:
            zon = "Z1 < 60% (Recuperación o Ritmo Suave)"
            state = "Z1"
        elif porcent < 70:
            zon = "Z2 < 70% (Resistencia Aeróbica)"
            state = "Z2"
        elif porcent < 80:
            zon = "Z3 < 80% (Tempo o Ritmo Moderado)"
            state = "Z3"
        elif porcent < 90:
            zon = "Z4 < 90% (Umbral Anaeróbico)"
            state = "Z4"
        elif porcent <= 100:
            zon = "Z5 < 100% (Capacidad Anaeróbica o Esfuerzo Máximo)"
            state = "Z5"
        else:
            zon = "Por encima de la FCmáx (valor no válido)"
            state = "Por encima de la FCmáx"
        
        x = x + 1
        
        clave = f"xr #{x}"
        valor = state
        resuldicc[clave] = valor
        
    
        elemento = f"el entrenamiento numero {x} se realizo en la zona {zon}"
        
        resul.append(elemento)

    print("Resultados completos:")
    print()
    for j in resul:
        print(f"• {j}")

def ztwocalc():
    fcztwo = maxhera * 0.7
    print()
    print(f"La frecuencia cardiaca promedio para un entrenamiento en la zona 2 (Z2) es de {fcztwo:.2f} bpm")    

def zonesort():
    znull = 0
    zone = 0
    ztwo = 0
    zthree = 0
    zfour = 0
    zfive = 0
    
    percen = float
    lstsze = len(resuldicc)
    for i in resuldicc.values():
        if i == "Por debajo de la zona de trabajo":
            znull += 1
        elif i == "Z1":
            zone += 1
        elif i == "Z2":
            ztwo += 1
        elif i == "Z3":
            zthree += 1
        elif i == "Z4":
            zfour += 1
        elif i == "Z5":
            zfive += 1
        
    znullper = (znull * 100)/lstsze
    z1per = (zone * 100)/lstsze
    z2per = (ztwo * 100)/lstsze
    z3per = (zthree * 100)/lstsze
    z4per = (zfour * 100)/lstsze
    z5per = (zfive * 100)/lstsze
    
    print()
    print(f"se realizaron {lstsze} ejercicios")
    print(f"• {znullper:.2f}% ejercicios se realizaron en la zona por debajo de la zona de trabajo")
    print(f"• {z1per:.2f}% fueron el zona Z1")
    print(f"• {z2per:.2f}% fueron el zona Z2")
    print(f"• {z3per:.2f}% fueron el zona Z3")
    print(f"• {z4per:.2f}% fueron el zona Z4")
    print(f"• {z5per:.2f}% fueron el zona Z5")
#================zona de ejecución=====================================================

# Solicitar la edad del usuario y ejecutar la funcion de fc máxima
agedat = int(input("Introduce tu edad: "))
maxhera(agedat)
# Calcular y mostrar la frecuencia cardiaca máxima estimada
print(f"Tu frecuencia cardiaca máxima estimada es {maxhera:.2f} bpm")

storagex()

resultmatrix()

ztwocalc()
    
zonesort()

        
        

    
    
    
        
        