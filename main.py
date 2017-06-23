import sys, numpy as np
sys.path.insert(0, '/Clases')
sys.path.insert(0, '/Funciones')

import Clases.puebloClase as pc, Funciones.funGe as fun, os, configparser as cp

rutaconf='./Settings/settings.ini'

sistema, red, ejecucion, version = fun.todoConfiguracion(rutaconf)

nombre = fun.sacaNombre()
carpeta = r'Resultados/Montecarlo/'+nombre+red['tipored']
os.makedirs(carpeta)

Npueblos = red['nredes']

#for b in [float(j) * 0.25 for j in range(1, 4, 1)]:
for beta in [float(l) / 10 for l in range(1, 8, 2)]:
    pueblos = [pc.Town(rutaconf=rutaconf, ired=i) for i in range(Npueblos)]
    b = sistema['b']
    for pueblo in pueblos:
        pueblo.evoluciona(b, beta)
        if ejecucion['tipometodo'] == 'tiempo':
            pueblo.analiza()
        pueblo.escribeTodo(carpeta, b, beta, sistema['r'])
        #pueblo.representaPar()

if ejecucion['tipometodo'] == 'tiempo':
    if ejecucion['grafica']:
        fun.dibujaGrafica(pueblos)
        print(fun.mediaTiempo(pueblos, graf=False))
    else:
        print(fun.mediaTiempo(pueblos, graf = ejecucion['grafica']))
else:
    if Npueblos > 1:
        mediaTotalParC = [[0 for i in range(ejecucion['cantidad2'])] for j in range(ejecucion['cantidad1'])]
        parametro1 = list(pueblos[0].parametro1)
        for i in range(Npueblos):
            mediaTotalParC += np.matrix(pueblos[i].mediaParC)
        mediaTotalParC /= Npueblos
        print(mediaTotalParC)

        nombre = carpeta + '/par_final_' + str(Npueblos) + '_' + str(ejecucion['nombrepar1']) + '.txt'
        outfile = open(nombre, 'wt')

        for j in range(0, ejecucion['cantidad1']):
            l = [str(float("{0:.3f}".format(parametro1[j]))),
                 str(mediaTotalParC[j,0])]
            #MediaTotalParC es una matriz de Numpy!
            data = '\t'.join("%s" % x for x in l) + '\n'
            outfile.write(data)

        outfile.close()