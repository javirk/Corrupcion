lista = {}

def init(lugar = 'MT'):
	global lista
	if lugar == 'ES':
		directorio = 'Resultados/Estacionario/'
	else:
		directorio = 'Resultados/Montecarlo/2382016103AL/'
	nombreArchivo = 'resu_r'

	lista = {'directorio': directorio, 'nombre_archivo': nombreArchivo}