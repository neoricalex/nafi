from conexao import *
from datetime import datetime
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import os, csv, time

# Funções de tratamento das requisições/cotações atuais
def obter_rates(ticker): # Para chamar: obter_rates('TICKER') :: Ex: obter_rates('EURUSD')

    rates = remote_send(reqSocket, 'COTACOES|' + ticker)
    rates = rates.split(',')
    preco_bid_ticker = rates[0]
    preco_ask_ticker = rates[1]
    quantidade_buy_volume_ticker = rates[2]
    quantidade_sell_volume_ticker = rates[3]
    quantidade_tick_volume_ticker = rates[4]
    quantidade_real_volume_ticker = rates[5]
    quantidade_buy_volume_market_ticker = rates[6]
    quantidade_sell_volume_market_ticker = rates[7]

    data = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    header_csv = ['Data','Bid', 'Ask', 'buy_volume_ticker', 'sell_volume_ticker', 'tick_volume_ticker', 'real_volume_ticker', 'buy_volume_market_ticker', 'sell_volume_market_ticker']
    body_csv = [data, preco_bid_ticker, preco_ask_ticker, quantidade_buy_volume_ticker, quantidade_sell_volume_ticker, quantidade_tick_volume_ticker, quantidade_real_volume_ticker, quantidade_buy_volume_market_ticker, quantidade_sell_volume_market_ticker]

    # Criando um CSV com as cotações recebidas
    # Verificando se o csv já existe
    if os.path.exists('./dados/rates_{}.csv'.format(ticker)):
        # Se existir apenda
        with open('./dados/rates_{}.csv'.format(ticker), 'a', newline='\n') as csvfile:
            writer = csv.writer(csvfile, delimiter=',')
            writer.writerow(body_csv)        
            csvfile.close()
    else:
        # Se não existir cria
        with open('./dados/rates_{}.csv'.format(ticker), 'w', newline='') as csvfile:
            writer = csv.writer(csvfile, delimiter=',')
            writer.writerow(header_csv)
            writer.writerow(body_csv)
            csvfile.close()
    # IDEIA TODO: Thread python paralelo para treinamento de agentes em tempo real;
# Funções de tratamento das cotações histórico passado
def teste():
    # Preços de Abertura/Encerramento da barra/vela anterior
    teste = remote_send(reqSocket, 'TESTE')
    teste = teste.split(',')
    preco_abertura = teste[0]
    preco_fechamento = teste[1]

    print('preco_abertura: ' + preco_abertura + ' preco_fechamento: ' + preco_fechamento)

