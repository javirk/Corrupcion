import sys
sys.path.insert(0, '/Settings')

import Settings.settingsMT as st, random, Settings.settingsAN as settingsAN, numpy as np, math, pandas as pd

def sacaParametro(i, cant):
    sup = 0.5
    inf = 0

    par = ((sup-inf)/float(cant))*i

    return par

def actualizaHistograma(S, evol, ired):
    for inodo in range(0, len(S)):
        evol[S[inodo]][ired*st.lista['N']+inodo] += 1
        #evol[S[inodo]][inodo] += 1
    return evol

def creaEvolucion():
    N = st.lista['N']
    # Queremos ver también correlación con el grado, por eso creo una columna más con el grado medio de ese nodo
    evol = pd.DataFrame([[0]*4]*N, index = list(range(0, N)), columns = list('kHCR'))
    evol = evol.astype('float64')
    return evol

def escribeHistograma(evol, carpeta):
    fname = carpeta+'/resu_histo.txt'
    decimals = pd.Series([3, 3, 3, 3], index = list('kHCR'))
    evol = evol.round(decimals)
    evol.to_csv(fname, index = None, sep = ' ', mode = 'w')

#def escribeParametro(mediaC, mediaH, mediaR, parametro, carpeta, nombrePar):
def escribeParametro(mediaC, par1, par2, npar1, npar2, carpeta):
    nombre = carpeta + '/resu_' + str(npar1) + str(npar2) + '.txt'
    outfile = open(nombre, 'wt')
    for i in range(0, st.lista['cantidad1']):
        for j in range(0, st.lista['cantidad2']):
            l = [str(float("{0:.3f}".format(par1[i]))), str(float("{0:.4f}".format(par2[j]))), str(float("{0:.4f}".format(mediaC[i][j])))]
            data = '\t'.join("%s" % x for x in l)
            data += "\n"
            outfile.write(data)
        data = "\n"
        outfile.write(data)

    outfile.close()

def dameN(filename):
    maximo = 0
    f = open(filename, "rt")

    for linea in f:
        linea = linea.split()
        linea = map(int, linea)
        maxv = max(linea)
        if maxv > maximo:
            maximo = maxv

    return maximo +1

def importarDatos(cantidad):
    for i in range(0, cantidad):
        filename = settingsAN.lista['directorio'] + settingsAN.lista['nombre_archivo'] + str(i) + '.txt'
        if i == 0:
            lon = len(open(filename).readlines())
            propC = np.zeros((lon, 1))
            propH = np.zeros((lon, 1))
            propR = np.zeros((lon, 1))
        else:
            lon = len(open(filename).readlines())
            aprop = np.zeros((lon, 1))
            #De momento todos los archivos deben ser del mismo tamaño, si no salta la excepción y salta el archivo
            try:
                propC = np.hstack((propC, aprop))
            except ValueError:
                print('Los archivos no tienen la misma longitud')
                break

            propH = np.hstack((propH, aprop))
            propR = np.hstack((propR, aprop))

        with open(filename, 'rt') as f:
            for linea in f:
                if linea.startswith('#'):
                    continue
               
                linea = linea.split()
                t = int(linea[0])
                #Se entiende que el tiempo siempre va de uno en uno, así que:
                propC[t][i] = float(linea[1])
                propH[t][i] = float(linea[2])
                propR[t][i] = float(linea[3])
                #propC.append(float(linea[1]))

        f.close()
    return propC, propH, propR

def importarLinks(cantidad):
    for i in range(0, cantidad):
        filename = settingsAN.lista['directorio'] + 'res_links' + str(i) + '.txt'
        if i == 0:
            lon = len(open(filename).readlines())
            HH = np.zeros((lon-1, 1))
            CC = np.zeros((lon-1, 1))
            RR = np.zeros((lon-1, 1))
            CH = np.zeros((lon-1, 1))
            HR = np.zeros((lon-1, 1))
            CR = np.zeros((lon-1, 1))
        else:
            #Esto es para meter los del siguiente archivo
            lon = len(open(filename).readlines())
            aprop = np.zeros((lon-1, 1))
            # De momento todos los archivos deben ser del mismo tamaño, si no salta la excepción y salta el archivo
            try:
                HH = np.hstack((HH, aprop))
            except ValueError:
                print('Los archivos no tienen la misma longitud')
                break

            CC = np.hstack((CC, aprop))
            RR = np.hstack((RR, aprop))
            CH = np.hstack((CH, aprop))
            HR = np.hstack((HR, aprop))
            CR = np.hstack((CR, aprop))

        with open(filename, 'rt') as f:
            for linea in f:
                if linea.startswith('#'):
                    continue

                linea = linea.split()
                if linea[0] == 't':
                    continue
                t = int(linea[0])
                suma = sum(list(map(float, linea))[1:])
                # Se entiende que el tiempo siempre va de uno en uno, así que:
                HH[t][i] = float(linea[1])/suma
                CC[t][i] = float(linea[2])/suma
                RR[t][i] = float(linea[3])/suma
                CH[t][i] = float(linea[4])/suma
                HR[t][i] = float(linea[5])/suma
                CR[t][i] = float(linea[6])/suma
                # propC.append(float(linea[1]))

        f.close()
    return HH, CC, RR, CH, HR, CR

