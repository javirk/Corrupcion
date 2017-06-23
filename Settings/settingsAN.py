lista = {}

def init(lugar = 'MT'):
	global lista
	if lugar == 'ES':
		directorio = 'Resultados/Estacionario/101020161153BA/'
	else:
		directorio = 'Resultados/Montecarlo/12102016105BA/'

	nombre_archivo = 'resu_r'  #Nombre común de los archivos a analizar

	salida = 'medias.txt' #Escribir sin / al principio



	lista = {'directorio': directorio, 'salida': salida, 'nombre_archivo': nombre_archivo}