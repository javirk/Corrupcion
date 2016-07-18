import sys
sys.path.insert(0, '/Settings')

import Settings.settingsMK as st, random, numpy as np

def multiplica(modo, H, C, iPers, red):
	producto = 1
	if modo == 'alfa':
		for i in range(0, red.conec[iPers]):
			indice = red.conex[iPers][i]
			indice = indice.astype(int)
			producto *= 1 - float(st.lista['alfa'])*float(C[indice])
	else:
		for i in range(0, red.conec[iPers]):
			indice = red.conex[iPers][i]
			indice = indice.astype(int)
			producto *= 1 - float(st.lista['beta'])*float(H[indice])

	return producto

def creaPersonas(H, C):
	Ntotal = len(H)
	for i in range(0, Ntotal):
		Hi = random.random()
		Ci = random.random()
		Ri = random.random()
		H[i] = Hi/(Hi+Ci+Ri)
		C[i] = Ci/(Hi+Ci+Ri)

	return H, C