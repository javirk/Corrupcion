import sys
sys.path.insert(0, '/Settings')
sys.path.insert(0, '/Funciones')

import Funciones.funcionesER as fER, Funciones.funcionesMK as fun, numpy as np
import Settings.settingsMK as st

st.init()

#Variables importantes
N = st.lista['N']
k = st.lista['k']
tiempo = st.lista['tiempo']
H = np.zeros((N, 1))
C = np.zeros((N, 1))

R = fER.red(guardar = st.lista['guardar'], archivo = False, k = k, N = N, tipo = 'ER')
H, C = fun.creaPersonas(H, C)
Hcopia = H
Ccopia = C

for itiempo in range(0, tiempo):
	for iPers in range(0, N):
		productobeta = fun.multiplica('beta', H, C, iPers, R)
		productoalfa = fun.multiplica('alfa', H, C, iPers, R)

		T13 = (1-st.lista['delta2'])*(1-(1-st.lista['b'])*productobeta)
		T32 = 1-(1-st.lista['delta1'])*productoalfa
		T21 = st.lista['r']
		T33 = (1-st.lista['delta2'])*(1-st.lista['b'])*productobeta

		Z = T13*T32 + T21*(1-T33) + T21*T32

		Hcopia[iPers] = T21*(1-T33)/Z
		Ccopia[iPers] = T21*T32/Z

	H = Hcopia
	C = Ccopia