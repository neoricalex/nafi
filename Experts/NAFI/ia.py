
from core.ambiente import Ambiente
from core.neuronio import Perceptron
import random
import sys
import numpy as np
try:
    import _pickle as pickle
except ImportError:
    import cPickle as pickle

np.random.seed(0)

def f(w, total_passos, total_resets, bancarrota):

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
            #print('[INFO] RESET [DEBUG] total_resets >= 10')
            ambiente.reset()
            bancarrota = True
            concluido = True

        if concluido == True:
            if bancarrota:
                pass
            filehandler = open("./core/w.pkl","wb")
            pickle.dump(w,filehandler)
            filehandler.close()
            print('==================================================')
            print('====================DEBUG=========================')
            print('==============CALIBRAGEM DOS W\'s=================')
            print('==================================================')
            print(w)
            print('==================================================')
            break

    return recompensa_total

if __name__ == "__main__":
        
    # Definindo o epsilon da máquina
    epsilon = sys.float_info.epsilon

    # Carregando a memória
    try:
        file = open("./core/memoria.pkl",'rb')
        w = pickle.load(file)
        file.close()
    except FileNotFoundError:
        # Caso não exista, cria a memória com o epsilon da máquina
        # TODO: Implementar > https://stats.stackexchange.com/questions/347106/what-is-epsilon-k-in-epsilon-greedy-algorithm
        filehandler = open("./core/memoria.pkl","wb")
        w = epsilon
        pickle.dump(w,filehandler)
        filehandler.close()

    # Definindo as variáveis do algoritmo
    ambiente = Ambiente()
    recompensa_total = 0
    total_passos = 0
    total_resets = 0
    acoes = ambiente.acoes()
    estado_inicial = random.choice(acoes)  # TODO: Melhorar a randomização inicial
    proximo_estado = estado_atual = estado_inicial
    acao = estado_atual
    recompensa = recompensa_total
    concluido = ambiente.concluido()
    bancarrota = False

    # Adicionando a matemática
    # hyperparameters
    npop = 50 # population size
    sigma = 0.1 # noise standard deviation
    alpha = 0.001 # learning rate

    # gerar dois arrays para comparação
    N = np.random.randn(npop, 50) # samples from a normal distribution N(0,1)
    R = np.zeros(npop) # Recompensas de cada w

    # Iniciar o Loop
    for j in range(npop):
        w_try = w + sigma*N[j] # jitter w using gaussian of sigma 0.1
        R[j] = f(w_try, total_passos, total_resets, bancarrota) # evaluate the jittered version
        #print('++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++', R[j])

    # standardize the rewards to have a gaussian distribution
    A = (R - np.mean(R)) / np.std(R)
    # perform the parameter update. The matrix multiply below
    # is just an efficient way to sum up all the rows of the noise matrix N,
    # where each row N[j] is weighted by A[j]
    w = w + alpha/(npop*sigma) * np.dot(N.T, A)

    training_inputs = []
    training_inputs.append(np.array([1, 1]))
    training_inputs.append(np.array([1, 0]))
    training_inputs.append(np.array([0, 1]))
    training_inputs.append(np.array([0, 0]))

    labels = np.array([1, 0, 0, 0])

    perceptron = Perceptron(2)
    perceptron.train(training_inputs, labels)

    inputs = np.array([1, 1])
    print('Teste:', perceptron.predict(inputs) )
    #=> 1

    inputs = np.array([0, 1])
    print('Teste:', perceptron.predict(inputs) ) 
    #=> 0

# Fazer o dict
#        asg_resp = as_client.create_auto_scaling_group(
#            AutoScalingGroupName=exp_name,
#            LaunchConfigurationName=exp_name,
#            MinSize=cluster_size,
#            MaxSize=cluster_size,
#            DesiredCapacity=cluster_size,
#            AvailabilityZones=[zone],
#            Tags=[
#                dict(Key="Name", Value=exp_name + "-worker"),
#                dict(Key="es_dist_role", Value="worker"),
#                dict(Key="exp_prefix", Value=exp_prefix),
#                dict(Key="exp_name", Value=exp_name),
#            ]
#        )
