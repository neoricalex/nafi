import gym, torch, zmq, random
from gym import error, spaces, utils
from gym.utils import seeding
from neoricalex.funcoes import *
from random import randrange
from torch.autograd import Variable

class Ambiente(gym.Env):  

    def __init__(self):

        # necessário para gym
        metadata = {'render.modes': ['human']}
        # necessário para quem não tem GPU
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

        self.tickers = ['EURUSD', 'GBPUSD', 'USDCHF', 'USDJPY', 'USDCAD', 'AUDUSD',
                        'EURCHF', 'EURJPY', 'EURGBP', 'EURCAD', 'GBPCHF', 'GBPJPY', 
                        'AUDJPY', 'GOLD', 'SILVER']

        self.tickers_index = randrange(len(self.tickers))
        self.ticker = self.tickers[self.tickers_index]

    def observacao(self):
        self.observacao = torch.FloatTensor(torch.zeros(10,10)).to(self.device)
        # Escolher ticker
        self.observacao[0] = self.tickers_index
        self.observacao[0][1] = float(infos_ticker(self.ticker)[0]) # Bid
        self.observacao[0][2] = float(infos_ticker(self.ticker)[1]) # Ask
        self.observacao[0][3] = float(infos_ticker(self.ticker)[2]) # Buy Volume
        self.observacao[0][4] = float(infos_ticker(self.ticker)[3]) # Sell Volume
        self.observacao[0][5] = float(infos_ticker(self.ticker)[4]) # Tick Volume
        self.observacao[0][6] = float(infos_ticker(self.ticker)[5]) # Real Volume
        self.observacao[0][7] = float(infos_ticker(self.ticker)[6]) # Buy Volume Market
        self.observacao[0][8] = float(infos_ticker(self.ticker)[7]) # Sell Volume Market
        self.observacao[0][9] = int(infos_ticker(self.ticker)[8])   # Data
        # Histórico do ticker; TODO: Deve ter mais histórico
        self.observacao_historico = historico_ticker(self.ticker, escolher_numero_velas())
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

        return self.observacao

    def estado(self, action):
        estado_inicial = action
        if isinstance(estado_inicial, int):
            estado_inicial = [estado_inicial]
        self.estados_iniciais = estado_inicial
        self.estado_anterior = self.estado_atual = self.estado_seguinte = self.estado_inicial = random.choice(self.estados_iniciais)
        self.estado_atual = self.observacao()

    def step(self, action):
        
        # Create a class that will be used to keep track of information about the transaction
        class Info(object):
            pass        
        info = Info()
        
        # Set the done flag to False. This indicates that we haven't sold all the shares yet.
        info.done = False
                
        # During training, if the DDPG fails to sell all the stocks before the given 
        # number of trades or if the total number shares remaining is less than 1, then stop transacting,
        # set the done Flag to True, return the current implementation shortfall, and give a negative reward.
        # The negative reward is given in the else statement below.
        if self.transacting and (self.timeHorizon == 0 or abs(self.shares_remaining) < self.tolerance):
            self.transacting = False
            info.done = True
            info.implementation_shortfall = self.total_shares * self.startingPrice - self.totalCapture
            info.expected_shortfall = self.get_expected_shortfall(self.total_shares)
            info.expected_variance = self.singleStepVariance * self.tau * self.totalSRSQ
            info.utility = info.expected_shortfall + self.llambda * info.expected_variance
            
        # We don't add noise before the first trade    
        if self.k == 0:
            info.price = self.prevImpactedPrice
        else:
            # Calculate the current stock price using arithmetic brownian motion
            info.price = self.prevImpactedPrice + np.sqrt(self.singleStepVariance * self.tau) * random.normalvariate(0, 1)
      
        # If we are transacting, the stock price is affected by the number of shares we sell. The price evolves 
        # according to the Almgren and Chriss price dynamics model. 
        if self.transacting:
            
            # If action is an ndarray then extract the number from the array
            if isinstance(action, np.ndarray):
                action = action.item()            

            # Convert the action to the number of shares to sell in the current step
            sharesToSellNow = self.shares_remaining * action
            # sharesToSellNow = min(self.shares_remaining * action, self.shares_remaining)
    
            if self.timeHorizon < 2:
                sharesToSellNow = self.shares_remaining

            # Since we are not selling fractions of shares, round up the total number of shares to sell to the nearest integer. 
            info.share_to_sell_now = np.around(sharesToSellNow)

            # Calculate the permanent and temporary impact on the stock price according the AC price dynamics model
            info.currentPermanentImpact = self.permanentImpact(info.share_to_sell_now)
            info.currentTemporaryImpact = self.temporaryImpact(info.share_to_sell_now)
                
            # Apply the temporary impact on the current stock price    
            info.exec_price = info.price - info.currentTemporaryImpact
            
            # Calculate the current total capture
            self.totalCapture += info.share_to_sell_now * info.exec_price

            # Calculate the log return for the current step and save it in the logReturn deque
            self.logReturns.append(np.log(info.price/self.prevPrice))
            self.logReturns.popleft()
            
            # Update the number of shares remaining
            self.shares_remaining -= info.share_to_sell_now
            
            # Calculate the runnig total of the squares of shares sold and shares remaining
            self.totalSSSQ += info.share_to_sell_now ** 2
            self.totalSRSQ += self.shares_remaining ** 2
                                        
            # Update the variables required for the next step
            self.timeHorizon -= 1
            self.prevPrice = info.price
            self.prevImpactedPrice = info.price - info.currentPermanentImpact
            
            # Calculate the reward
            currentUtility = self.compute_AC_utility(self.shares_remaining)
            reward = (abs(self.prevUtility) - abs(currentUtility)) / abs(self.prevUtility)
            self.prevUtility = currentUtility
            
            # If all the shares have been sold calculate E, V, and U, and give a positive reward.
            if self.shares_remaining <= 0:
                
                # Calculate the implementation shortfall
                info.implementation_shortfall  = self.total_shares * self.startingPrice - self.totalCapture
                   
                # Set the done flag to True. This indicates that we have sold all the shares
                info.done = True
        else:
            reward = 0.0
        
        self.k += 1
            
        # Set the new state
        state = np.array(list(self.logReturns) + [self.timeHorizon / self.num_n, self.shares_remaining / self.total_shares])

        return (state, np.array([reward]), info.done, info)



    def reset(self):
        pass
    def render(self, mode='human', close=False):
        pass
    
    def get_trade_list(self):
        # Calculate the trade list for the optimal strategy according to equation (18) of the AC paper
        trade_list = np.zeros(self.num_n)
        ftn = 2 * np.sinh(0.5 * self.kappa * self.tau)
        ftd = np.sinh(self.kappa * self.liquidation_time)
        ft = (ftn / ftd) * self.total_shares
        for i in range(1, self.num_n + 1):       
            st = np.cosh(self.kappa * (self.liquidation_time - (i - 0.5) * self.tau))
            trade_list[i - 1] = st
        trade_list *= ft
        return trade_list
