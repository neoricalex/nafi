import torch, zmq, random
import random
from random import randrange
from torch.autograd import Variable
from core.funcoes import *
import numpy as np

class Ambiente():  

    def __init__(self):

        self.estado_atual = 0
        self.recompensas = 0.00 # Saldo do Agente
        self.carteira = [] # Portfólio
        self.ticker = 'N/A' # Ticker da posição
        self.ticker_bom = [] # Ticker que ja ganhou
        self.volume = 0.00 # Volume da posição
        self.preco = 0.00 # Preço da posição
        
        # necessário para quem não tem GPU
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

        self.tickers = ['EURUSD', 'GBPUSD', 'USDCHF', 'USDJPY', 'USDCAD', 'AUDUSD',
                        'EURCHF', 'EURJPY', 'EURGBP', 'EURCAD', 'GBPCHF', 'GBPJPY', 
                        'AUDJPY']

        self.tickers_index = randrange(len(self.tickers))
        self.ticker_selecionado = self.tickers[self.tickers_index]

        self.observacao = torch.FloatTensor(torch.zeros(10,10)).to(self.device)
        # Cotações ticker
        self.observacao[0] = self.tickers_index
        self.observacao[0][1] = float(infos_ticker(self.ticker_selecionado)[0]) # Bid
        self.observacao[0][2] = float(infos_ticker(self.ticker_selecionado)[1]) # Ask
        self.observacao[0][3] = float(infos_ticker(self.ticker_selecionado)[2]) # Buy Volume
        self.observacao[0][4] = float(infos_ticker(self.ticker_selecionado)[3]) # Sell Volume
        self.observacao[0][5] = float(infos_ticker(self.ticker_selecionado)[4]) # Tick Volume
        self.observacao[0][6] = float(infos_ticker(self.ticker_selecionado)[5]) # Real Volume
        self.observacao[0][7] = float(infos_ticker(self.ticker_selecionado)[6]) # Buy Volume Market
        self.observacao[0][8] = float(infos_ticker(self.ticker_selecionado)[7]) # Sell Volume Market
        self.observacao[0][9] = int(infos_ticker(self.ticker_selecionado)[8])   # Data
        # Histórico do ticker; TODO: Deve ter mais histórico
        self.observacao_historico = historico_ticker(self.ticker_selecionado, escolher_numero_velas())
        self.observacao[1][0] = float(self.observacao_historico[0]) # Open
        self.observacao[1][1] = float(self.observacao_historico[1]) # High
        self.observacao[1][2] = float(self.observacao_historico[2]) # Low
        self.observacao[1][3] = float(self.observacao_historico[3]) # Close
        self.observacao[1][4] = int(self.observacao_historico[4]) # Data
        # Infos da conta na corretora
        self.observacao_conta = infos_conta()
        self.observacao[2][0] = float(self.observacao_conta[0]) # Saldo
        self.observacao[2][1] = float(self.observacao_conta[1]) # Crédito
        self.observacao[2][2] = float(self.observacao_conta[2]) # Lucro
        self.observacao[2][3] = float(self.observacao_conta[3]) # Equity
        self.observacao[2][4] = float(self.observacao_conta[4]) # Margem
        self.observacao[2][5] = float(self.observacao_conta[5]) # Margem Livre
        self.observacao[2][6] = float(self.observacao_conta[6]) # Margem Level
        self.observacao[2][7] = float(self.observacao_conta[7]) # Margem socall
        self.observacao[2][8] = float(self.observacao_conta[8]) # Margem soso
        self.observacao[2][9] = int(self.observacao_conta[9]) # data
        # Abrir Posição TODO: Tratar os dados do retorno
        self.observacao_abrir_posicao = abrir_posicao(self.ticker, self.volume)
    

    def acoes(self):
        self.opcoes = [] # Opções do Agente
        self.abrir_posicao = self.opcoes.append('abrir_posicao')
        self.fechar_posicao = self.opcoes.append('fechar_posicao')
        self.selecionar_ticker = self.opcoes.append('selecionar_ticker')
        self.selecionar_melhor_ticker = self.opcoes.append('selecionar_melhor_ticker')
        self.selecionar_volume = self.opcoes.append('selecionar_volume')
        self.selecionar_preco = self.opcoes.append('selecionar_preco')

        return self.opcoes

    def estados(self, acao):
        if acao == 'fechar_posicao':

            if not self.carteira:
                #print('Sem posições para fechar')
                self.recompensas -= 2
            else:
                #print('Existem posições para fechar')
                self.recompensas += 1               

        elif acao == 'abrir_posicao':

            #print('Abrindo posição...')
            if self.ticker == 'N/A':
                self.recompensas -= 2

            elif self.volume == 0.0:
                self.recompensas -= 2

            elif self.preco == 0.0:
                self.recompensas -= 2
            else:
                # Checkando se o agente tem saldo
                self.preco_total_operacao = self.preco * self.volume
                if self.preco_total_operacao > self.recompensas:
                    self.recompensas -= 2
                else:
                    # Checkando se o investimento não é mais de 1,5% do saldo
                    self.investimento = self.recompensas * 0.015
                    if self.preco_total_operacao > self.investimento:
                        self.recompensas -= 2
                    else:
                        print('OPEN', self.ticker, 'VOLUME:',self.volume, 'PREÇO',  self.preco)
                        self.ticker_bom.append(self.ticker)
                        self.recompensas += 1


        elif acao == 'selecionar_ticker':
            self.ticker = self.ticker_selecionado
            self.recompensas += 1

        elif acao == 'selecionar_melhor_ticker':
            if not self.ticker_bom:
                self.recompensas -= 2
            else:
                self.ticker = randrange(len(self.ticker_bom))
                self.recompensas += 2

        elif acao == 'selecionar_volume':
            # TODO: Implementar > https://scikit-learn.org/stable/auto_examples/linear_model/plot_lasso_and_elasticnet.html#sphx-glr-auto-examples-linear-model-plot-lasso-and-elasticnet-py
            self.volume = round(random.random(), 2)
            self.recompensas += 1

        elif acao == 'selecionar_preco':
            self.preco = self.observacao[0][2].item() # TODO: 
            self.recompensas += 1

        else:
            print('[DEBUG]: Opção não existente na acao:', acao)

        return self.acao, self.recompensas

    def acao(self, acao):
        self.estado_atual = self.estados(acao)

        return self.acao, self.recompensas

    def concluido(self):
        if self.recompensas >= 1000.00:
            return True
        else:
            return False

    def reset(self):
        self.estado_atual = self.acao
        self.recompensas = 0.00 # Saldo do Agente
        self.carteira = [] # Portfólio
        self.ticker = 'N/A' # Ticker da posição
        self.ticker_bom = [] # Ticker que ja ganhou
        self.volume = 0.00 # Volume da posição
        self.preco = 0.00 # Preço da posição

        return random.random()