from classNewton import Newton


Exemplo = Newton()

Exemplo.setBarra(1, 1, 1.04, 0, 0 + 0*1j, 0 + 0*1j) 
Exemplo.setBarra(2, 2, 1.00, 0, 100e6 + 50e6*1j, 0 + 0*1j) # Chutar o valor de tensão em barras PQ
Exemplo.setBarra(3, 3, 1.02, 0, 0 + 0*1j, 70e6 + 0*1j) # Barra PV

Exemplo.printBarra()
Exemplo.setSesp()

Exemplo.ligacoes(1,2, impedancia=0.05 + 0.4j)
Exemplo.ligacoes(1,3, impedancia=0.3 + 0.46j)
Exemplo.ligacoes(2,3, impedancia=0.01 + 0.09j)

Exemplo.printLigacoes()

Exemplo.ybus()