def desvstaPesada(desv):
    aux = 1/(desv*desv)
    final = 1/sum(aux)
    return math.sqrt(final)

def escribeLinks(links, ired, carpeta):
    links.insert(0, 't', list(range(0, len(links))))
    fname = carpeta+'/res_links' + str(ired) + '.txt'
    links.to_csv(fname, index = None, sep = ' ', mode = 'w')

def sacaNombre():
    import datetime
    i = datetime.datetime.now()
    fname = str(i.day)+str(i.month)+str(i.year)+str(i.hour)+str(i.minute)
    return fname

def todoConfiguracion(rutaconf):
    import configparser as cp
    
    # Pasar todos los parámetros a variables usables leyendo del archivo de configuracion
    Config = cp.ConfigParser()
    Config.read(rutaconf)
    secc = Config.sections()

    sistema = {}
    red = {}
    ejecucion = {}
    version = {}

    leeConfig(Config, secc, sistema, red, ejecucion, version)
    
    return sistema, red, ejecucion, version

def leeConfig(Config, secc, sistema, red, ejecucion, version):
    for seccion in secc:
        options = Config.options(seccion)
        for option in options:
            if seccion == 'Red':
                try:
                    red[option] = Config.getint(seccion, option)
                except:
                    try:
                        red[option] = Config.getboolean(seccion, option)
                    except:
                        red[option] = Config.get(seccion, option)
            elif seccion == 'Sistema':
                try:
                    sistema[option] = Config.getfloat(seccion, option)
                except:
                    try:
                        sistema[option] = Config.getboolean(seccion, option)
                    except:
                        sistema[option] = Config.get(seccion, option)
            elif seccion == 'Ejecucion':
                try:
                    ejecucion[option] = Config.getint(seccion, option)
                except:
                    try:
                        ejecucion[option] = Config.getboolean(seccion, option)
                    except:
                        ejecucion[option] = Config.get(seccion, option)
            elif seccion == 'Version':
                try:
                    version[option] = Config.getint(seccion, option)
                except:
                    try:
                        version[option] = Config.getboolean(seccion, option)
                    except:
                        version[option] = Config.get(seccion, option)
            else:
                print("Hay un error en el archivo de configuración")
                exit()

def mediaTiempo(pueblos, graf = True):
    Npueblos = len(pueblos)
    # Mediar los datos:
    mediaC = np.array([pueblos[i].mediaTotal['C'] for i in range(Npueblos)])
    desvC = np.array([pueblos[i].desvTotal['C'] for i in range(Npueblos)])

    mediaH = np.array([pueblos[i].mediaTotal['H'] for i in range(Npueblos)])
    desvH = np.array([pueblos[i].desvTotal['H'] for i in range(Npueblos)])

    mediaR = np.array([pueblos[i].mediaTotal['R'] for i in range(Npueblos)])
    desvR = np.array([pueblos[i].desvTotal['R'] for i in range(Npueblos)])

    mediaTotal = {'C': np.ma.average(mediaC, weights=desvC)}
    desvTotal = {'C': desvstaPesada(desvC)}

    mediaTotal['H'] = np.ma.average(mediaH, weights=desvH)
    desvTotal['H'] = desvstaPesada(desvH)

    mediaTotal['R'] = np.ma.average(mediaR, weights=desvR)
    desvTotal['R'] = desvstaPesada(desvR)

    if not graf:
        resu = ['H = ' + str(float("{0:.7f}".format(mediaTotal['H']))) + ' ± ' + str(
            float("{0:.7f}".format(desvTotal['H']))) + '\n',
                'C = ' + str(float("{0:.7f}".format(mediaTotal['C']))) + ' ± ' + str(
                    float("{0:.7f}".format(desvTotal['C']))) + '\n',
                'R = ' + str(float("{0:.7f}".format(mediaTotal['R']))) + ' ± ' + str(
                    float("{0:.7f}".format(desvTotal['R']))) + '\n']

        '''for i in range(0, len(resu)):
            print(resu[i])'''
        return resu
    else:
        return mediaTotal, desvTotal

