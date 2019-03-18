import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import time
sns.set()

import pandas as pd
#google = pd.read_csv('./dados/GOOG.csv')
#google.head()

def get_state(data, t, n):
    d = t - n + 1
    block = data[d : t + 1] if d >= 0 else -d * [data[0]] + data[: t + 1]
    res = []
    for i in range(n - 1):
        res.append(block[i + 1] - block[i])
    return np.array([res])



class Deep_Evolution_Strategy:
    def __init__(
        self, neuronios, recompensa_function, populacao_size, sigma, learning_rate
    ):
        self.neuronios = neuronios
        self.recompensa_function = recompensa_function
        self.populacao_size = populacao_size
        self.sigma = sigma
        self.learning_rate = learning_rate

    def _get_neuronio_from_populacao(self, neuronios, populacao):
        neuronios_populacao = []
        for index, i in enumerate(populacao):
            jittered = self.sigma * i
            neuronios_populacao.append(neuronios[index] + jittered)
        return neuronios_populacao

    def get_neuronios(self):
        return self.neuronios

    def train(self, epoch = 100, printar_cada = 1):
        lasttime = time.time()
        for i in range(epoch):
            populacao = []
            recompensas = np.zeros(self.populacao_size)
            for k in range(self.populacao_size):
                x = []
                for w in self.neuronios:
                    x.append(np.random.randn(*w.shape))
                populacao.append(x)
            for k in range(self.populacao_size):
                neuronios_populacao = self._get_neuronio_from_populacao(
                    self.neuronios, populacao[k]
                )
                recompensas[k] = self.recompensa_function(neuronios_populacao)
            recompensas = (recompensas - np.mean(recompensas)) / np.std(recompensas)
            for index, w in enumerate(self.neuronios):
                A = np.array([p[index] for p in populacao])
                self.neuronios[index] = (
                    w
                    + self.learning_rate
                    / (self.populacao_size * self.sigma)
                    * np.dot(A.T, recompensas).T
                )
            if (i + 1) % printar_cada== 0:
                recompensas = self.recompensa_function(self.neuronios)
                #print(
                #    'iteração %d. recompensa: %f'
                #    % (i + 1, recompensas)
                #)
        print('[Treinamento] ROI:', recompensas, 'em', time.time() - lasttime, 'segundos')

        return recompensas


class Modelo:
    def __init__(self, dendritos, axonios, sinapses):
        self.neuronios = [
            np.random.randn(dendritos, axonios),
            np.random.randn(axonios, sinapses),
            np.random.randn(axonios, 1),
            np.random.randn(1, axonios),
        ]

    def predict(self, dendrito):
        feed = np.dot(dendrito, self.neuronios[0]) + self.neuronios[-1]
        decision = np.dot(feed, self.neuronios[1])
        buy = np.dot(feed, self.neuronios[2])
        return decision, buy

    def get_neuronios(self):
        return self.neuronios

    def ligar_neuronios(self, neuronios):
        self.neuronios = neuronios


class Agente:

    populacao_SIZE = 15
    SIGMA = 0.1
    LEARNING_RATE = 0.03

    def __init__(
        self, modelo, money, max_buy, max_sell, close, window_size, skip
    ):
        self.window_size = window_size
        self.skip = skip
        self.close = close
        self.modelo = modelo
        self.initial_money = money
        self.max_buy = max_buy
        self.max_sell = max_sell
        self.es = Deep_Evolution_Strategy(
            self.modelo.get_neuronios(),
            self.get_recompensa,
            self.populacao_SIZE,
            self.SIGMA,
            self.LEARNING_RATE,
        )

    def act(self, sequence):
        decision, buy = self.modelo.predict(np.array(sequence))
        return np.argmax(decision[0]), int(buy[0])

    def get_recompensa(self, neuronios):
        initial_money = self.initial_money
        starting_money = initial_money
        len_close = len(self.close) - 1

        self.modelo.neuronios = neuronios
        state = get_state(self.close, 0, self.window_size + 1)
        inventory = []
        quantity = 0
        for t in range(0, len_close, self.skip):
            action, buy = self.act(state)
            next_state = get_state(self.close, t + 1, self.window_size + 1)
            if action == 1 and initial_money >= self.close[t]:
                if buy < 0:
                    buy = 1
                if buy > self.max_buy:
                    buy_units = self.max_buy
                else:
                    buy_units = buy
                total_buy = buy_units * self.close[t]
                initial_money -= total_buy
                inventory.append(total_buy)
                quantity += buy_units
            elif action == 2 and len(inventory) > 0:
                if quantity > self.max_sell:
                    sell_units = self.max_sell
                else:
                    sell_units = quantity
                quantity -= sell_units
                total_sell = sell_units * self.close[t]
                initial_money += total_sell

            state = next_state
        return ((initial_money - starting_money) / starting_money) * 100

    def fit(self, iterations, checkagem):
        recompensas = self.es.train(iterations, printar_cada = checkagem)

        return recompensas

    def buy(self):
        initial_money = self.initial_money
        len_close = len(self.close) - 1
        state = get_state(self.close, 0, self.window_size + 1)
        starting_money = initial_money
        states_sell = []
        states_buy = []
        inventory = []
        quantity = 0
        for t in range(0, len_close, self.skip):
            action, buy = self.act(state)
            next_state = get_state(self.close, t + 1, self.window_size + 1)
            if action == 1 and initial_money >= self.close[t]:
                if buy < 0:
                    buy = 1
                if buy > self.max_buy:
                    buy_units = self.max_buy
                else:
                    buy_units = buy
                total_buy = buy_units * self.close[t]
                initial_money -= total_buy
                inventory.append(total_buy)
                quantity += buy_units
                states_buy.append(t)
                print(
                    'day %d: buy %d units at price %f, total balance %f'
                    % (t, buy_units, total_buy, initial_money)
                )
            elif action == 2 and len(inventory) > 0:
                bought_price = inventory.pop(0)
                if quantity > self.max_sell:
                    sell_units = self.max_sell
                else:
                    sell_units = quantity
                if sell_units < 1:
                    continue
                quantity -= sell_units
                total_sell = sell_units * self.close[t]
                initial_money += total_sell
                states_sell.append(t)
                try:
                    invest = ((total_sell - bought_price) / bought_price) * 100
                except:
                    invest = 0
                print(
                    'day %d, sell %d units at price %f, investment %f %%, total balance %f,'
                    % (t, sell_units, total_sell, invest, initial_money)
                )
            state = next_state

        invest = ((initial_money - starting_money) / starting_money) * 100
        print(
            '\ntotal gained %f, total investment %f %%'
            % (initial_money - starting_money, invest)
        )
        plt.figure(figsize = (20, 10))
        plt.plot(close, label = 'true close', c = 'g')
        plt.plot(
            close, 'X', label = 'predict buy', markevery = states_buy, c = 'b'
        )
        plt.plot(
            close, 'o', label = 'predict sell', markevery = states_sell, c = 'r'
        )
        plt.legend()
        plt.show()
