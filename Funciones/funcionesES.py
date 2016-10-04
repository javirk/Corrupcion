import sys

sys.path.insert(0, '/Settings')

import Settings.settingsES as st, random, numpy as np

def estacionario(H, C, red):
	Hcopia = H
	Ccopia = C
	matriz = np.zeros((2, 2))
	for iPers in range(0, st.lista['N']):
		if st.lista['interacciona']:
			producto = 1
			for i in range(0, red.conec[iPers]):
				indice = red.conex[iPers][i]
				indice = indice.astype(int)
				producto *= (1 - float(st.lista['alfa']) * float(C[indice]))

			T22 = (1 - st.lista['delta1']) * producto
			T21 = st.lista['r']

			producto = 1
			for i in range(0, red.conec[iPers]):
				indice = red.conex[iPers][i]
				indice = indice.astype(int)
				R_in = 1 - H[indice] - C[indice]
				producto *= (1 - float(st.lista['delta2']) * float(R_in))
			T23 = 1 - producto

			productobeta = 1
			productogamma = 1
			for i in range(0, red.conec[iPers]):
				indice = red.conex[iPers][i]
				indice = indice.astype(int)
				productobeta *= (1 - float(st.lista['beta']) * float(H[indice]))
			for i in range(0, red.conec[iPers]):
				indice = red.conex[iPers][i]
				indice = indice.astype(int)
				R_in = 1 - H[indice] - C[indice]
				productogamma *= (1 - float(st.lista['delta2']) * float(R_in))

			T33 = (1 - st.lista['b']) * productobeta * productogamma
		else:
			producto = 1
			for i in range(0, red.conec[iPers]):
				indice = red.conex[iPers][i]
				indice = indice.astype(int)
				producto *= (1 - float(st.lista['alfa']) * float(C[indice]))

			T22 = (1 - st.lista['delta1']) * producto
			T21 = st.lista['r']
			T23 = st.lista['delta2']

			productobeta = 1
			for i in range(0, red.conec[iPers]):
				indice = red.conex[iPers][i]
				indice = indice.astype(int)
				productobeta *= (1 - float(st.lista['beta']) * float(H[indice]))

			T33 = (1 - st.lista['delta2']) * (1 - st.lista['b']) * productobeta


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

def cortaVector(vector, cantidad):
	long = int(cantidad*vector.size/100)
	cvector = np.zeros((long, 1))
	for i in range(0, long):
		cvector[i] = vector[i]

	return cvector

def sacaHubs(red):
	sconec = cortaVector(red.conec, 25)
	total = int(st.lista['cuanto'] * sconec.size/100)
	hubs = np.argpartition(sconec, -total, axis = 0)[-total:]

	return hubs

def creaPersonas(H, C):
	Ntotal = len(H)
	for i in range(0, Ntotal):
		H[i] = st.lista['inicialHonestos']
		C[i] = 1-H[i]
	return H, C

def escribeTodo(propC, propH, iRed):
	nombre = 'Resultados/Estacionario/resu_r' + str(iRed) + '.txt'
	outfile = open(nombre, 'wt')
	for t in range(0, len(propC)):
		l = [str(t), str(propC[t]), str(propH[t]), str(1 - propC[t] - propH[t])]
		data = '\t'.join("%s" % x for x in l)
		data += "\n"
		outfile.write(data)
	outfile.close()

def escribeParametro(mediaC, par1, par2, npar1, npar2, carpeta):
	nombre = carpeta + '/resu_' + str(npar1) + str(npar2) + '.txt'
	outfile = open(nombre, 'wt')

	valormedia = np.round(mediaC, decimals=4)

	for i in range(0, st.lista['cantidad1']):
		for j in range(0, st.lista['cantidad2']):
			l = [str(float("{0:.4f}".format(par1[i]))), str(float("{0:.4f}".format(par2[j]))), str(float(valormedia[i][j]))]
			data = '\t'.join("%s" % x for x in l)
			data += "\n"
			outfile.write(data)
		data = "\n"
		outfile.write(data)
	outfile.close()

def sacaAcumulada(vec, nuevo = -1):
	if len(vec) == st.lista['tiempoTer'] and nuevo != -1:
		for i in range(1, st.lista['tiempoTer']):
			vec[i-1] = vec[i]
		vec[st.lista['tiempoTer']-1] = nuevo

	acumulada = sum(vec) / float(len(vec))

	return acumulada, vec

def sacaNombre():
    import datetime
    i = datetime.datetime.now()
    fname = str(i.day)+str(i.month)+str(i.year)+str(i.hour)+str(i.minute)
    return fname

def sacaParametro(i, cant):
    sup = 0.5
    inf = 0

    par = ((sup-inf)/float(cant))*i

    return par

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
