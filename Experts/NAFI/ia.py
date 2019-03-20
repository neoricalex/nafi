<<<<<<< HEAD
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import time, csv, os, random
from conexao import *
try:
    import _pickle as pickle
except ImportError:
    import cPickle as pickle


def get_state(data, t, n):
    d = t - n + 1
    block = data[d : t + 1] if d >= 0 else -d * [data[0]] + data[: t + 1]
    res = []
    for i in range(n - 1):
        res.append(block[i + 1] - block[i])
    return np.array([res])

def ticker():
  tickers = ['EURUSD', 'GBPUSD', 'USDCHF', 'USDJPY', 'USDCAD', 'AUDUSD',
              'EURCHF', 'EURJPY', 'EURGBP', 'EURCAD', 'GBPCHF', 'GBPJPY', 
              'AUDJPY', 'GOLD', 'SILVER', 'XAUUSD', 'XAGUSD']
  #ticker = random.choice(tickers)
  ticker = 'EURUSD'

  return ticker

def alvo(ticker):
  alvo = remote_send(reqSocket, 'INFO_TICKER|' + ticker )
  alvo = alvo.split(',')
  alvo = alvo[1]
 
  header_csv = ['cotacao']
  body_csv = [alvo]

  # Verificando se o csv já existe
  if os.path.exists('./dados/cotacao_{}.csv'.format(ticker)):
      # Se existir apenda
      with open('./dados/cotacao_{}.csv'.format(ticker), 'a', newline='\n') as csvfile:
          writer = csv.writer(csvfile, delimiter=',')
          writer.writerow(body_csv)        
          csvfile.close()
  else:
      # Se não existir cria
      with open('./dados/cotacao_{}.csv'.format(ticker), 'w', newline='') as csvfile:
          writer = csv.writer(csvfile, delimiter=',')
          writer.writerow(header_csv)
          writer.writerow(body_csv)
          csvfile.close()

  alvo = pd.read_csv('./dados/cotacao_{}.csv'.format(ticker))
  alvo = alvo.cotacao.values.tolist()
  
  return alvo

close = alvo(ticker())

class Model:
    def __init__(self, input_size, layer_size, output_size):
        self.weights = [
            np.random.randn(input_size, layer_size),
            np.random.randn(layer_size, output_size),
            np.random.randn(layer_size, 1),
            np.random.randn(1, layer_size),
        ]

    def predict(self, inputs):
        feed = np.dot(inputs, self.weights[0]) + self.weights[-1]
        decision = np.dot(feed, self.weights[1])
        buy = np.dot(feed, self.weights[2])
        return decision, buy

    def get_weights(self):
        return self.weights

    def set_weights(self, weights):
        self.weights = weights

    def save(self, filename='./dados/neuronios.pkl'):
        with open(filename, 'wb') as fp:
            pickle.dump(self.weights, fp)

    def load(self, filename='./dados/neuronios.pkl'):
        with open(filename, 'rb') as fp:
            self.weights = pickle.load(fp)

class Agent:

    POPULATION_SIZE = 50
    SIGMA = 0.1
    LEARNING_RATE = 0.001

    def __init__(
        self, model, money, max_buy, max_sell, close, window_size, skip
    ):
        self.window_size = window_size
        self.skip = skip
        self.close = close
        self.model = model
        self.initial_money = money
        self.max_buy = max_buy
        self.max_sell = max_sell
        self.es = Deep_Evolution_Strategy(
            self.model.get_weights(),
            self.get_reward,
            self.POPULATION_SIZE,
            self.SIGMA,
            self.LEARNING_RATE,
        )

    def act(self, sequence):
        decision, buy = self.model.predict(np.array(sequence))
        return np.argmax(decision[0]), int(buy[0])

    def get_reward(self, weights):
        initial_money = self.initial_money
        starting_money = initial_money
        len_close = len(self.close) - 1

        self.model.weights = weights
        state = get_state(self.close, 0, self.window_size + 1)
        inventory = []
        quantity = 0
        for t in range(0, len_close, self.skip):
            action, buy = self.act(state)
            next_state = get_state(self.close, t + 1, self.window_size + 1)
            if action == 1 and initial_money >= self.close[t] and quantity > 0:
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

    def fit(self, iterations, checkpoint):
        self.es.train(iterations, print_every = checkpoint)

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
                #print(
                #    'day %d: buy %d units at price %f, total balance %f'
                #    % (t, buy_units, total_buy, initial_money)
                #)
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
                #print(
                #    'day %d, sell %d units at price %f, investment %f %%, total balance %f,'
                #    % (t, sell_units, total_sell, invest, initial_money)
                #)
            state = next_state

        invest = ((initial_money - starting_money) / starting_money) * 100
        print(
            '\n[Lucro/Prejuizo] %f [ROI] %f %%'
            % (initial_money - starting_money, invest)
        )
        #plt.figure(figsize = (20, 10))
        #plt.plot(close, label = 'true close', c = 'g')
        #plt.plot(
        #    close, 'X', label = 'predict buy', markevery = states_buy, c = 'b'
        #)
        #plt.plot(
        #    close, 'o', label = 'predict sell', markevery = states_sell, c = 'r'
        #)
        #plt.legend()
        #plt.show()

