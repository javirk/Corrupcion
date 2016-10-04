import sys
sys.path.insert(0, '/Settings')
sys.path.insert(0, '/Funciones')

import Funciones.funcionesMT as fun, numpy as np, fnmatch, Settings.settingsAN as st, os, pandas as pd
st.init(lugar = 'ES')

#Hay que importar tantas redes como haya en el directorio que le pongamos. Por defecto será Resultados/ (definido en settingsAN)
cantidad = len(fnmatch.filter(os.listdir(st.lista['directorio']), 'resu_r*.txt'))
cantidadlinks = len(fnmatch.filter(os.listdir(st.lista['directorio']), 'res_links*.txt'))

propC, propH, propR = fun.importarDatos(cantidad)
if cantidadlinks > 0:
    HH, CC, RR, CH, HR, CR = fun.importarLinks(cantidadlinks)

    #Sacamos ahora la media de los links y la metemos en una matriz. Columnas: HH, CC... Filas: medias
    medias = np.hstack((np.reshape(HH.mean(0), (len(HH.mean(0)), 1)), np.reshape(CC.mean(0), (len(HH.mean(0)), 1)), np.reshape(RR.mean(0), (len(HH.mean(0)), 1)), np.reshape(CH.mean(0), (len(HH.mean(0)), 1)), np.reshape(HR.mean(0), (len(HH.mean(0)), 1)), np.reshape(CR.mean(0), (len(HH.mean(0)), 1))))
    #Hacemos un dataframe para guardar todo bien fácil
    df = pd.DataFrame(data=medias.astype(float), columns = ['HH', 'CC', 'RR', 'CH', 'HR', 'CR'])
    fname = st.lista['directorio'] + 'analizado_links.txt'
    df.to_csv(fname, sep=' ', header=True, float_format='%.5f', index=False)

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
print('H = ' + str(float("{0:.7f}".format(mediaTotal['H']))) + ' ± ' + str(float("{0:.7f}".format(desvTotal['H']))) + '\n')
print('C = ' + str(float("{0:.7f}".format(mediaTotal['C']))) + ' ± ' + str(float("{0:.7f}".format(desvTotal['C']))) + '\n')
print('R = ' + str(float("{0:.7f}".format(mediaTotal['R']))) + ' ± ' + str(float("{0:.7f}".format(desvTotal['R']))) + '\n')

x = input("¿Quieres dibujar todo? [s/n]")
if x == 's':
    fun.dibujaGrafica(propC, propH, propR)
