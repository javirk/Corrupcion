import sys
sys.path.insert(0, '/Settings')
sys.path.insert(0, '/Funciones')

import Funciones.funcionesER as fER, Funciones.funcionesES as fun, numpy as np
import Settings.settingsES as settingsES

settingsES.init()

#Variables importantes
N = settingsES.lista['N']
k = settingsES.lista['k']
tiempo = settingsES.lista['tiempo']
H = np.zeros((N, 1))
C = np.zeros((N, 1))
mediaH = []
mediaC = []

for ired in range(0, settingsES.lista['Nredes']):
	print("Red número "+str(ired))
	propC = []
	propR = []
	propH = []
	ruta = 'red_' + str(ired) + '.txt'

	red = fER.red(guardar = settingsES.lista['guardar'], archivo = True, ruta = ruta)
	H, C = fun.creaPersonas(H, C)

	for i in range(0, tiempo):
		H, C = fun.estacionario(H, C, red)
		#Se saca la media para cada tiempo para ver cómo evoluciona
		mediaH.append(float(H.mean(0)))
		mediaC.append(float(C.mean(0)))

	fun.escribeTodo(mediaC, mediaH, ired)
