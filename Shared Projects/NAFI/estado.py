from dados import *
import pandas as pd
import numpy as np
import time

# Agora vamos escolher um ticker para trabalharmos
ticker = escolher_ticker()
if os.path.exists('./dados/historico_{}.csv'.format(ticker)):
    infos_ticker(ticker)
else:
    popular_csv_infos_ticker(ticker, 24)

df = pd.read_csv('./dados/historico_{}.csv'.format(ticker))
# Agora vamos definir o nosso alvo
alvo = df.preco_compra.values.tolist()

# Agora vamos criar uma funcionalidade tecnica pra nossa IA. 
# Porém a partir daqui a minha "Expertise" acaba e irei apenas mencionar as fontes,
# assim como as formas de como eu as interpreto. Portanto a você de fazer sua pesquisa se encontrar
# alguma coisa errada em minha interpretação.
def estado_atual(dados, tecido_nervoso, numero_velas_que_queremos_prever):
    # A técnica que vamos usar peguei do huseinzol05[1], que por sua vez pegou do Karpathy[2], e que,
    # por sua vez, usou uma técnica académicamente descrita como NES - Natural Evolution Strategy[3], 
    # que ficou conhecida através da galera da OpenAI, em que venceram no Dota 2 em 1v1.

    # Aquilo que queremos definir aqui é: t = (t + 1) — t
    # Onde t é o numero de população(tecido_nervoso), o n o sigma (numero_velas_que_queremos_prever),
    # e os dados (preço_fechamento) o alpha
    # O alpha é adaptável, assim como o número de população e sigma (alpha / (npops * sigma))
    indice = tecido_nervoso - numero_velas_que_queremos_prever + 1
    bloco = dados[indice : tecido_nervoso + 1] if indice >= 0 else -indice * [dados[0]] + dados[: tecido_nervoso + 1]
    resultado_estado_atual = []
    for i in range(numero_velas_que_queremos_prever - 1):
        resultado_estado_atual.append(bloco[i + 1] - bloco[i])
    return np.array([resultado_estado_atual])