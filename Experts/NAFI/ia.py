from core.ambiente import Ambiente
from core.neuronio import Perceptron
import random
import sys, math
import numpy as np
try:
    import _pickle as pickle
except ImportError:
    import cPickle as pickle
# Para ser reproduzivel...
np.random.seed(0)

class Agente(object):

    def f(self, receptores, total_passos, total_resets, bancarrota):

        while True:
            # [PERCEPTRON] Vamos apendar os receptores 
            dendritos.append(np.array(receptores))

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
                file = open("./core/receptores.pkl","wb")
                pickle.dump(receptores,file)
                file.close()
                #print('==================================================')
                #print('====================DEBUG=========================')
                #print('==============CALIBRAGEM DOS W\'s=================')
                #print('==================================================')
                #print(w)
                #print('==================================================')
                break

        return recompensa_total

    def carregar_memoria(self):
        # Carregando a memória
        try:
            file = open("./core/receptores.pkl",'rb')
            receptores = pickle.load(file)
            file.close()
        except FileNotFoundError:
            # Caso não exista, cria a memória com o epsilon da máquina
            # TODO: Implementar > https://stats.stackexchange.com/questions/347106/what-is-epsilon-k-in-epsilon-greedy-algorithm
            file = open("./core/receptores.pkl","wb")
            receptores = epsilon
            pickle.dump(receptores,file)
            file.close()

        return receptores

if __name__ == "__main__":

    # Instanciar as classes
    agente = Agente()
    ambiente = Ambiente()
        
    # Definindo o epsilon com o epsilon da máquina
    epsilon = sys.float_info.epsilon

    # Carregar a memória
    receptores = agente.carregar_memoria()

    # Definindo as variáveis do algoritmo
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
    # Being adapted from https://openai.com/blog/evolution-strategies/
    # With hyperparameters from http://www.jmlr.org/papers/volume15/wierstra14a/wierstra14a.pdf

    mu = 13 # Número de População/Tickers <NOTE: Talvez venha a trocar por lambda. Estou analisando>
    sigma = 0.1 # Ruído gaussiano
    eta = 0.01 # Taxa de aprendizagem
    # TODO: definir o rho

    # gerar dois arrays para comparação
    N = np.random.randn(mu, 13) # samples from a normal distribution N(0,1)
    R = np.zeros(mu) # Recompensas de cada receptor

    # Iniciar o Loop
    for receptor in range(mu):
        impulso = receptores + sigma*N[receptor] # jitter receptores using gaussian of sigma 0.1
        R[receptor] = agente.f(impulso, total_passos, total_resets, bancarrota) # evaluate the jittered version

    # standardize the rewards to have a gaussian distribution
    A = (R - np.mean(R)) / np.std(R)
    # perform the parameter update. The matrix multiply below
    # is just an efficient way to sum up all the rows of the noise matrix N,
    # where each row N[receptor] is weighted by A[receptor]
    receptores = receptores + eta/(mu*sigma) * np.dot(N.T, A)

    # TODO: Fazer um for loop em cada iteração para definirmos que o 1 é bom e o 0 é a Bancarrota
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
    #inp = np.asarray([impulso])

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