class Deep_Evolution_Strategy:
    def __init__(
        self, weights, reward_function, population_size, sigma, learning_rate
    ):
        self.weights = weights
        self.reward_function = reward_function
        self.population_size = population_size
        self.sigma = sigma
        self.learning_rate = learning_rate

    def _get_population(self):
        population = []
        for k in range(self.population_size):
            x = []
            for w in self.weights:
                x.append(np.random.randn(*w.shape))
            population.append(x)

        return population

    def _get_weight_from_population(self, weights, population):
        weights_population = []
        for index, i in enumerate(population):
            jittered = self.sigma * i
            weights_population.append(weights[index] + jittered)

        return weights_population

    def get_weights(self):
        return self.weights

    def train(self, epoch = 128, print_every = 1):
        try:
          model.load()
        except FileNotFoundError:
          pass

        model.get_weights()
        model.set_weights(self.weights)
        lasttime = time.time()
        for i in range(epoch):
            population = self._get_population()
            rewards = np.zeros(self.population_size)
            for k in range(self.population_size):
                weights_population = self._get_weight_from_population(
                    self.weights, population[k]
                )
                rewards[k] = self.reward_function(weights_population)
            rewards = (rewards - np.mean(rewards)) / np.std(rewards)
            for index, w in enumerate(self.weights):
                A = np.array([p[index] for p in population])
                self.weights[index] = (
                    w
                    + self.learning_rate
                    / (self.population_size * self.sigma)
                    * np.dot(A.T, rewards).T
                )
            if (i + 1) % print_every == 0:
                print(
                    'Ao final de %d iterações a recompensa é de %f'
                    % (i + 1, self.reward_function(self.weights))
                )
                
        print('Treinamento efetuado em', time.time() - lasttime, 'segundos')

        model.save()

window_size = 24
layer_size = 8192
output_size = 3
max_buy = 5
max_sell = 5
money = 1000
skip = 1
iterations = 100
checkpoint = 10

model = Model(input_size = window_size, 
              layer_size = layer_size, 
              output_size = output_size)
agent = Agent(
    model = model,
    money = money,
    max_buy = max_buy,
    max_sell = max_sell,
    close = close,
    window_size = window_size,
    skip = skip)
agent.fit(iterations = iterations, checkpoint = checkpoint)
agent.buy()
=======
import time
from core.envs.griduniverse_env import GridUniverseEnv


def run_griduniverse_from_text_file():
    """
    Run a random agent on an environment that was save via ascii text file.
    Check core/envs/maze_text_files for examples or the _create_custom_world_from_text() function within the environment
    """
    print('\n' + '*' * 20 + 'Creating a pre-made GridUniverse from text file and running random agent on it' + '*' * 20 + '\n')
    env = GridUniverseEnv(custom_world_fp='./core/envs/maze_text_files/mundo.txt')
    for i_episode in range(1):
        observation = env._reset()
        for t in range(10000):
            env._render(mode='graphic')
            action = env.action_space.sample()
            #print('go ' + env.action_descriptors[action])
            #time.sleep(1.5) # uncomment to watch slower
            observation, reward, done, info = env._step(action)
            if done:
                print("Episode finished after {} timesteps".format(t + 1))
                break


if __name__ == '__main__':
    # Run random agent on environment variations
    run_griduniverse_from_text_file()

>>>>>>> d2c44fb939895a2bc23de6fe512d2c7b2d30edd7