def dibujaGrafica(pueblos):
    import matplotlib.pyplot as plt
    import matplotlib.patches as mpatches
    tiempoMax = len(pueblos[0].propC)
    t = np.arange(0., tiempoMax)
    fig, ax = plt.subplots(1)
    #for pueblo in range(0, len(pueblos)):
    ax.plot(t, pueblos[0].propC, 'r-', linewidth = 1.0, alpha = 0.8, label = 'Corruptos')
    ax.plot(t, pueblos[0].propH, 'b-', linewidth = 1.0, alpha = 0.8, label = 'Honestos')
    ax.plot(t, pueblos[0].propR, 'g-', linewidth = 1.0, alpha = 0.8, label = 'Reservados')

    medias, desv = mediaTiempo(pueblos)
    ax.plot(t, [medias['C']] * tiempoMax, 'r-', linewidth = 1.5)
    ax.plot(t, [medias['H']] * tiempoMax, 'b-', linewidth = 1.5)
    ax.plot(t, [medias['R']] * tiempoMax, 'g-', linewidth = 1.5)

    #Representación de los intervalos
    ax.fill_between(t, [medias['C'] - desv['C']] * tiempoMax, [medias['C'] + desv['C']] * tiempoMax, color='r',
                    alpha=.2)
    ax.fill_between(t, [medias['H'] - desv['H']] * tiempoMax, [medias['H'] + desv['H']] * tiempoMax, color='b',
                    alpha=.2)
    ax.fill_between(t, [medias['R'] - desv['R']] * tiempoMax, [medias['R'] + desv['R']] * tiempoMax, color='g',
                    alpha=.2)

    plt.title('Montecarlo en redes ER')
    ax.set_ylabel('Proporción')
    ax.set_xlabel('Tiempo')
    ax.set_ylim([0.20,0.45])
    classes = ['Corruptos', 'Honestos', 'Reservados']
    class_colours = ['r', 'b', 'g']
    recs = []
    for i in range(0, len(class_colours)):
        recs.append(mpatches.Rectangle((0, 0), 1, 1, fc = class_colours[i]))
    ax.legend(recs, classes, loc = 4, fancybox = True, framealpha = 0.7)
    #ax.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0., fancybox = True, framealpha = 0.5)
    plt.show()

'''def dibujaGrafica(propC, propH, propR):
    import matplotlib.pyplot as plt
    import matplotlib.patches as mpatches
    t = np.arange(0., len(propC))
    fig, ax = plt.subplots(1)
    ax.plot(t, propC, 'r-', linewidth = 1.0, alpha = 0.8, label = 'Corruptos')
    ax.plot(t, propH, 'b-', linewidth = 1.0, alpha = 0.8, label = 'Honestos')
    ax.plot(t, propR, 'g-', linewidth = 1.0, alpha = 0.8, label = 'Reservados')

    ax.plot(t, [propC.mean(0)] * len(propC), 'r-', linewidth = 1.5)
    ax.plot(t, [propH.mean(0)] * len(propC), 'b-', linewidth = 1.5)
    ax.plot(t, [propR.mean(0)] * len(propC), 'g-', linewidth = 1.5)

    ax.set_ylabel('Proporción')
    ax.set_xlabel('Tiempo')
    classes = ['Corruptos', 'Honestos', 'Reservados']
    class_colours = ['r', 'b', 'g']
    recs = []
    for i in range(0, len(class_colours)):
        recs.append(mpatches.Rectangle((0, 0), 1, 1, fc = class_colours[i]))
    ax.legend(recs, classes, loc = 4, fancybox = True, framealpha = 0.7)
    #ax.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0., fancybox = True, framealpha = 0.5)
    plt.show()'''

def copy(src, dest):
    import shutil, errno
    try:
        shutil.copytree(src, dest)
    except OSError as e:
        # If the error was caused because the source wasn't a directory
        if e.errno == errno.ENOTDIR:
            shutil.copy(src, dest)
            print('Directory successfully copied.')
        else:
            print('Directory not copied. Error: %s' % e)