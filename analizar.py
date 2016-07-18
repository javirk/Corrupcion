import sys
sys.path.insert(0, '/Settings')
sys.path.insert(0, '/Funciones')

import Funciones.funcionesMT as fun, numpy as np, fnmatch, Settings.settingsAN as st, os
st.init()

#Hay que importar tantas redes como haya en el directorio que le pongamos. Por defecto será Resultados/ (definido en settingsAN)
cantidad = len(fnmatch.filter(os.listdir(st.lista['directorio']), 'resu_r*.txt'))

propC, propH, propR = fun.importarDatos(cantidad)

#Se promedia entre redes con una media pesada. PropC, etc son matrices con todos los resultados
mediaC = propC.mean(0)
#MediaC es un vector fila, igual que desvC
desvC = propC.std(0)
mediaTotal = {'C': np.ma.average(mediaC, weights=desvC)}
#mediaTotal es un diccionario con las medias
desvTotal = {'C': fun.desvstaPesada(desvC)}

mediaH = propH.mean(0)
desvH = propR.std(0)
mediaTotal['H'] = np.ma.average(mediaH, weights = desvH)
desvTotal['H'] = fun.desvstaPesada(desvH)

mediaR = propR.mean(0)
desvR = propH.std(0)
mediaTotal['R'] = np.ma.average(mediaR, weights = desvR)
desvTotal['R'] = fun.desvstaPesada(desvR)

print('Se han obtenido los siguientes resultados: \n')
print('H = ' + str(float("{0:.7f}".format(mediaTotal['H']))) + '±' + str(float("{0:.7f}".format(desvTotal['H']))) + '\n')
print('C = ' + str(float("{0:.7f}".format(mediaTotal['C']))) + '±' + str(float("{0:.7f}".format(desvTotal['C']))) + '\n')
print('R = ' + str(float("{0:.7f}".format(mediaTotal['R']))) + '±' + str(float("{0:.7f}".format(desvTotal['R']))) + '\n')