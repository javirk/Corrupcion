lista = {}

def init():
	global lista

	k = 6
	N = 1000
	delta1 = 0.5
	alfa = 0.5
	r = 0.
	delta2 = 0.5
	b = 0.5
	beta = 0.5
	guardar = False
	Nredes = 1
	tiempo = 10
	tiempoTer = 200
	tipoRed = 'BA'
	inHonestos = 0.9
	epsilon = 1/1000
	inter = False #Esto es otro modelo, con gamma.

	version = 2
	# Version:
	# 2: MODELO 4P: Delta1 = 0 y Delta2 se sustituye por la probabilidad de infecci�n: Delta2 --> R/N
	#	(la probabilidad ahora la da la proporci�n de reservados)
	# Cualquier otro valor deja el c�digo como era originalmente


	# Cosas para el archivo mtParametro.py
	cantidad1 = 40
	cantidad2 = 1
	nombrePar1 = 'alfa'
	nombrePar2 = 'b'

	#Cosas para ver comportamiento de hubs
	dinamica = False
	cuanto_cortar = 2 #Es un porcentaje que indica la cantidad de entre el 25% primeros

	#Cosas para sacar histogramas
	histograma = True
	paso_tiempo = 2

	lista = {'cuanto': cuanto_cortar, 'hubs': dinamica, 'nombrePar1': nombrePar1, 'nombrePar2': nombrePar2, 'cantidad1': cantidad1,
			 'cantidad2': cantidad2, 'eps': epsilon, 'version': version, 'tipoRed': tipoRed, 'inicialHonestos': inHonestos, 'interacciona': inter,
			 'tiempoTer': tiempoTer, 'Nredes': Nredes, 'k': k, 'N': N, 'delta1': delta1, 'delta2': delta2, 'alfa': alfa,
			 'beta': beta, 'r': r, 'b': b, 'guardar': guardar, 'tiempo': tiempo, 'histograma': histograma, 'paso': paso_tiempo}