import random, pandas as pd, Clases.redClase as rClass, numpy as np, configparser as cp
import prettyplotlib as ppl

import matplotlib.pyplot as plt
import matplotlib as mpl
from prettyplotlib import brewer2mpl

import statistics
from tqdm import tqdm

class Town:
    def __init__(self, rutaconf = '../Settings/settings.ini', ired = 0):
        #Pasar todos los parámetros a variables usables leyendo del archivo de configuracion
        self.Config = cp.ConfigParser()
        self.Config.read(rutaconf)
        secc = self.Config.sections()

        self.ired = ired
        self.sistema = {}
        self.red = {}
        self.ejecucion = {}
        self.version = {}

        self.leeConfig(secc)

        if self.version['version'] == 2:
            self.sistema['delta1']  = 0

        self.rutaRed = 'red_'+str(ired)+'.txt'

        #Declara variables importantes
        self.S = [None]*self.red['n']
        if self.ejecucion['buscalinks']:
            self.links = self.creaLinks()
        else:
            self.links = 0

        self.propC = []
        self.propH = []
        self.propR = []
        self.mediaTotal = {'H': 0, 'C': 0, 'R': 0}
        self.desvTotal = {'H': 0, 'C': 0, 'R': 0}

        if self.ejecucion['tipometodo'] == 'par':
            self.c1 = self.ejecucion['cantidad1']
            self.c2 = self.ejecucion['cantidad2']
            self.nombrePar1 = self.ejecucion['nombrepar1']
            self.nombrePar2 = self.ejecucion['nombrepar2']

        #Crea la red que se pide con la cantidad de nodos que pone
        if self.red['tipored'] == 'BA':
            self.R = rClass.redBA(guardar=self.red['guardar'], archivo=True, ruta=self.rutaRed, k=self.red['k'], N=self.red['n'])
        elif self.red['tipored'] == 'AL':
            self.R = rClass.redAL(guardar=self.red['guardar'], archivo=True, ruta=self.rutaRed)
        else:
            self.R = rClass.redER(guardar=self.red['guardar'], archivo=True, ruta=self.rutaRed, k=self.red['k'], N=self.red['n'])

        self.creaPersonas()

    def leeConfig(self, secc):
        for seccion in secc:
            options = self.Config.options(seccion)
            for option in options:
                if seccion == 'Red':
                    try:
                        self.red[option] = self.Config.getint(seccion, option)
                    except:
                        try:
                            self.red[option] = self.Config.getboolean(seccion, option)
                        except:
                            self.red[option] = self.Config.get(seccion, option)
                elif seccion == 'Sistema':
                    try:
                        self.sistema[option] = self.Config.getfloat(seccion, option)
                    except:
                        try:
                            self.sistema[option] = self.Config.getboolean(seccion, option)
                        except:
                            self.sistema[option] = self.Config.get(seccion, option)
                elif seccion == 'Ejecucion':
                    try:
                        self.ejecucion[option] = self.Config.getint(seccion, option)
                    except:
                        try:
                            self.ejecucion[option] = self.Config.getboolean(seccion, option)
                        except:
                            self.ejecucion[option] = self.Config.get(seccion, option)
                elif seccion == 'Version':
                    try:
                        self.version[option] = self.Config.getint(seccion, option)
                    except:
                        try:
                            self.version[option] = self.Config.getboolean(seccion, option)
                        except:
                            self.version[option] = self.Config.get(seccion, option)
                else:
                    print("Hay un error en el archivo de configuración")
                    exit()

    def evoluciona(self, b, beta):
        if self.ejecucion['tipometodo'] == 'tiempo':
            for t in range(0, self.ejecucion['tterma']):
                self.montecarlo()

            # Acabamos de termalizar, toca medir.
            for t in range(0, self.ejecucion['tmedida']):
                if self.ejecucion['buscalinks']:
                    self.links.loc[t + 1] = self.links.loc[t]

                self.montecarlo()

                self.propC.append(self.S.count('C') / self.red['n'])
                self.propH.append(self.S.count('H') / self.red['n'])
                self.propR.append(self.S.count('R') / self.red['n'])

        elif self.ejecucion['tipometodo'] == 'par':
            self.sistema['b'] = b
            self.sistema['beta'] = beta
            #Evolución por parámetro
            self.parametro1 = [None] * self.c1
            self.parametro2 = [None] * self.c2

            self.mediaParC = [[0 for i in range(self.c2)] for j in range(self.c1)]

            for i in tqdm(range(0, self.c1)):
                if self.c1 > 1:
                    self.sistema[self.nombrePar1] = self.sacaParametro(i, self.c1)
                self.parametro1[i] = self.sistema[self.nombrePar1]

                for j in range(0, self.c2):
                    if self.c2 > 1:
                        self.sistema[self.nombrePar2] = self.sacaParametro(j, self.c2)
                    self.parametro2[j] = self.sistema[self.nombrePar2]
                    #print(self.nombrePar2 + ' = ' + str(self.parametro2[j]))

                    for t in range(0, self.ejecucion['tterma']):
                        self.montecarlo()

                    for t in range(0, self.ejecucion['tmedida']):
                        self.montecarlo()

                        self.propC.append(self.S.count('C') / self.red['n'])
                        self.propH.append(self.S.count('H') / self.red['n'])
                        self.propR.append(self.S.count('R') / self.red['n'])

                    self.mediaParC[i][j] = sum(self.propC) / float(len(self.propC))
                    self.creaPersonas()
                    self.propC = []
                    self.propH = []
                    self.propR = []

    def analiza(self):
        self.mediaTotal['C'] = sum(self.propC)/float(len(self.propC))
        self.desvTotal['C'] = statistics.stdev(self.propC)
        self.mediaTotal['H'] = sum(self.propH)/float(len(self.propH))
        self.desvTotal['H'] = statistics.stdev(self.propH)
        self.mediaTotal['R'] = sum(self.propR)/float(len(self.propR))
        self.desvTotal['R'] = statistics.stdev(self.propR)

        #self.sacaResultados()

    def sacaResultados(self):
        resu = ['H = ' + str(float("{0:.7f}".format(self.mediaTotal['H']))) + ' ± ' + str(
            float("{0:.7f}".format(self.desvTotal['H']))) + '\n',
                'C = ' + str(float("{0:.7f}".format(self.mediaTotal['C']))) + ' ± ' + str(
                    float("{0:.7f}".format(self.desvTotal['C']))) + '\n',
                'R = ' + str(float("{0:.7f}".format(self.mediaTotal['R']))) + ' ± ' + str(
                    float("{0:.7f}".format(self.desvTotal['R']))) + '\n']
        for i in range(0, len(resu)):
            print(resu[i])

    def escribeTodo(self, carpeta, b, beta, r):
        if self.ejecucion['tipometodo'] == 'tiempo':
            nombre = carpeta + '/resu_r' + str(self.ired) + '.txt'
            outfile = open(nombre, 'wt')
            for t in range(0, len(self.propC)):
                l = [str(t), str(self.propC[t]), str(self.propH[t]), str(self.propR[t])]
                data = '\t'.join("%s" % x for x in l)
                data += "\n"
                outfile.write(data)
            outfile.close()

        elif self.ejecucion['tipometodo'] == 'par':
            if self.c2 > 1:
                nombre = carpeta + '/par_' + str(self.ired) + '_' + str(self.nombrePar1) + str(
                    self.nombrePar2) + '.txt'
                outfile = open(nombre, 'wt')
            else:
                bst = "%0.2f" % b
                rst = "%0.2f" % r
                betast = "%0.2f" % beta
                nombre = carpeta + '/par_' + bst + '_' + rst + '_' + betast + '.txt'

                print(nombre)
                outfile = open(nombre, 'wt')

            for i in range(0, self.c1):
                if self.c2 > 1:
                    for j in range(0, self.c2):
                        l = [str(float("{0:.3f}".format(self.parametro1[i]))), str(float("{0:.4f}".format(self.parametro2[j]))),
                             str(float("{0:.4f}".format(self.mediaParC[i][j])))]
                        data = '\t'.join("%s" % x for x in l)
                        data += "\n"
                        outfile.write(data)
                else:
                    l = [str(float("{0:.3f}".format(self.parametro1[i]))),
                         str(float("{0:.4f}".format(self.mediaParC[i][0])))]
                    data = '\t'.join("%s" % x for x in l)
                    outfile.write(data)
                data = "\n"
                outfile.write(data)

            outfile.close()

        self.escribeConf(carpeta)

    def escribeConf(self, carpeta):
        #ConfigW en el que se escribe
        configW = cp.ConfigParser()
        secc = self.Config.sections()
        for seccion in secc:
            configW.add_section(seccion)
            if seccion == 'Red':
                for valor in self.red:
                    configW.set(seccion, valor, str(self.red[valor]))
            elif seccion == 'Sistema':
                for valor in self.sistema:
                    configW.set(seccion, valor, str(self.sistema[valor]))
            elif seccion == 'Ejecucion':
                for valor in self.ejecucion:
                    configW.set(seccion, valor, str(self.ejecucion[valor]))
            elif seccion == 'Version':
                for valor in self.version:
                    configW.set(seccion, valor, str(self.version[valor]))

        with open(carpeta+'/par.cfg', 'w') as configfile:
            configW.write(configfile)

    def rellena(self):
        for nodo in range(0, self.red['n']):
            for i in range(0, self.red.conec[nodo]):
                if self.red.conex[nodo][i] > nodo:
                    ilink = self.S[int(nodo)] + self.S[int(self.red.conex[nodo][i])]
                    ilink = ''.join(sorted(ilink))
                    self.links[ilink][0] += 1

    def montecarlo(self):
        Scopia = [x[:] for x in self.S]
        for iPers in range(0, self.red['n']):
            producto = 1
            if self.S[iPers] == 'R':
                if random.random() < self.sistema['r']:
                    Scopia[iPers] = 'H'
            elif self.S[iPers] == 'H':
                if random.random() < self.sistema['delta1']:
                    Scopia[iPers] = 'C'
                else:
                    for j in range(0, self.R.conec[iPers][0]):
                        indice = self.R.conex[iPers][j]
                        indice = indice.astype(int)
                        if self.S[indice] == 'C':
                            producto *= 1 - self.sistema['alfa']

                    prob = producto
                    if random.random() > prob:
                        Scopia[iPers] = 'C'
            else:
                if self.version['version'] == 1:
                    for j in range(0, self.R.conec[iPers]):
                        indice = self.R.conex[iPers][j]
                        indice = indice.astype(int)
                        if self.S[indice] == 'R':
                            producto *= (1 - self.sistema['delta2'])
                    prob = 1 - producto
                elif self.version['version'] == 2:
                    cuentaR = self.S.count('R')
                    prob = cuentaR / len(self.S)
                else:
                    # Si es Corrupto puede pasar a Honesto con delta2:
                    prob = self.sistema['delta2']

                if random.random() < prob:
                    Scopia[iPers] = 'H'
                else:
                    producto = 1
                    if random.random() < self.sistema['b']:
                        Scopia[iPers] = 'R'
                    else:
                        for j in range(0, self.R.conec[iPers][0]):
                            indice = self.R.conex[iPers][j]
                            indice = indice.astype(int)
                            if self.S[indice] == 'H':
                                producto *= (1 - self.sistema['beta'])

                        prob = producto
                        if random.random() > prob:
                            Scopia[iPers] = 'R'

            if self.ejecucion['buscalinks']:
                self.cambiaLink(Scopia, iPers)
        self.S = [x[:] for x in Scopia]

    def creaLinks(self):
        self.links = pd.DataFrame([[0] * 6], columns=['HH', 'CC', 'RR', 'CH', 'HR', 'CR'])

        # Rellena el dataframe ese
        self.rellena()

        return self.links

    def cambiaLink(self, Scopia, pers):
        for inodo in range(0, self.red.conec[pers]):
            if self.R.conex[pers][inodo] < pers:
                ilink = Scopia[int(pers)] + Scopia[int(self.R.conex[pers][inodo])]
                # Lo ordeno alfabéticamente para no tener problemas
                ilink = ''.join(sorted(ilink))
                self.links[ilink][len(self.links) - 1] += 1

                ilink = self.S[int(pers)] + self.S[int(self.R.conex[pers][inodo])]
                ilink = ''.join(sorted(ilink))
                self.links[ilink][len(self.links) - 1] -= 1

    def creaPersonas(self):
        for i in range(0, self.red['n']):
            if random.random() < self.sistema['prophon']:
                self.S[i] = 'H'
            else:
                self.S[i] = 'C'

    def representaPar(self):
        if self.c2 == 1:
            fig, ax = plt.subplots(1)
            ppl.plot(self.parametro1, self.mediaParC)
            fig.savefig('plot_prettyplotlib_default.png')

    def sacaParametro(self, i, cant):
        sup = 1.0
        inf = 0.0

        par = ((sup - inf) / float(cant)) * i + inf

        return par