
from core.ambiente import Ambiente
from core.funcoes import pingar_mt5
import random
import sys
import numpy as np
try:
    import _pickle as pickle
except ImportError:
    import cPickle as pickle

np.random.seed(0)

def f(w):
    ambiente = Ambiente()
    recompensa_total = 0
    total_passos = 0
    total_resets = 0
    acoes = ambiente.acoes()
    estado_inicial = random.choice(acoes)  
    concluido = ambiente.concluido()
    proximo_estado = estado_atual = estado_inicial
    acao = estado_atual
    recompensa = recompensa_total
    concluido = ambiente.concluido()

    while True:
        concluido = ambiente.concluido()
        acao, recompensa = ambiente.acao(random.choice(acoes))
        recompensa_total = recompensa
        total_passos += 1

        if recompensa_total <= -100.00:             
            recompensa_total -= 1
            ambiente.reset()
            total_resets += 1

        if total_resets >= 10:
            print('[INFO] RESET [DEBUG] total_resets >= 10')
            ambiente.reset()
            concluido = True

        if concluido == True:
            filehandler = open("./core/w.pkl","wb")
            pickle.dump(w,filehandler)
            filehandler.close()

            break

    return recompensa_total

if __name__ == "__main__":
        
    # hyperparameters
    npop = 50 # population size
    sigma = 0.1 # noise standard deviation
    alpha = 0.001 # learning rate
    # Definindo o epsilon
    epsilon = sys.float_info.epsilon

    try:
        file = open("./core/w.pkl",'rb')
        w = pickle.load(file)
        file.close()
    except:
        filehandler = open("./core/w.pkl","wb")
        w = epsilon
        pickle.dump(w,filehandler)
        filehandler.close()

    N = np.random.randn(npop, 13) # samples from a normal distribution N(0,1)
    R = np.zeros(npop)
    for j in range(npop):
        w_try = w + sigma*N[j] # jitter w using gaussian of sigma 0.1
        R[j] = f(w_try) # evaluate the jittered version
        print('++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++', R[j])

    # standardize the rewards to have a gaussian distribution
    A = (R - np.mean(R)) / np.std(R)
    # perform the parameter update. The matrix multiply below
    # is just an efficient way to sum up all the rows of the noise matrix N,
    # where each row N[j] is weighted by A[j]
    w = w + alpha/(npop*sigma) * np.dot(N.T, A)
