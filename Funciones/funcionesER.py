import sys
sys.path.insert(0, '/Funciones')

import random, numpy as np

class redER:
	def __init__(self, guardar = False, archivo = True, ruta = 'red_0.txt', k = 6, N = 1000):
		self.conec = []
		self.conex = []
		self.ady = []
		self.guardar = guardar

		if archivo:
			self.ruta = 'Input/' + ruta
			error = self.inicializa()
			if error:
				print("Ha habido un error, te doy una Erdos-Renyi en su lugar")
				self.dameER()
		else:
			self.k = k
			self.kmax = 0
			self.N = N
			self.dameER()

	def genera(self):
		p = self.k/(self.N - 1)

		for i in range(0, self.N):
			for j in range(i+1, self.N):
				alea = random.random()
				if alea < p:
					self.ady[i][j] = 1
					self.ady[j][i] = 1
					self.conec[i] += 1
					self.conec[j] += 1

					if (self.conec[i] > self.kmax) or (self.conec[j] > self.kmax):
						vec = np.zeros((self.N, 1))
						self.conex = np.hstack((self.conex, vec))
						self.kmax += 1

					self.conex[i][self.conec[i]-1] = j
					self.conex[j][self.conec[j]-1] = i

	def creaTodo(self):
		self.conec = np.zeros((self.N, 1))
		self.conec = self.conec.astype(int)

		self.ady = np.zeros((self.N, self.N))
		self.ady = self.ady.astype(int)

		self.conex = np.zeros((self.N, self.kmax))
		self.conex = self.conex.astype(int)

	def componenteGigante(self, nodo, cuenta):
		for i in range(0, self.conec[nodo]):
			if cuenta[self.conex[nodo][i]] == 0:
				cuenta[self.conex[nodo][i]] = 1
				self.componenteGigante(self.conex[nodo][i], cuenta)

	def dameER(self):
		es = 0
		while es == 0:
			cuenta = np.zeros((self.N, 1))
			self.kmax = 0
			self.creaTodo()
			self.genera()
			self.componenteGigante(0, cuenta)

			if 0 in cuenta:
				es = 0
			else:
				es = 1

		if self.guardar :
			self.escribeRed()

	def dibuja(self):
		import networkx as nx, matplotlib.pyplot as plt
		G = nx.from_numpy_matrix(self.ady)
		plt.close()
		nx.draw_random(G)
		plt.savefig('Resultados/red.png')

	def inicializa(self):
		try:
			f = open(self.ruta, 'rt')
		except:
			print("No pudo abrirse el archivo especificado")
			error = True
			return error

		error = 0

		import Funciones.funcionesMT as Fun
		self.N = Fun.dameN(self.ruta)
		self.kmax = 0
		self.creaTodoER()

		for linea in f:
			linea = linea.split()
			i = int(linea[0])
			j = int(linea[1])
			self.ady[i][j] = 1
			self.ady[j][i] = 1

			self.conec[i] += 1
			self.conec[j] += 1

			if (self.conec[i] > self.kmax) or (self.conec[j] > self.kmax):
				vec = np.zeros((self.N, 1))
				self.conex = np.hstack((self.conex, vec))
				self.kmax += 1

			self.conex[i][self.conec[i]-1] = j
			self.conex[j][self.conec[j]-1] = i

		cuenta = np.zeros((self.N, 1))
		self.componenteGigante(0, cuenta)
		if 0 in cuenta:
			print("Ojo, la red tiene nodos aislados")

		f.close()
		return error

	def escribeRed(self):
		import os
		cuenta = 0
		while os.path.isfile('Output/ER/red_'+str(cuenta)+'.txt'):
			cuenta += 1

		nombre = 'Output/ER/red_'+str(cuenta)+'.txt'

		f = open(nombre, 'wt')
		#primera = '#Red de tipo ' + self.tipo + '\n'
		#f.write(primera)

		for j in range(0, self.N):
			for i in range(0, self.kmax):
				if self.conex[j][i] > j:
					l = [str(j), str(int(self.conex[j][i]))]
					data = ' '.join("%s" % x for x in l)
					data += "\n"
					f.write(data)

		f.close()
		print('Red guardada en ' + nombre)

