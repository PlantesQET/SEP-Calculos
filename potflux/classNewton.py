import cmath as cmt
import math as mt
import numpy as np
import matplotlib.pyplot as plt

class Newton:
    def __init__(self) -> None:
        print('Classe Newton Criada')
        self.__Sbase = 100e6

        self.__Sesp = dict()
        self.__Sbarras = dict()

        self.__dados = dict()
        self.__tensaoPlot = dict()
        self.__angPlot = dict()

        self.__Ligacoes = dict()
        self.__ybus = list()

        # Contadores de barras
        self.__nPQ = int()
        self.__nPV = int()
        self.__listTensao = list()
        self.__listAng = list()

        # Submatrizes da Jacobiana
        self.__Jacob = list()
        self.__J1 = list()
        self.__J2 = list()
        self.__J3 = list()
        self.__J4 = list()

        self.__x = list()


    def setBarra(self, barra, code, tensao, ang, carga, geracao):
        """
        codes: 1 - Tensão e Angulo; 2 -> P e Q; 3 -> P e V.
        
        ang -> graus
        tensao -> pu
        carga e geracao -> VA

        """
        self.__dados[barra] = {'code' : code, 'tensao' : tensao, 'ang' : mt.radians(ang), 
                               'carga' : (carga/self.__Sbase), 'geracao' : (geracao/self.__Sbase)}
        
        self.__tensaoPlot[barra] = [tensao]
        self.__angPlot[barra] = [ang]
    
    def printBarra(self):
        """
        Método printa as informações
        """
        print('\n\n =================== DADOS: =======================')
        print('Sbase = ', self.__Sbase, ' VA')
        for i in self.__dados: print(self.__dados[i])
        print('==================================================')
    
    def setSesp(self):
        """
        Método utilizado para calcular a potencia especifica de cada barra. Os valores
        automaticamente.
        """
        for i in self.__dados:
            if self.__dados[i]['code'] == 2: # Barra tipo PQ
                self.__Sesp[i] = {'Pesp' : np.real(self.__dados.get(i)['geracao'] - self.__dados.get(i)['carga']),
                                  'Qesp' : float(
                                    np.imag(self.__dados.get(i)['geracao'] - self.__dados.get(i)['carga'])
                                  )}
            elif self.__dados[i]['code'] == 3: # Barra tipo PV
                self.__Sesp[i] = {'Pesp' : np.real(self.__dados.get(i)['geracao'] - self.__dados.get(i)['carga']),
                                  'Qesp' : float(
                                    np.imag(self.__dados.get(i)['geracao'] - self.__dados.get(i)['carga'])
                                  )}
        
        print('\n\n =================== DADOS: =======================')
        print(self.__Sesp, ' pu')
        print('==================================================')
    
    def ligacoes(self, barra1, barra2, impedancia=None, admitancia=None):
        """
        Define as ligações ligadas entre a barra 1 e a barra 2

        As informações devem estar em PU
        """
        if impedancia is None:
            impedancia = 1/admitancia
        elif admitancia is None:
            admitancia = 1/impedancia
        else:
            return 'ERRO! A Admitancia ou impedancia devem ser informadas'
        
        self.__Ligacoes[(barra1,barra2)] = {'Impedancia' : impedancia,
                                            'Admitancia' : admitancia}
        
    def printLigacoes(self):
        """
        Método imprime as ligações entre as barra
        """
        print('\n\n =================== LIGAÇÕES: =======================')
    
        for i in self.__Ligacoes: print('Ligação ', i, '\t', self.__Ligacoes[i])
        print('==================================================')
    
    def __printYbus(self):
        print('\n\n =================== YBUS: =======================')
        for i in self.__ybus: print(i)
        print('==================================================')

    def ybus(self):
        self.__ybus = np.ones((len(self.__dados), len(self.__dados)), dtype=complex)

        for i in range(len(self.__ybus)):
            lin = []
            for j in range(len(self.__ybus)):
                if i==j:
                    lin.append(0)
                else:
                    if self.__Ligacoes.__contains__(tuple([i + 1, j + 1])):
                        lin.append(-self.__Ligacoes.get(tuple([i + 1, j + 1]))['Admitancia'])
                    elif self.__Ligacoes.__contains__(tuple([j + 1, i + 1])):
                        lin.append(-self.__Ligacoes.get(tuple([j + 1, i + 1]))['Admitancia'])
                    else:
                        lin.append(0)
            for j in range(len(self.__ybus)):
                if i==j:
                    lin[j] = -1 * sum(lin)
            self.__ybus[i] = lin

        for i in self.__dados:
            #print('Valor de i =', len(self.__dados))
            if self.__dados.get(i)['code'] == 2:
                self.__nPQ += 1
                print('Valor de NPQ', self.__nPQ)
            elif self.__dados.get(i)['code'] == 3:
                self.__nPV += 1
                print('Valor de NPV', self.__nPV)
            else:
                print('Erro')
                #return 'Erro!'
        
        self.__printYbus()
        #print('O valor de nPQ={}, e nPV={}.'.format(self.__nPQ,self.__nPV))
    def printValores(self):
        print('O valor de nPQ={}, e nPV={}.'.format(self.__nPQ,self.__nPV))

    def Sinjetada(self):
        
        self.__Sinjetada = dict()
        self.__deltaPeQ = []
        self.__ResiduoP = []
        self.__ResiduoQ = []

        for i in self.__dados:
            soma1 = []
            soma2 = []
            if self.__dados[i]['code'] != 1:
                for j in self.__dados:
                    soma1.append(
                        #Potencia Ativa
                        abs(self.__ybus[i-1][j-1]) *
                        abs(self.__dados.get(i)['tensao']) *
                        abs(self.__dados.get(j)['tensao']) *
                        mt.cos(np.angle(self.__ybus[i-1][j-1]) 
                            - self.__dados.get(i)['ang'] 
                            + self.__dados.get(j)['ang'])
                    )

                    soma2.append(
                        #Potencia Reativa
                        -abs(self.__ybus[i-1][j-1]) *
                        abs(self.__dados.get(i)['tensao']) *
                        abs(self.__dados.get(j)['tensao']) *
                        mt.sin(np.angle(self.__ybus[i-1][j-1]) 
                            - self.__dados.get(i)['ang'] 
                            + self.__dados.get(j)['ang'])
                    )
                self.__ResiduoP.append(
                    np.real(
                        self.__Sesp.get(i)['Pesp'] - sum(soma1)
                    )
                )
                if self.__dados[i]['code'] == 2:
                    self.__ResiduoQ.append(
                        np.imag(self.__Sesp.get(i)['Qesp'] * 1j - sum(soma2))
                    )
        for i in range(len(self.__ResiduoP)):
            self.__deltaPeQ.append(self.__ResiduoP[i])
        for i in range(len(self.__ResiduoQ)):
            self.__deltaPeQ.append(self.__ResiduoQ[i])

        for i in self.__deltaPeQ: print(i)

    def __setJ1(self, listAng, nPQ, nPV):
        """
        Método privado usado para calcular a submatriz J1 da matriz Jacobiana
        
        :param listAng: Lista de angulos a serem calculados no circuito. ( Barras PQ e PV).
        :param nPQ: numero de barra PQ.
        :param nPV: número de barras PV.

        return: retorna a matriz J1.
        """
        self.__J1 = np.ones((nPQ + nPV, nPQ + nPV))

        mainDiagonal = []
        outDiagonal = []

        for i in listAng:
            soma = []
            for j in range(1,len(self.__dados) + 1, 1):
                if i != j:
                    soma.append(
                        abs(self.__ybus[i-1][j-1]) * 
                        abs(self.__dados.get(i)['tensao']) *
                        abs(self.__dados.get(j)['tensao']) *
                        cmt.sin(cmt.phase(self.__ybus[i-1][j-1])- 
                                self.__dados.get(i)['ang'] +
                                self.__dados.get(j)['ang']
                                )
                    )
            mainDiagonal.append(sum(soma))
        
        for i in listAng:
            for j in listAng:
                if i != j:
                    outDiagonal.append(
                        -abs(self.__ybus[i-1][j-1]) * 
                        abs(self.__dados.get(i)['tensao']) *
                        abs(self.__dados.get(j)['tensao']) *
                        cmt.sin(cmt.phase(self.__ybus[i-1][j-1])- 
                                self.__dados.get(i)['ang'] +
                                self.__dados.get(j)['ang']
                                )
                    )
        m = 0
        for i in range(len(listAng)):
            for j in range(len(listAng)):
                if i == j:
                    self.__J1[i][j] = np.real(mainDiagonal[j])
                else:
                    self.__J1[i][j] = np.real(outDiagonal[m])
                    m += 1
        
        print('\n J1 = \n', self.__J1)
        
        return self.__J1
    
    def __setJ2(self, listTensao, listAng, nPQ, nPV):
        """
        Método privado usado para calcular a submatriz J2 da matriz Jacobiana
        
        :param listTensao: Lista de angulos a serem calculados no circuito. ( Barras PQ e PV).
        :param nPQ: numero de barra PQ.
        :param nPV: número de barras PV.

        return: retorna a matriz J1.
        """
        self.__J2 = np.ones((nPQ + nPV, nPQ))

        mainDiagonal = []
        outDiagonal = []

        for i in listAng:
            soma = []
            a = 0
            for j in range(1,len(self.__dados) + 1, 1):
                if i != j:
                    soma.append(
                        abs(self.__ybus[i-1][j-1]) * 
                        abs(self.__dados.get(j)['tensao']) *
                        cmt.cos(cmt.phase(self.__ybus[i-1][j-1])- 
                                self.__dados.get(i)['ang'] +
                                self.__dados.get(j)['ang']
                                )
                    )
            a = (   2 * abs(self.__dados.get(i)['tensao']) * abs(self.__ybus[i-1][i-1]) *
                    cmt.cos(cmt.phase(self.__ybus[i-1][i-1])))
            
            mainDiagonal.append(a + sum(soma))
        
        for i in listAng:
            for j in listTensao:
                if i != j:
                    outDiagonal.append(
                        abs(self.__ybus[i-1][j-1]) * 
                        abs(self.__dados.get(i)['tensao']) *
                        cmt.cos(cmt.phase(self.__ybus[i-1][j-1])- 
                                self.__dados.get(i)['ang'] +
                                self.__dados.get(j)['ang']
                                )
                    )
        m = 0
        for i in range(nPQ + nPV):
            k = nPV
            for j in range(nPQ):
                if i < nPV:
                    self.__J2[i][j] = np.real(outDiagonal[m])
                    m += 1
                elif i>= nPV:
                    if i - nPV == j:
                        self.__J2[i][j] = np.real(mainDiagonal[j + nPV])
                        k += 1
                    else:
                        self.__J2[i][j] = np.real(outDiagonal[m])
                        m += 1
        
        print('\n K = ', k, '\n')
        print('\n J2 = \n', self.__J2)
        
        return self.__J2



    def __setJ3(self, listTensao, listAng, nPQ, nPV):
        """
        Método privado usado para calcular a submatriz J2 da matriz Jacobiana
        
        :param listTensao: Lista de angulos a serem calculados no circuito. ( Barras PQ e PV).
        :param nPQ: numero de barra PQ.
        :param nPV: número de barras PV.

        return: retorna a matriz J1.
        """
        self.__J3 = np.ones((nPQ , nPQ + nPV))

        mainDiagonal = []
        outDiagonal = []

        for i in listAng:
            soma = []
            for j in range(1,len(self.__dados) + 1, 1):
                if i != j:
                    soma.append(
                        abs(self.__ybus[i-1][j-1]) * 
                        abs(self.__dados.get(i)['tensao']) *
                        abs(self.__dados.get(j)['tensao']) *
                        cmt.cos(cmt.phase(self.__ybus[i-1][j-1]) - 
                                self.__dados.get(i)['ang'] +
                                self.__dados.get(j)['ang']
                                )
                    )
            
            mainDiagonal.append(sum(soma))
        
        for i in listAng:
            for j in listTensao:
                if i != j:
                    outDiagonal.append(
                        -abs(self.__ybus[i-1][j-1]) * 
                        abs(self.__dados.get(i)['tensao']) *
                        abs(self.__dados.get(j)['tensao']) *
                        cmt.cos(cmt.phase(self.__ybus[i-1][j-1])- 
                                self.__dados.get(i)['ang'] +
                                self.__dados.get(j)['ang']
                                )
                    )
        m = 0
        for i in range(nPQ):
            for j in range(nPQ + nPV):
                if j < nPV:
                    self.__J3[i][j] = np.real(outDiagonal[m])
                    m += 1
                elif j >= nPV:
                    if j - nPV == i:
                        self.__J3[i][j] = np.real(mainDiagonal[i + nPV])
                    else:
                        self.__J3[i][j] = np.real(outDiagonal[m])
                        m += 1
        

        print('\n J3 = \n', self.__J3)
        
        return self.__J3
    

    def __setJ4(self, listTensao, listAng, nPQ, nPV):
        """
        Método privado usado para calcular a submatriz J2 da matriz Jacobiana
        
        :param listTensao: Lista de angulos a serem calculados no circuito. ( Barras PQ e PV).
        :param nPQ: numero de barra PQ.
        :param nPV: número de barras PV.

        return: retorna a matriz J1.
        """
        self.__J4 = np.ones((nPQ, nPQ))

        mainDiagonal = []
        outDiagonal = []

        for i in listAng:
            soma = []
            a = 0
            for j in range(1,len(self.__dados) + 1, 1):
                if i != j:
                    soma.append(
                        abs(self.__ybus[i-1][j-1]) * 
                        abs(self.__dados.get(j)['tensao']) *
                        cmt.sin(cmt.phase(self.__ybus[i-1][j-1])- 
                                self.__dados.get(i)['ang'] +
                                self.__dados.get(j)['ang']
                                )
                    )
            a = (   2 * abs(self.__dados.get(i)['tensao']) * abs(self.__ybus[i-1][i-1]) *
                    cmt.sin(cmt.phase(self.__ybus[i-1][i-1])))
            
            mainDiagonal.append(- a - sum(soma))
        
        for i in listAng:
            for j in listTensao:
                if i != j:
                    outDiagonal.append(
                        -abs(self.__ybus[i-1][j-1]) * 
                        abs(self.__dados.get(i)['tensao']) *
                        cmt.sin(cmt.phase(self.__ybus[i-1][j-1]) - 
                                self.__dados.get(i)['ang'] +
                                self.__dados.get(j)['ang']
                                )
                    )
        m = 0
        for i in range(nPQ):
            for j in range(nPQ):
                if i == j:
                    self.__J4[i][j] = np.real(mainDiagonal[j + nPV])
                   
                else:
                    self.__J4[i][j] = np.real(outDiagonal[m])
                    m += 1
        
        #print('\n K = ', k, '\n')
        print('\n J4 = \n', self.__J4)
        
        return self.__J4
    
    def setJacob(self, listTensao, listAng):

        
        print(f'Barras PQ = {self.__nPQ} e PV = {self.__nPV}')

        self.__Jacob = []
        self.__listTensao = listTensao
        self.__listAng = listAng

        nXn = len(listTensao) + len(listAng)

        J1 = self.__setJ1(listAng, self.__nPQ, self.__nPV)
        J2 = self.__setJ2(listTensao, listAng, self.__nPQ, self.__nPV)
        J3 = self.__setJ3(listTensao, listAng, self.__nPQ, self.__nPV)
        J4 = self.__setJ4(listTensao, listAng, self.__nPQ, self.__nPV)

        self.__Jacob = np.zeros((nXn, nXn))

        for i in range(nXn):
            h = []
            k = []

            if i < len(J1):
                for j in range(len(J1[i])): h.append(J1[i][j])
                for j in range(len(J2[i])): h.append(J2[i][j])
                self.__Jacob[i] = np.hstack(h)
            elif i >= len(J1):
                m = i - len(J1)
                for j in range(len(J3[m])): k.append(J3[m][j])
                for j in range(len(J4[m])): k.append(J4[m][j])
                self.__Jacob[i] = np.hstack(k)

        print(' ================== Matriz do Jacob ======================')

        print('\nJ1 = ')
        for i in J1: print(i)
        print('\nJ2 = ')
        for i in J2: print(i)
        print('\nJ3 = ')
        for i in J3: print(i)
        print('\nJ4 = ')
        for i in J4: print(i)

        print('\nJacobiana = ')
        for i in self.__Jacob: print(i)

        print(' =========================================================')

    def getDados(self):
        return self.__dados
    
    def linearSystem(self):
        """
            Método para palcular resultados do sistema linear
            O sistema é do tipo:
                [delta P delta Q] = [Jacobiana] . [Resultado]
        """

        self.__x = []

        self.__x = np.linalg.solve(self.__Jacob, self.__deltaPeQ)
        deucerto = np.allclose(np.dot(self.__Jacob, self.__x), self.__deltaPeQ) 
        print('\n\t Due certo?', deucerto)

        ang = []
        tens = []

        for i in range(len(self.__x)):
            if i < (self.__nPQ + self.__nPV):
                ang.append(self.__x[i])
            else:
                tens.append(self.__x[i])

        m = 0
        for i in range(len(self.__dados)):
            #print('Valor de i agora =', i)
            #print('Dados =', self.__dados.get(i+1)['code'])
            if self.__dados.get(i+1)['code'] != 1:
                self.__dados[i + 1]['ang'] += float(np.real(ang[m]))
                self.__angPlot[i + 1].append(self.__dados[i + 1]['ang'])
                m += 1
        
        m = 0
        for i in range(len(self.__dados)):
            if self.__dados.get(i + 1)['code'] == 2:
                #print('Dados =', self.__dados.get(i+1)['code'])
                self.__dados[i + 1]['tensao'] += float(np.real(tens[m]))
                self.__tensaoPlot[i + 1].append(self.__dados[i + 1]['tensao'])
                m += 1

    def NovaInjecao(self):
        """
        Metodo utilizado para calcular o novo valor de injeção de potencia aparente nas barras de folga e PV.
        (P e Q nas de folga e Q nas P)
        """

        self.__Sbarras = dict()

        for i in self.__dados:
            soma1 = []
            soma2 = []
            if self.__dados[i]['code'] != 2:
                for j in self.__dados:
                    soma1.append(
                        #Potencia Ativa
                        abs(self.__ybus[i-1][j-1]) *
                        abs(self.__dados.get(i)['tensao']) *
                        abs(self.__dados.get(j)['tensao']) *
                        mt.cos(np.angle(self.__ybus[i-1][j-1]) 
                            - self.__dados.get(i)['ang'] 
                            + self.__dados.get(j)['ang'])
                    )

                    soma2.append(
                        #Potencia Reativa
                        -abs(self.__ybus[i-1][j-1]) *
                        abs(self.__dados.get(i)['tensao']) *
                        abs(self.__dados.get(j)['tensao']) *
                        mt.sin(np.angle(self.__ybus[i-1][j-1]) 
                            - self.__dados.get(i)['ang'] 
                            + self.__dados.get(j)['ang'])
                    )
            if self.__dados[i]['code'] == 1:
                self.__Sbarras = {'P' : np.real(sum(soma1)), 'Q' : np.imag(sum(soma1))}
            elif self.__dados[i]['code'] == 3:
                self.__Sbarras = {'P' : 0, 'Q' : np.imag(sum(soma2))}
        
        for i in self.__dados:
            if self.__dados[i]['code'] == 1:
                self.__dados[i]['geracao'] = self.__Sbarras.get(i)['P'] + self.__Sbarras.get(i)['Q'] * 1j
            elif self.__dados[i]['code'] == 3:
                self.__dados[i]['geracao'] = np.real(self.__dados.get(i)['geracao']) + self.__Sbarras.get(i)['Q'] * 1j