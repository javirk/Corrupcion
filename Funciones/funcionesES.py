import sys

sys.path.insert(0, '/Settings')

import Settings.settingsES as st, random, numpy as np

def estacionario(H, C, red):
	Hcopia = H
	Ccopia = C
	matriz = np.zeros((2, 2))
	for iPers in range(0, st.lista['N']):
		producto = 1
		for i in range(0, red.conec[iPers]):
			indice = red.conex[iPers][i]
			indice = indice.astype(int)
			producto *= (1 - float(st.lista['alfa'])*float(C[indice]))

		T22 = (1 - st.lista['delta1']) * producto
		T21 = st.lista['r']
		T23 = st.lista['delta2']

		producto = 1
		for i in range(0, red.conec[iPers]):
			indice = red.conex[iPers][i]
			indice = indice.astype(int)
			producto *= (1 - float(st.lista['beta'])*float(H[indice]))

		T33 = (1 - st.lista['delta2']) * (1 - st.lista['b']) * producto

		matriz[0][0] = T22 - T21
		matriz[0][1] = T23 - T21
		matriz[1][0] = 1 - T22
		matriz[1][1] = T33

		# Cambiamos H:
		#Scopia[iPers * 2 + 1] = matriz[0][0] * S[iPers * 2] + matriz[0][1] * S[iPers * 2 + 1] + T21
		Hcopia[iPers] = matriz[0][0] * H[iPers] + matriz[0][1] * C[iPers] + T21
		# Cambiamos C:
		Ccopia[iPers] = matriz[1][0] * H[iPers] + matriz[1][1] * C[iPers]
	H = Hcopia
	C = Ccopia
	return H, C

def creaPersonas(H, C):
	Ntotal = len(H)
	for i in range(0, Ntotal):
		Hi = random.random()
		Ci = random.random()
		Ri = random.random()
		H[i] = Hi/(Hi+Ci+Ri)
		C[i] = Ci/(Hi+Ci+Ri)

	return H, C

def escribeTodo(propC, propH, iRed):
	nombre = 'Resultados/Estacionario/resu_r' + str(iRed) + '.txt'
	outfile = open(nombre, 'wt')
	for t in range(0, len(propC)):
		l = [str(t), str(propC[t]), str(propH[t]), str(1 - propC[t] - propH[t])]
		data = '\t'.join("%s" % (x) for x in l)
		data += "\n"
		outfile.write(data)
	outfile.close()


def importarDatos(cantidad):
	for i in range(0, cantidad):
		filename = settingsAN.lista['directorio'] + settingsAN.lista['nombre_archivo'] + str(i) + '.txt'
		if i == 0:
			lon = len(open(filename).readlines())
			propC = np.zeros((lon, 1))
			propH = np.zeros((lon, 1))
			propR = np.zeros((lon, 1))
		else:
			lon = len(open(filename).readlines())
			aprop = np.zeros((lon, 1))
			# De momento todos los archivos deben ser del mismo tamaño, si no salta la excepción y salta el archivo
			try:
				propC = np.hstack((propC, aprop))
			except ValueError:
				print('Los archivos no tienen la misma longitud')
				break

			propH = np.hstack((propH, aprop))
			propR = np.hstack((propR, aprop))

		with open(filename, 'rt') as f:
			for linea in f:
				if linea.startswith('#'):
					continue

				linea = linea.split()
				t = int(linea[0])
				# Se entiende que el tiempo siempre va de uno en uno, así que:
				propC[t][i] = float(linea[1])
				propH[t][i] = float(linea[2])
				propR[t][i] = float(linea[3])
			# propC.append(float(linea[1]))

		f.close()
	return propC, propH, propR
