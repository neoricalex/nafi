from agente import *
from estrategia import *
from modelo import *
import numpy as np
from dados import *
import time

# Pegando dados
ticker = escolher_ticker()
print('Ticker:', ticker)
if os.path.exists('./dados/historico_{}.csv'.format(ticker)):
    infos_ticker(ticker)
else:
    popular_csv_infos_ticker(ticker, 1) # 1 dia no Timeframe H1
cotacoes_ticker = infos_ticker(ticker)
historico_ticker = pd.read_csv('./dados/historico_{}.csv'.format(ticker))

# Setando a entrada na DeepRN
impulsos = np.asarray(historico_ticker)
numero_impulsos = np.count_nonzero(impulsos)
dendritos = 30
axonios = numero_impulsos * dendritos
print('Número de Axónios:', axonios)
sinapses = 3

# Setando a Saida (Em testes)
solucao = np.array([cotacoes_ticker[0], cotacoes_ticker[1], cotacoes_ticker[8]])

# Setando o Modelo 
model = FeedForwardNetwork(layer_sizes=[numero_impulsos, dendritos, axonios, sinapses])

def criar_recompensa(agente):
    global solucao, model, impulsos
    model.set_weights(agente)
    prediction = model.predict(impulsos)

    initial_money = 10000
    starting_money = initial_money
    skip = 1
    max_buy = 5
    max_sell = 5
    close = historico_ticker.preco_compra.values.tolist()
 
    modelo = Modelo(dendritos = dendritos, axonios = axonios, sinapses = sinapses)             
    agente = Agente(
        modelo = modelo,
        money = starting_money,
        max_buy = max_buy,
        max_sell = max_sell,
        close = close,
        window_size = dendritos,
        skip = skip,
    )
    recompensa_agente = agente.fit(iterations = 1, checkagem = 1)

    return recompensa_agente
 
try:
    es = EvolutionStrategy(model.get_weights(), criar_recompensa, population_size=20, sigma=0.1, learning_rate=0.03, decay=0.995, num_threads=1)
    es.run(1, print_step=1)
    while True:
        print('O ticker', ticker, 'finalizou o treinamento com', axonios, 'axónios!')
        time.sleep(3600)
except:
    print('Reiniciando a IA ...')

#optimized_weights = es.get_weights()
#model.set_weights(optimized_weights)

#modelo = Modelo(window_size, 1000, 3)
#len_close = len(close) - 1
#neuronio = modelo
#state = get_state(close, 0, window_size + 1)
#inventory = []
#quantity = 0

#agent.buy()