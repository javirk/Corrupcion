import sys
sys.path.insert(0, '/Settings')
sys.path.insert(0, '/Clases')

import Clases.redClase as fER, Clases.funcionesES as fun, numpy as np
import Settings.settingsES as settingsES, os, pandas as pd

settingsES.init()

#Variables importantes
N = settingsES.lista['N']
k = settingsES.lista['k']
tiempo = settingsES.lista['tiempo']
tiempoTer = settingsES.lista['tiempoTer']

#Creación de la carpeta en la que guardar los resultados
nombre = fun.sacaNombre()
carpeta = r'Resultados/Estacionario/'+nombre+settingsES.lista['tipoRed']
os.makedirs(carpeta)
print("Los resultados se guardarán en la carpeta:" + carpeta)

if settingsES.lista['histograma']:
	evol = fun.creaEvolucion()

for ired in range(0, settingsES.lista['Nredes']):
	print("Red número "+str(ired))
	H = np.zeros((N, 1))
	C = np.zeros((N, 1))
	mediaH = []
	mediaC = []
	ruta = 'red_' + str(ired) + '.txt'

	if settingsES.lista['tipoRed'] == 'BA':
		red = fER.redBA(guardar=settingsES.lista['guardar'], archivo=True, ruta=ruta, k=k, N=N)
	elif settingsES.lista['tipoRed'] == 'AL':
		red = fER.redAL(guardar=settingsES.lista['guardar'], archivo=True, ruta=ruta)
	else:
		red = fER.redER(guardar=settingsES.lista['guardar'], archivo=True, ruta=ruta, k=k, N=N)

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
		mediaH.append(float(sum(H)/float(len(H))))
		mediaC.append(float(sum(C)/float(len(C))))

		if settingsES.lista['histograma'] and itiempo % settingsES.lista['paso'] == 0:
			evol = fun.actualizaHistograma(H, C, evol, ired)
		if settingsES.lista['hubs']:
			for ihub in range(0, hubs.size):
				mediaHubs[0][ihub] += H[hubs[ihub]]
				mediaHubs[1][ihub] += C[hubs[ihub]]

		H, C = fun.estacionario(H, C, red)

	"""if settingsES.lista['histograma']:
		for i in range(0, N):
			evol['k'][j] += red.conec[j][0]"""

	#Mete más filas al dataframe para la siguiente red y añade el grado de cada nodo
	if settingsES.lista['histograma']:
		for i in range(0, N):
			evol['k'][ired*N+i] += red.conec[i][0]
			#print(red.conec[i][0])

		if ired+1 < settingsES.lista['Nredes']:
			auxdf = pd.DataFrame([[0]*4]*N, index = list(range(N*(ired+1), N*(ired+1)+N)), columns = list('kHCR'))
			auxdf = auxdf.astype('float64')
			evol = evol.append(auxdf)

	fun.escribeTodo(mediaC, mediaH, ired, carpeta)

if settingsES.lista['histograma']:
	evol['H'] /= (tiempo / settingsES.lista['paso'])
	evol['C'] /= (tiempo / settingsES.lista['paso'])
	evol['R'] /= (tiempo / settingsES.lista['paso'])
	#evol['k'] /= settingsES.lista['Nredes']

	fun.escribeHistograma(evol, carpeta)