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

#Exemplo.ybus()
#Exemplo.Sinjetada()
#Exemplo.setJacob(listTensao=[2], listAng=[2,3])

#print('Os dados de dados', Exemplo.getDados().get(0)['code'])

#Exemplo.linearSystem()

Exemplo.solveCircuito(iteracoes=5,listTensao=[2],listAng=[2,3])

nPQA = 0
nPVA = 0 

#for i in Exemplo.getDados():
#    print('Valor de i =', Exemplo.getDados().get(i)['code'])
#    if Exemplo.getDados().get(i)['code'] == 2:
#        nPQA += 1
#        
#    elif Exemplo.getDados().get(i)['code'] == 3:
#        nPVA += 1
#        
#    else:
#        print('Erro')
#print('O valor de nPQ={}, e nPV={}.'.format(nPQA,nPVA))
#