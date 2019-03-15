import numpy as np
from evolution_strategy import *
from feed_forward_network import *
import random

# A feed forward neural network with input size of 5, two hidden layers of size 4 and output of size 3
model = FeedForwardNetwork(layer_sizes=[5, 4, 4, 3])

solution = np.int(100)
inp = np.asarray([1, 2, 3, 4, 5])

def get_reward(weights):
    global solution, model, inp
    model.set_weights(weights)
    prediction = model.predict(inp)
    # here our best reward is zero
    reward = -np.sum(np.square(solution - prediction))
    return reward

# if your task is computationally expensive, you can use num_threads > 1 to use multiple processes;
# if you set num_threads=-1, it will use number of cores available on the machine; Here we use 1 process as the
#  task is not computationally expensive and using more processes would decrease the performance due to the IPC overhead.
es = EvolutionStrategy(model.get_weights(), get_reward, population_size=20, sigma=0.1, learning_rate=0.03, decay=0.995, num_threads=1)
es.run(1000, print_step=100)

optimized_weights = es.get_weights()
print(optimized_weights)
#model.set_weights(optimized_weights)