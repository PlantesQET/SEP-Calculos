import cmath as cmt
import math as mt
import numpy as np
import matplotlib.pyplot as plt

class Newton:
    def __init__(self) -> None:
        print('Classe Newton Criada')
        self.__Sbase = 100e6
        self.__Sesp = dict()

        self.__dados = dict()
        self.__tensaoPlot = dict()
        self.__angPlot = dict()

        self.__Ligacoes = dict()
        self.__ybus = list()

        # Contadores de barras
        self.__nPQ = int()
        self.__nPV = int()

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

        self.__printYbus()

        for i in self.__dados:
            if self.__dados.get(i)['code'] == 2:
                self.__nPQ += 1
            elif self.__dados.get(i)['code'] == 3:
                self.__nPV += 1
            else:
                return 'Erro!'
    
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

