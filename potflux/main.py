from classNewton import Newton

Exemplo = Newton()

Exemplo.setBarra(1, 1, 1.05, 0.00, 0 + 0*1j, 0 + 0*1j) # Barra V e Ang 
Exemplo.setBarra(2, 2, 1.00, 0.00, 400e6 + 250e6*1j, 0 + 0*1j) # Chutar o valor de tensão em Barras PQ
Exemplo.setBarra(3, 3, 1.04, 0.00, 0 + 0*1j, 200e6 + 0*1j) # Barra PV

Exemplo.printBarra()
Exemplo.setSesp()

Exemplo.ligacoes(1,2, impedancia=0.05 + 0.4j)
Exemplo.ligacoes(1,3, impedancia=0.3 + 0.46j)
Exemplo.ligacoes(2,3, impedancia=0.01 + 0.09j)

Exemplo.printLigacoes()

Exemplo.solveCircuito(iteracoes=5,listTensao=[2],listAng=[2,3])

