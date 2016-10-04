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
tiempoTer = settingsES.lista['tiempoTer']

for ired in range(0, settingsES.lista['Nredes']):
	print("Red número "+str(ired))
	H = np.zeros((N, 1))
	C = np.zeros((N, 1))
	mediaH = []
	mediaC = []
	ruta = 'red_' + str(ired) + '.txt'

	red = fER.redBA(guardar = settingsES.lista['guardar'], archivo = True, ruta = ruta)
	if settingsES.lista['hubs']:
		#En caso de que queramos ver la dinámica de los hubs:
		hubs = fun.sacaHubs(red)
		mediaHubs = np.zeros((2, hubs.size))
		print('Conectividad:')
		for ihub in range(0, hubs.size):
			print(red.conec[hubs[ihub]])
	H, C = fun.creaPersonas(H, C)

	for itiempo in range(0, tiempoTer):
		H, C = fun.estacionario(H, C, red)
		#Se saca la media para cada tiempo para ver cómo evoluciona
	for itiempo in range(0, tiempo):
		mediaH.append(float(H.mean(0)))
		mediaC.append(float(C.mean(0)))
		if settingsES.lista['hubs']:
			for ihub in range(0, hubs.size):
				mediaHubs[0][ihub] += H[hubs[ihub]]
				mediaHubs[1][ihub] += C[hubs[ihub]]
		H, C = fun.estacionario(H, C, red)
	print('Media:')
	mediaHubs /= tiempo
	print(mediaHubs)

	#fun.escribeTodo(mediaC, mediaH, ired)