import sys
sys.path.insert(0, '/Settings')
sys.path.insert(0, '/Funciones')

import Funciones.funcionesER as fER, Funciones.funcionesMT as fun, numpy as np
import Settings.settingsMT as settingsMT, os

settingsMT.init()

#Variables importantes
N = settingsMT.lista['N']
k = settingsMT.lista['k']
tiempo = settingsMT.lista['tiempo']
tiempoTer = settingsMT.lista['tiempoTer']

if not settingsMT.lista['guardar']:
	print("Las redes no se guardarán, si quieres cambiarlo para el programa\n")

S = [None]*N

nombre = fun.sacaNombre()
carpeta = r'Resultados/Montecarlo/'+nombre+settingsMT.lista['tipoRed']
os.makedirs(carpeta)

for ired in range(0, settingsMT.lista['Nredes']):
	print("Red número " + str(ired))
	propC = []
	propR = []
	propH = []
	ruta = 'red_'+str(ired)+'.txt'
	if settingsMT.lista['tipoRed'] == 'BA':
		R = fER.redBA(guardar=settingsMT.lista['guardar'], archivo=True, ruta=ruta, k=k, N=N)
	elif settingsMT.lista['tipoRed'] == 'AL':
		R = fER.redAL(guardar=settingsMT.lista['guardar'], archivo=True, ruta=ruta)
	else:
		R = fER.redER(guardar=settingsMT.lista['guardar'], archivo=True, ruta=ruta, k=k, N=N)

	S = fun.creaPersonas(S)
	links = fun.creaLinks(S, R)
	print(links)

	completo = False
	if completo:
		for t in range(0, tiempo):
			links.loc[t+1] = links.loc[t]

			S = fun.montecarlo(S, R, links=links)

			propC.append(S.count('C')/N)
			propH.append(S.count('H')/N)
			propR.append(S.count('R')/N)
	else:
		#Primero se termaliza (esos resultados no valen para nada)
		for t in range(0, tiempoTer):
			#links.loc[t + 1] = links.loc[t]
			S = fun.montecarlo(S, R, links=links)

		#Acabamos de termalizar, toca medir.
		for t in range(0, tiempo):
			links.loc[t + 1] = links.loc[t]

			S = fun.montecarlo(S, R, links=links)

			propC.append(S.count('C')/N)
			propH.append(S.count('H')/N)
			propR.append(S.count('R')/N)

	fun.escribeLinks(links, ired, carpeta)

	fun.escribeTodo(propC, propH, propR, ired, carpeta)
