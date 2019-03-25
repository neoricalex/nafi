import torch, zmq, random
from random import randrange
from torch.autograd import Variable
from core.funcoes import *

class Ambiente:  

    def __init__(self):

        self.recompensas = 0.00 # Saldo do Agente
        self.opcoes = [] # Opções do Agente
        self.carteira = [] # Portfólio
        self.ticker = 'N/A'
        self.volume = 0.00
        
        # necessário para quem não tem GPU
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

        self.tickers = ['EURUSD', 'GBPUSD', 'USDCHF', 'USDJPY', 'USDCAD', 'AUDUSD',
                        'EURCHF', 'EURJPY', 'EURGBP', 'EURCAD', 'GBPCHF', 'GBPJPY', 
                        'AUDJPY', 'GOLD', 'SILVER']

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
        # Abrir Posição TODO: Tratar os fafos do retorno
        self.observacao_abrir_posicao = abrir_posicao(self.ticker, self.volume)
    

    def acoes(self):
        self.abrir_posicao = self.opcoes.append('abrir_posicao')
        self.fechar_posicao = self.opcoes.append('fechar_posicao')
        self.selecionar_ticker = self.opcoes.append('selecionar_ticker')
        self.selecionar_volume = self.opcoes.append('selecionar_volume')

        return self.opcoes

    def acao(self, acao):

        if acao == 'fechar_posicao':

            if not self.carteira:
                print('Sem posições para fechar')
                self.recompensas -= 2
            else:
                print('Existem posições para fechar')
                self.recompensas += 1               

        elif acao == 'abrir_posicao':

            print('Abrindo posição...')
            if self.ticker == 'N/A':
                self.recompensas -= 2

            else:
                print('Abrindo posição com o ticker', self.ticker, '...')
                if self.volume == 0.0:
                    print('Sem Volume')
                    self.recompensas -= 2
                else:
                    print('Abrindo posição com o ticker', self.ticker, 'com o volume de', self.volume, '...')
                    self.recompensas += 1

        elif acao == 'selecionar_ticker':
            self.ticker = self.ticker_selecionado
            self.recompensas += 1

        elif acao == 'selecionar_volume':
            self.volume = 0.01  # TODO: Mais IA por aqui ...
            self.recompensas += 1

        else:
            print('Bug detetado!')

        return self.acao, self.recompensas

    def concluido(self):
        if self.recompensas == 10.00:
            self.reset()
            return True
        else:
            return False

    def reset(self):
        self.recompensas = 0.00 # Saldo do Agente
        self.opcoes = [] # Opções do Agente
        self.carteira = [] # Portfólio
        self.ticker = 'N/A'
        self.volume = 0.00