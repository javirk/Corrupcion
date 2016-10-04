import sys
sys.path.insert(0, '/Settings')
sys.path.insert(0, '/Funciones')

import Funciones.funcionesER as fER, Funciones.funcionesMT as fun
import Settings.settingsMT as settingsMT, os

settingsMT.init()

#Variables importantes
N = settingsMT.lista['N']
k = settingsMT.lista['k']
tiempo = settingsMT.lista['tiempo']
tiempoTer = settingsMT.lista['tiempoTer']
c1 = settingsMT.lista['cantidad1']
c2 = settingsMT.lista['cantidad2']

if not settingsMT.lista['guardar']:
	print("Las redes no se guardarán, si quieres cambiarlo para el programa\n")

S = [None]*N
parametro1 = [None]*c1
parametro2 = [None]*c2
mediaC = [[0 for i in range(c2)] for j in range(c1)]
mediaH = [[]]
mediaR = [[]]
nombrePar1 = settingsMT.lista['nombrePar1']
nombrePar2 = settingsMT.lista['nombrePar2']

nombre = fun.sacaNombre()
carpeta = r'Resultados/MontecarloPar/'+nombre+settingsMT.lista['tipoRed']
os.makedirs(carpeta)
print("Los resultados se guardarán en la carpeta:" + carpeta)

# Definimos la red que vamos a usar:
ruta = 'red_0.txt'

if settingsMT.lista['tipoRed'] == 'BA':
    R = fER.redBA(guardar=settingsMT.lista['guardar'], archivo=True, ruta=ruta, k=k, N=N)
elif settingsMT.lista['tipoRed'] == 'AL':
    R = fER.redAL(guardar=settingsMT.lista['guardar'], archivo=True, ruta=ruta)
else:
    R = fER.redER(guardar=settingsMT.lista['guardar'], archivo=True, ruta=ruta, k=k, N=N)


for i in range(0,c1):
    if c1 > 1:
        settingsMT.lista[nombrePar1] = fun.sacaParametro(i, c1)
    parametro1[i] = settingsMT.lista[nombrePar1]
    print(nombrePar1 + ' = ' + str(settingsMT.lista[nombrePar1]))
    for j in range(0, c2):
        if c2 > 1:
            settingsMT.lista[nombrePar2] = fun.sacaParametro(j, c2)
        parametro2[j] = settingsMT.lista[nombrePar2]
        print(nombrePar2 + ' = ' + str(settingsMT.lista[nombrePar2]))

        S = [None] * N
        S = fun.creaPersonas(S)
        propC = []
        propR = []
        propH = []

        for t in range(0, tiempoTer):
            S = fun.montecarlo(S, R)

        for t in range(0, tiempo):
            S = fun.montecarlo(S, R)

            propC.append(S.count('C') / N)
            propH.append(S.count('H') / N)
            propR.append(S.count('R') / N)

        mediaC[i][j] = sum(propC)/float(len(propC))
        #mediaH[i][j] = sum(propH)/float(len(propH))
        #mediaR[i][j] = sum(propR)/float(len(propR))
        #print(propC)

fun.escribeParametro(mediaC, parametro1, parametro2, nombrePar1, nombrePar2, carpeta)