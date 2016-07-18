import sys
sys.path.insert(0, '/Funciones')

import random, numpy as np

class red:
	def __init__(self, guardar = False, archivo = True, ruta = 'red_0.txt', k = 6, N = 1000, tipo = 'ER'):
		self.conec = []
		self.conex = []
		self.ady = []
		self.guardar = guardar

		if archivo:
			self.ruta = 'Input/' + ruta
			error = self.inicializa()
			if error == True:
				print("Ha habido un error, te doy una Erdos-Renyi en su lugar")
				self.dameER()
		else:
			self.k = k
			self.kmax = 0
			self.N = N
			self.tipo = tipo
			if tipo == 'ER':
				self.dameER();	
		
	def generaER(self):
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

	def creaTodoER(self):
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
		while (es == 0):
			cuenta = np.zeros((self.N, 1))
			self.kmax = 0
			self.creaTodoER()
			self.generaER()
			self.componenteGigante(0, cuenta)

			if 0 in cuenta:
				es = 0
			else:
				es = 1

		if self.guardar == True:
			self.escribeRed()
			
		"""else:
									print('La red no se guardara. Si cambias de opinion, la funcion se llama escribeRed()\n')
									"""

	def dibujaER(self):
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
		while os.path.isfile('red_'+str(cuenta)+'.txt'):
			cuenta += 1

		nombre = 'Output/red_'+str(cuenta)+'.txt'

		f = open(nombre, 'wt')
		#primera = '#Red de tipo ' + self.tipo + '\n'
		#f.write(primera)

		for j in range(0, self.N):
			for i in range(0, self.kmax):
				if self.conex[j][i] > j:
					l = [str(j), str(int(self.conex[j][i]))]
					data = ' '.join("%s" % (x) for x in l)
					data = data + "\n"
					f.write(data)

		f.close()
		print('Red guardada en ' + nombre)