
from core.ambiente import Ambiente
from core.neuronio import Perceptron
import random
import sys
import numpy as np
try:
    import _pickle as pickle
except ImportError:
    import cPickle as pickle
# Para ser reproduzivel...
np.random.seed(0)

class Agente(object):

    def f(self, w, total_passos, total_resets, bancarrota):

        while True:
            # [PERCEPTRON] Vamos apendar os w's 
            dendritos.append(np.array(w))

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
                filehandler = open("./core/dablios.pkl","wb")
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
        file = open("./core/dablios.pkl",'rb')
        w = pickle.load(file)
        file.close()
    except FileNotFoundError:
        # Caso não exista, cria a memória com o epsilon da máquina
        # TODO: Implementar > https://stats.stackexchange.com/questions/347106/what-is-epsilon-k-in-epsilon-greedy-algorithm
        filehandler = open("./core/dablios.pkl","wb")
        w = epsilon
        pickle.dump(w,filehandler)
        filehandler.close()

    # Definindo as variáveis do algoritmo
    agente = Agente()
    ambiente = Ambiente()
    recompensa_total = 0
    total_passos = 0
    total_resets = 0
    acoes = ambiente.acoes()
    estado_inicial = random.choice(acoes)  # TODO: Melhorar a randomização inicial
    proximo_estado = estado_atual = estado_inicial
    acao = estado_atual
    recompensa = recompensa_total
    bancarrota = False
    # Fazer o neurónio(Perceptron) na unha. Mais infos: https://pt.wikipedia.org/wiki/Perceptron
    # Adapted from https://medium.com/@thomascountz/19-line-line-by-line-python-perceptron-b6f113b161f3
    dendritos = []

    # Adicionando a matemática
    # Adapted from https://openai.com/blog/evolution-strategies/
    # hyperparameters
    npop = 13 # population size
    sigma = 0.1 # noise standard deviation
    alpha = 0.001 # learning rate

    # gerar dois arrays para comparação
    N = np.random.randn(npop, 13) # samples from a normal distribution N(0,1)
    R = np.zeros(npop) # Recompensas de cada w

    # Iniciar o Loop
    for j in range(npop):
        w_try = w + sigma*N[j] # jitter w using gaussian of sigma 0.1
        R[j] = agente.f(w_try, total_passos, total_resets, bancarrota) # evaluate the jittered version

    # standardize the rewards to have a gaussian distribution
    A = (R - np.mean(R)) / np.std(R)
    # perform the parameter update. The matrix multiply below
    # is just an efficient way to sum up all the rows of the noise matrix N,
    # where each row N[j] is weighted by A[j]
    w = w + alpha/(npop*sigma) * np.dot(N.T, A)
    print(dendritos)
    exit()
    # TODO: Fazer um for loop em cada iteração para definirmos que o 1 Lucrou é bom e o 0 é a Bancarrota
    #labels = np.array([1, 0, 0, 0])

    # TODO: depois e tambem a cada iteração vamos criar um neurónio para treinar ele
    #perceptron = Perceptron(total_passos)
    #perceptron.train(dendritos, labels)

    #inputs = np.array([1, 1])
    #print('Teste:', perceptron.predict(inputs) )
    #=> 1

    #inputs = np.array([0, 1])
    #print('Teste:', perceptron.predict(inputs) ) 
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

    # Iniciando a rede neural
    # Adapted from https://github.com/alirezamika/evostra
    #model = FeedForwardNetwork(layer_sizes=[5, 4, 4, 50])

    # A solução é os w's que estamos otimizando
    #solution = np.array(w)
 
    # Os inputs é os w's alterados com o sigma
    #inp = np.asarray([w_try])

    # A diferença dos dois ou será a função LOSS ou o valor Otimizado do Sigma. TODO: Pensar e analizar melhor
    #def get_reward(weights):
    #    global solution, model, inp
    #    model.set_weights(weights)
    #    prediction = model.predict(inp)
    #    # here our best reward is zero
    #    reward = -np.sum(np.square(solution - prediction))
    #    return reward

    #es = EvolutionStrategy(model.get_weights(), get_reward, population_size=20, sigma=0.1, learning_rate=0.03, decay=0.995, num_threads=1)
    #es.run(1000, print_step=100)