class redBA:
	def __init__(self, guardar=False, archivo=True, ruta='red_0.txt', k=6, N=1000):
		self.conec = []
		self.conex = []
		self.ady = []
		self.guardar = guardar

		if archivo:
			self.ruta = 'Input/' + ruta
			error = self.inicializa()
			if error:
				print("Ha habido un error, te doy una Barabasi-Albert en su lugar")
				self.guardar = guardar
				self.genera()
				if self.guardar:
					self.escribeRed()
		else:
			self.k = k
			self.kmax = 3
			self.N = N
			self.m0 = 3
			self.m = int(self.k/2)
			self.guardar = guardar

			self.genera()

			if self.guardar:
				self.escribeRed()
				print("La red está acabada y guardada.")

	def creaTodo(self):
		self.conec = np.zeros((self.N, 1))
		self.conec = self.conec.astype(int)

		#self.kmax = max(self.conec)

		self.ady = np.zeros((self.N, self.N))
		self.conex = np.zeros((self.N, self.kmax))

		for i in range(0, self.m0):
			for j in range(i + 1, self.m0):
				self.conec[i] += 1
				self.conec[j] += 1

				self.conex[i][j - 1] = j
				self.conex[j][i] = i

				self.ady[i][j] = 1
				self.ady[j][i] = 1

		self.kmax = int(max(self.conec))

	def componenteGigante(self, nodo, cuenta):
		for i in range(0, self.conec[nodo]):
			if cuenta[self.conex[nodo][i]] == 0:
				cuenta[self.conex[nodo][i]] = 1
				self.componenteGigante(self.conex[nodo][i], cuenta)

	"""def dameRed(self):
		es = 0
		while es == 0:
			cuenta = np.zeros((self.N, 1))
			self.kmax = 0
			self.creaTodoER()
			self.generaER()
			self.componenteGigante(0, cuenta)

			if 0 in cuenta:
				es = 0
			else:
				es = 1

		if self.guardar:
			self.escribeRed()"""

	def buscaNodo(self, rand, caja):
		for i in range(0, len(caja)):
			if i == len(caja)-1:
				link = i
				return link
			elif caja[i] <= rand <= caja[i+1]:
				link = i
				return link

	def creaCajas(self, t, newcon = []):
		pi = [None] * t
		caja = np.zeros((t, 1))
		# Creamos el vector de probabilidades y las cajas
		for inodo in range(0, t):
			if newcon == []:
				#Si la lista está vacía es porque estamos en la primera iteración y se puede usar self.conec
				pi[inodo] = self.conec[inodo] / sum(self.conec)
			else:
				pi[inodo] = newcon[inodo]/sum(newcon)

			if inodo == 0:
				caja[inodo] = 0
			else:
				caja[inodo] = caja[inodo - 1] + pi[inodo - 1]

		return pi, caja

	def conecta(self, links, nodo):
		#self.conec = np.append(self.conec, len(links))
		for ilink in range(0, len(links)):
			self.conec[links[ilink]] += 1
			self.conec[nodo] += 1

			if (self.conec[links[ilink]] > self.kmax) or (self.conec[nodo] > self.kmax):
				vec = np.zeros((self.N, 1))
				self.conex = np.hstack((self.conex, vec))
				self.kmax += 1

			self.conex[nodo][self.conec[nodo] - 1] = links[ilink]
			self.conex[links[ilink]][self.conec[links[ilink]] - 1] = nodo

			#Actualización de la matriz de adyacencia
			self.ady[links[ilink]][nodo] = 1
			self.ady[nodo][links[ilink]] = 1

	def genera(self):
		# Primero generamos una estructura en forma de triángulo con m0(= 3) nodos
		self.creaTodo()
		# Ahora empieza el algoritmo de Barabási-Albert
		for t in range(self.m0, self.N):
			if t%100 == 0:
				print("Llevo " + str(t))
			#Se lanza tres números aleatorios para ver dónde caen los links
			link = []
			for al in range(0, self.m):
				alea = random.random()
				if al == 0:
					pi, caja = self.creaCajas(t)
					link.append(self.buscaNodo(alea, caja))
				else:
					newcon = [x[:] for x in self.conec]
					for i in range(0, len(link)):
						newcon[link[i]] = 0
					pi, caja = self.creaCajas(t, newcon = newcon)
					link.append(self.buscaNodo(alea, caja))

			# Se conectan ahora el nodo nuevo con los tres nodos elegidos
			self.conecta(link, t)

	def dibuja(self):
		import networkx as nx, matplotlib.pyplot as plt
		G = nx.from_numpy_matrix(self.ady)
		plt.close()
		nx.draw_random(G)
		plt.savefig('../Plot/red.png')

	def inicializa(self):
		try:
			f = open(self.ruta, 'rt')
		except:
			print("No pudo abrirse el archivo especificado")
			error = True
			return error

		error = 0

		import Funciones.funcionesMT as Fun
		self.N = Fun.dameN(self.ruta)
		self.kmax = 0
		self.creaTodoER()

		for linea in f:
			linea = linea.split()
			i = int(linea[0])
			j = int(linea[1])
			self.ady[i][j] = 1
			self.ady[j][i] = 1

			self.conec[i] += 1
			self.conec[j] += 1

			if (self.conec[i] > self.kmax) or (self.conec[j] > self.kmax):
				vec = np.zeros((self.N, 1))
				self.conex = np.hstack((self.conex, vec))
				self.kmax += 1

			self.conex[i][self.conec[i] - 1] = j
			self.conex[j][self.conec[j] - 1] = i

		cuenta = np.zeros((self.N, 1))
		self.componenteGigante(0, cuenta)
		if 0 in cuenta:
			print("Ojo, la red tiene nodos aislados")

		f.close()
		return error

	def escribeRed(self):
		import os
		cuenta = 0

		while os.path.isfile('Output/BA/red_' + str(cuenta) + '.txt'):
			cuenta += 1

		nombre = 'Output/BA/red_' + str(cuenta) + '.txt'

		f = open(nombre, 'wt')
		# primera = '#Red de tipo ' + self.tipo + '\n'
		# f.write(primera)

		for j in range(0, self.N):
			for i in range(0, self.kmax):
				if self.conex[j][i] > j:
					l = [str(j), str(int(self.conex[j][i]))]
					data = ' '.join("%s" % x for x in l)
					data += "\n"
					f.write(data)

		f.close()
		print('Red guardada en ' + nombre)

	def dibujaGrado(self):
		H = [0]*self.kmax

		for i in range(0, self.N):
			H[self.conec[i]-1] += 1

		#print(H)

		nombre = 'histograma.txt'
		outfile = open(nombre, 'wt')
		for i in range(0, self.kmax):
			l = [str(i), str(H[i])]
			data = '\t'.join("%s" % (x) for x in l)
			data += "\n"
			outfile.write(data)
		outfile.close()

#R = redBA(archivo = False, k = 6, N = 1000)