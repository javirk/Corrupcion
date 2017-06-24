import sys, numpy as np
sys.path.insert(0, '/Clases')
sys.path.insert(0, '/Funciones')

import Clases.puebloClase as pc, Funciones.funGe as fun, os, configparser as cp

rutaconf='./Settings/settings.ini'

sistema, red, ejecucion, version = fun.todoConfiguracion(rutaconf)

#La carpeta donde se van a guardar los resultados se crea dentro de la carpeta Montecarlo y depende de la fecha
#Si da error es porque ya existe una carpeta con el mismo nombre en la ruta
nombre = fun.sacaNombre()
carpeta = r'Resultados/Montecarlo/'+nombre+red['tipored']
os.makedirs(carpeta)

Npueblos = red['nredes']

#Crea tantos pueblos como se necesite
pueblos = [pc.Town(rutaconf=rutaconf, ired=i) for i in range(Npueblos)]
b = sistema['b']
beta = sistema['beta']
for pueblo in pueblos:
    # Simula con el método de Monte Carlo. Evoluciona es un método que también termaliza. Guarda los datos en propC
    # en el caso de que ejecucion['tipometodo'] = 'tiempo'. Si no, en la matriz mediaParC
    pueblo.evoluciona(b, beta)
    if ejecucion['tipometodo'] == 'tiempo':
        # Analiza los resultados de ese pueblo (media, varianza...). No es necesario pasar argumentos porque propC
        # son variables locales de la clase
        pueblo.analiza()
    pueblo.escribeTodo(carpeta, b, beta, sistema['r'])
    #pueblo.representaPar()

# Lo siguiente es para escribir los resultados

if ejecucion['tipometodo'] == 'tiempo':
    #Si se quiere dibujar la gráfica
    if ejecucion['grafica']:
        fun.dibujaGrafica(pueblos)
    print(fun.mediaTiempo(pueblos, graf=False))

else:
    if Npueblos > 1:
        # Se media entre todos los pueblos
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