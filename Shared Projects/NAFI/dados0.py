from datetime import datetime, timedelta
from conexao import *
import os, csv

'''
    Primeiro temos de angariar os dados históricos para trabalharmos
'''
# Definindo as datas de inicio e fim: Ano, Mês, Dia, Hora, Segundo
inicio = datetime(2019, 1, 1, 0, 0)
fim = datetime(2019, 2, 28, 0, 0)
data_inicio = fim - inicio

# Definindo os tickers e TimeFrames
tickers = ['EURUSD', 'GBPUSD', 'USDCHF', 'USDJPY', 'USDCAD', 'AUDUSD', 'EURCHF', 'EURJPY', 'EURGBP', 'EURCAD', 'GBPCHF', 'GBPJPY', 'AUDJPY']
#timeframes = ['PERIOD_CURRENT' , 'PERIOD_M1' , 'PERIOD_M5' , 'PERIOD_M15' , 'PERIOD_M30' ,'PERIOD_H1' , 'PERIOD_H4' , 'PERIOD_D1' , 'PERIOD_W1' , 'PERIOD_MN1' , 'PERIOD_M2' , 'PERIOD_M3' , 'PERIOD_M4' , 'PERIOD_M6' , 'PERIOD_M10' , 'PERIOD_M12' , 'PERIOD_H1' , 'PERIOD_H2' , 'PERIOD_H3' , 'PERIOD_H4' , 'PERIOD_H6' , 'PERIOD_H8' , 'PERIOD_H12' , 'PERIOD_D1' , 'PERIOD_W1' , 'PERIOD_MN1']

# Para cada ticker ...
for ticker in tickers:
    # ... Para cada dia ...
    for i in range(data_inicio.days + 1):
            # ... Pede as cotações ...
            data_inicial = inicio + timedelta(i)
            data_inicial = 'D\'' + str(data_inicial)
            data_final = inicio + timedelta(i + 1)
            data_final = 'D\'' + str(data_final)
            cotacoes = remote_send(reqSocket, 'DATA|' + ticker + '|PERIOD_D1|' + data_inicial + '|' + data_final)
            cotacoes = cotacoes.split(',')
            tick_open = cotacoes[0]
            tick_high = cotacoes[1]
            tick_low = cotacoes[2]
            tick_close = cotacoes[3]
            data_header_csv = str(inicio + timedelta(i))
            #print(ticker, data_inicial, data_final, tick_open, tick_high, tick_low, tick_close)

            # ... E manda para um CSV

            # Definindo o header e body do CSV
            header_csv = ['Data', 'Open', 'High', 'Low', 'Close']
            body_csv = [data_header_csv, tick_open, tick_high, tick_low, tick_close]
            # Se o CSV existir appenda
            if os.path.exists('dados/cotacoes_historicas_{}.csv'.format(ticker)):
                with open('dados/cotacoes_historicas_{}.csv'.format(ticker), 'a', newline='\n') as csvfile:
                    writer = csv.writer(csvfile, delimiter=',')
                    writer.writerow(body_csv)        
                    csvfile.close()
            # Se não existir cria
            else:
                with open('dados/cotacoes_historicas_{}.csv'.format(ticker), 'w', newline='\n') as csvfile:
                    writer = csv.writer(csvfile, delimiter=',')
                    writer.writerow(header_csv)
                    writer.writerow(body_csv)
                    csvfile.close()


# Agora vamos selecionar um timeframe
def escolher_timeframe():
    timeframes = ['PERIOD_CURRENT' , 'PERIOD_M1' , 'PERIOD_M5' , 'PERIOD_M15' , 'PERIOD_M30' ,'PERIOD_H1' , 'PERIOD_H4' , 'PERIOD_D1' , 'PERIOD_W1' , 'PERIOD_MN1' , 'PERIOD_M2' , 'PERIOD_M3' , 'PERIOD_M4' , 'PERIOD_M6' , 'PERIOD_M10' , 'PERIOD_M12' , 'PERIOD_H1' , 'PERIOD_H2' , 'PERIOD_H3' , 'PERIOD_H4' , 'PERIOD_H6' , 'PERIOD_H8' , 'PERIOD_H12' , 'PERIOD_D1' , 'PERIOD_W1' , 'PERIOD_MN1']
    timeframe = random.choice(timeframes)

    return timeframe

# Depois vamos criar o nosso histórico
# pra saber a que preços abriram e fecharam as velas/barras anteriores
def preco_velas_anteriores(numero_velas):
    # Como o MT5 não sabe que o que queremos é o preço para cada vela,
    # e não o preço da vela em questão temos de iterar
    for i in range(1, numero_velas + 1):
        # OK, agora vamos pedir o preço para cada vela
        preco_velas = remote_send(reqSocket, 'HISTORICO|' + str(i))
        preco_velas = preco_velas.split(',')
        preco_abertura = preco_velas[0]
        preco_fechamento = preco_velas[1]
        data_vela = preco_velas[2]

        # depois vamos criar o header e o body do CSV
        header_csv = ['data', 'preco_abertura', 'preco_fechamento']
        body_csv = [data_vela, preco_abertura, preco_fechamento]

        # Verificando se o csv já existe
        if os.path.exists('./dados/historico_{}.csv'.format(numero_velas)):
            # Se existir apenda
            with open('./dados/historico_{}.csv'.format(numero_velas), 'a', newline='\n') as csvfile:
                writer = csv.writer(csvfile, delimiter=',')
                writer.writerow(body_csv)        
                csvfile.close()
        else:
            # Se não existir cria
            with open('./dados/historico_{}.csv'.format(numero_velas), 'w', newline='') as csvfile:
                writer = csv.writer(csvfile, delimiter=',')
                writer.writerow(header_csv)
                writer.writerow(body_csv)
                csvfile.close()
# Agora que temos o nosso historico preparado temos de popular o CSV com dados
numero_velas = 30 # Quantas velas?
# Comente a linha abaixo quando o csv tiver sido populado
# Ideia TODO: "Handlar" melhor esta parte
preco_velas_anteriores(numero_velas)
# Agora vamos definir que só queremos trabalhar com o preço de fechamento
# Lista TODO: Formatar a data no MT5 para TimeToString
fechamento = pd.read_csv('./dados/historico_{}.csv'.format(numero_velas))
fechamento = fechamento.preco_fechamento.values.tolist()
# Agora vamos criar uma funcionalidade tecnica pra nossa IA. 
# Porém a partir daqui a minha "Expertise" acaba e irei apenas mencionar as fontes,
# assim como as formas de como eu as interpreto. Portanto a você de fazer sua pesquisa se encontrar
# alguma coisa errada em minha interpretação.
def estado_atual(dados, t, n):
    # A técnica que vamos usar é a descrita no Artigo Académico:
    # [D. Wierstra, T. Schaul, J. Peters and J. Schmidhuber (2008)](http://people.idsia.ch/~tom/publications/nes.pdf)
    # Que ficou conhecido através da galera da OpenAI que venceram no Dota 2 em 1v1
    # Aquilo que queremos definir aqui é: t = (t + 1) — t
    # Onde t é o numero de população, o n o sigma (numero de velas que queremos prever),
    # e os dados (preço_fechamento) o alpha
    # O alpha é adaptável, assim como o número de população e sigma (alpha / (npops * sigma))
    d = t - n + 1
    bloco = dados[d : t + 1] if d >= 0 else -d * [dados[0]] + dados[: t + 1]
    resultado = []
    for i in range(n - 1):
        resultado.append(bloco[i + 1] - bloco[i])
    return np.array([resultado])


