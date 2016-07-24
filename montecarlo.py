import sys
sys.path.insert(0, '/Settings')
sys.path.insert(0, '/Funciones')

import Funciones.funcionesER as fER, Funciones.funcionesMT as fun
import Settings.settingsMT as settingsMT

settingsMT.init()

#Variables importantes
N = settingsMT.lista['N']
k = settingsMT.lista['k']
tiempo = settingsMT.lista['tiempo']
tiempoTer = settingsMT.lista['tiempoTer']

if not settingsMT.lista['guardar']:
	print("Las redes no se guardarán, si quieres cambiarlo para el programa\n")

S = [None]*N

for ired in range(0, settingsMT.lista['Nredes']):
	print("Red número " + str(ired))
	propC = []
	propR = []
	propH = []
	R = fER.redER(guardar = settingsMT.lista['guardar'], archivo = False, k = k, N = N)
	S = fun.creaPersonas(S)

	completo = False
	if completo:
		for t in range(0, tiempo):
			S = fun.montecarlo(S, R)

			propC.append(S.count('C')/N)
			propH.append(S.count('H')/N)
			propR.append(S.count('R')/N)
	else:
		#Primero se termaliza (esos resultados no valen para nada)
		for t in range(0, tiempoTer):
			S = fun.montecarlo(S, R)

		#Acabamos de termalizar, toca medir.
		for t in range(0, tiempo):
			S = fun.montecarlo(S, R)

			propC.append(S.count('C')/N)
			propH.append(S.count('H')/N)
			propR.append(S.count('R')/N)

	fun.escribeTodo(propC, propH, propR, ired)