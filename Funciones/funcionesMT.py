import sys
sys.path.insert(0, '/Settings')

import Settings.settingsMT as st, random, Settings.settingsAN as settingsAN, numpy as np, math, pandas as pd

def sacaParametro(i, cant):
    sup = 0.5
    inf = 0

    par = ((sup-inf)/float(cant))*i

    return par

def creaPersonas(S):
    N = len(S)
    for i in range(0, N):
        if random.random() < st.lista['inicialHonestos']:
            S[i] = 'H'
        else:
            S[i] = 'C'

    return S

def creaLinks(S, red):
    links = pd.DataFrame([[0]*6], columns = ['HH', 'CC', 'RR', 'CH', 'HR', 'CR'])

    #Rellena el dataframe ese
    links = rellena(S, links, red)

    return links

def rellena(S, links, red):
    for nodo in range(0, len(S)):
        for i in range(0, red.conec[nodo]):
            if red.conex[nodo][i] > nodo:
                ilink = S[int(nodo)] + S[int(red.conex[nodo][i])]
                ilink = ''.join(sorted(ilink))
                links[ilink][0] += 1
    return links

    #rellena(S, nodo+1, links, red)
    
def escribeTodo(propC, propH, propR, iRed, carpeta):
    nombre = carpeta+'/resu_r' + str(iRed) + '.txt'
    outfile = open(nombre, 'wt')
    for t in range(0, len(propC)):
        l = [str(t), str(propC[t]), str(propH[t]), str(propR[t])]
        data = '\t'.join("%s" % x for x in l)
        data += "\n"
        outfile.write(data)
    outfile.close()

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

def montecarlo(S, red, links = 0):
    cambios = st.lista['cambios']
    Scopia = [x[:] for x in S]
    for iPers in range(0, len(S)):
        producto = 1
        if S[iPers] == 'R':
            if random.random() < st.lista['r']:
                Scopia[iPers] = 'H'
        elif S[iPers] == 'H':
            if random.random() < st.lista['delta1']:
                Scopia[iPers] = 'C'
            else:
                for j in range(0, red.conec[iPers]):
                    indice = red.conex[iPers][j]
                    indice = indice.astype(int)
                    if S[indice] == 'C':
                        producto *= 1 - st.lista['alfa']

                prob = producto
                if random.random() > prob:
                    Scopia[iPers] = 'C'
        else:
            if cambios == 1:
                for j in range(0, red.conec[iPers]):
                    indice = red.conex[iPers][j]
                    indice = indice.astype(int)
                    if S[indice] == 'R':
                        producto *= (1 - st.lista['delta2'])
                prob = 1-producto
            elif cambios == 2:
                cuentaR = S.count('R')
                prob = cuentaR/len(S)
            else:
                #Si es Corrupto puede pasar a Honesto con delta2:
                prob = st.lista['delta2']

            if random.random() < prob:
                Scopia[iPers] = 'H'
            else:
                producto = 1
                if random.random() < st.lista['b']:
                    Scopia[iPers] = 'R'
                else:
                    for j in range(0, red.conec[iPers]):
                        indice = red.conex[iPers][j]
                        indice = indice.astype(int)
                        if S[indice] == 'H':
                            producto *= (1 - st.lista['beta'])

                    prob = producto
                    if random.random() > prob:
                        Scopia[iPers] = 'R'

        if st.lista['buscaLink']:
            links = cambiaLink(S, Scopia, iPers, links, red)
    S = [x[:] for x in Scopia]
    return S

def cambiaLink(S, Scopia, pers, links, red):
    for inodo in range(0, red.conec[pers]):
        if red.conex[pers][inodo] < pers:
            ilink = Scopia[int(pers)] + Scopia[int(red.conex[pers][inodo])]
            #Lo ordeno alfabéticamente para no tener problemas
            ilink = ''.join(sorted(ilink))
            links[ilink][len(links)-1] += 1

            ilink = S[int(pers)] + S[int(red.conex[pers][inodo])]
            ilink = ''.join(sorted(ilink))
            links[ilink][len(links)-1] -= 1

    return links

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

def dibujaGrafica(propC, propH, propR):
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
    ax.legend(recs, classes, loc = 4, fancybox = True, framealpha = 0.6)
    #ax.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0., fancybox = True, framealpha = 0.5)
    plt.show()