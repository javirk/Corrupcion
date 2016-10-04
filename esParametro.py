import sys
sys.path.insert(0, '/Settings')
sys.path.insert(0, '/Funciones')

import Funciones.funcionesER as fER, Funciones.funcionesES as fun, numpy as np
import Settings.settingsES as settingsES, os

settingsES.init()

#Variables importantes
N = settingsES.lista['N']
k = settingsES.lista['k']
tiempo = settingsES.lista['tiempo']
tiempoTer = settingsES.lista['tiempoTer']
c1 = settingsES.lista['cantidad1']
c2 = settingsES.lista['cantidad2']
nombrePar1 = settingsES.lista['nombrePar1']
nombrePar2 = settingsES.lista['nombrePar2']

parametro1 = [None]*c1
parametro2 = [None]*c2
mediaC = [[0 for i in range(c2)] for j in range(c1)]
mediaH = []

nombre = fun.sacaNombre()
carpeta = r'Resultados/EstacionarioPar/'+nombre+settingsES.lista['tipoRed']
os.makedirs(carpeta)
print("Los resultados se guardarán en la carpeta:" + carpeta)

ruta = 'red_0.txt'

if settingsES.lista['tipoRed'] == 'BA':
    red = fER.redBA(guardar=settingsES.lista['guardar'], archivo=True, ruta=ruta, k=k, N=N)
elif settingsES.lista['tipoRed'] == 'AL':
    red = fER.redAL(guardar=settingsES.lista['guardar'], archivo=True, ruta=ruta)
else:
    red = fER.redER(guardar=settingsES.lista['guardar'], archivo=True, ruta=ruta, k=k, N=N)

#for i in range(0, cantidad):

for i in range(0, c1):
    if c1 > 1:
        settingsES.lista[nombrePar1] = fun.sacaParametro(i, c1)
    parametro1[i] = settingsES.lista[nombrePar1]
    print(nombrePar1 + ' = ' + str(settingsES.lista[nombrePar1]))

    for j in range(0, c2):
        if c2 > 1:
            settingsES.lista[nombrePar2] = fun.sacaParametro(j, c2)
        parametro2[j] = settingsES.lista[nombrePar2]
        print(nombrePar2 + ' = ' + str(settingsES.lista[nombrePar2]))

        H = np.zeros((N, 1))
        C = np.zeros((N, 1))

        propH = []
        propC = []
        vecpuntos = []

        H, C = fun.creaPersonas(H, C)
        #settingsES.lista[nombrePar] = fun.sacaParametro(i, cantidad)
        #parametro[i] = fun.sacaParametro(i, cantidad)

        for itiempo in range(0, tiempoTer):
            H, C = fun.estacionario(H, C, red)
            vecpuntos.append(float(C.mean(0)))
        acumuladaC, vecpuntos = fun.sacaAcumulada(vecpuntos)


        # Se saca la media para cada tiempo para ver cómo evoluciona
        #Condición de parada: abs(punto-media anterior)<epsilon (=10^-4)
        while abs(C.mean(0) - acumuladaC) > settingsES.lista['eps']:
            H, C = fun.estacionario(H, C, red)

            acumuladaC, vecpuntos = fun.sacaAcumulada(vecpuntos, nuevo = C.mean(0))
            print('H = ' + str(sum(H)/float(len(H))))
            print('C = ' + str(sum(C)/float(len(C))))

        #mediaC.append(float(C.mean(0)))
        #mediaH.append(float(H.mean(0)))

        mediaC[i][j] = sum(C) / float(len(C))
        #mediaH[i][j] = sum(H)/float(len(H))
        """for itiempo in range(0, tiempo):
            propH.append(float(H.mean(0)))
            propC.append(float(C.mean(0)))
            H, C = fun.estacionario(H, C, red)

        mediaC[i] = sum(propC) / float(len(propC))
        mediaH[i] = sum(propH) / float(len(propH))"""

fun.escribeParametro(mediaC, parametro1, parametro2, nombrePar1, nombrePar2, carpeta)