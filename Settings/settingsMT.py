lista = {}
def init():
	global lista

	#Ajustes comunes
	k = 6
	N = 1000
	delta1 = 0.5
	alfa = 0.5
	r = 0.9
	delta2 = 0.5
	b = 0.05
	beta = 0.5
	guardarRed = False
	Nredes = 1
	tiempo = 150
	tiempoTer = 50
	tipoRed = 'ER'
	inicialHonestos = 0.9

	#Ajustes archivo mtTiempo.py
	buscaLink = False

	# Cosas para sacar histogramas
	histograma = True
	paso_tiempo = 2

	#Cosas para el archivo mtParametro.py
	cantidad1 = 10
	cantidad2 = 10
	nombrePar1 = 'beta'
	nombrePar2 = 'r'

	version = 0
	"""Version:
		1: Delta2 pasa a ser la probabilidad de infección: Delta2 --> 1-Prod(1-Delta2 Aij Rj)
		2: Delta2 se sustituye por la probabilidad de infección: Delta2 --> R/N (la probabilidad ahora la da la
			proporción de reservados)
		Cualquier otro valor deja el código como era originalmente"""

	lista = {'nombrePar1': nombrePar1, 'nombrePar2': nombrePar2, 'cambios': version, 'cantidad1': cantidad1, 'cantidad2': cantidad2,
			 'buscaLink': buscaLink, 'inicialHonestos': inicialHonestos, 'tipoRed': tipoRed, 'k': k, 'N': N, 'delta1': delta1,
			 'delta2': delta2, 'alfa': alfa, 'beta': beta, 'r': r, 'b': b, 'guardar': guardarRed, 'Nredes': Nredes, 'tiempo': tiempo,
			 'tiempoTer': tiempoTer, 'histograma': histograma, 'paso': paso_tiempo}