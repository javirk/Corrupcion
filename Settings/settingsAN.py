def init(lugar = 'MT'):
	global lista
	if lugar == 'ES':
		directorio = 'Resultados/Estacionario/'
	else:
		directorio = 'Resultados/Montecarlo/'
	nombreArchivo = 'resu_r'

	lista = {'directorio': directorio, 'nombre_archivo': nombreArchivo}