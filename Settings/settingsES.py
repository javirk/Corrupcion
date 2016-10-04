lista = {}

def init():
	global lista

	k = 6
	N = 1000
	delta1 = 0
	alfa = 0.5
	r = 0.5
	delta2 = 0
	b = 0.5
	beta = 0.5
	guardar = False
	Nredes = 20
	tiempo = 100
	tiempoTer = 50
	tipoRed = 'BA'
	inHonestos = 0.9
	epsilon = 1/10000
	inter = False

	# Cosas para el archivo mtParametro.py
	cantidad1 = 20
	cantidad2 = 20
	nombrePar1 = 'delta1'
	nombrePar2 = 'delta2'

	#Cosas para ver comportamiento de hubs
	dinamica = True
	cuanto_cortar = 2 #Es un porcentaje que indica la cantidad de entre el 25% primeros

	lista = {'cuanto': cuanto_cortar, 'hubs': dinamica, 'nombrePar1': nombrePar1, 'nombrePar2': nombrePar2, 'cantidad1': cantidad1, 'cantidad2': cantidad2, 'eps': epsilon, 'tipoRed': tipoRed, 'inicialHonestos': inHonestos, 'interacciona': inter, 'tiempoTer': tiempoTer, 'Nredes': Nredes, 'k': k, 'N': N, 'delta1': delta1, 'delta2': delta2, 'alfa': alfa, 'beta': beta, 'r': r, 'b': b, 'guardar': guardar, 'tiempo': tiempo}