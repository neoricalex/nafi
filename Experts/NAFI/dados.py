from conexao import *
from time import time
import os, csv, random, datetime
import pandas as pd

# Primeiro vamos acessar nossa conta na corretora, obter as infos e mandar para um CSV
def infos_conta():
    infos_conta = remote_send(reqSocket, 'INFO_CONTA')
    infos_conta = infos_conta.split(',')
    saldo = infos_conta[0]
    credito = infos_conta[1]
    lucro = infos_conta[2]
    equity = infos_conta[3]
    margem = infos_conta[4]
    margem_livre = infos_conta[5]
    margem_level = infos_conta[6]
    margem_socall = infos_conta[7]
    margem_soso = infos_conta[8]
    data = infos_conta[9]
    data = datetime.datetime.fromtimestamp(int(data)).strftime('%Y-%m-%d %H:%M:%S')

     # criando o header e o body do CSV
    header_csv = ['data', 'saldo']
    body_csv = [data, saldo]

    # Verificando se o csv já existe
    if os.path.exists('./dados/infos_conta.csv'):
        # Se existir apenda
        with open('./dados/infos_conta.csv', 'a', newline='\n') as csvfile:
            writer = csv.writer(csvfile, delimiter=',')
            writer.writerow(body_csv)        
            csvfile.close()
    else:
        # Se não existir cria
        with open('./dados/infos_conta.csv', 'w', newline='') as csvfile:
            writer = csv.writer(csvfile, delimiter=',')
            writer.writerow(header_csv)
            writer.writerow(body_csv)
            csvfile.close()
# Agora vamos selecionar um Ticker
# escolher randomicamente
def escolher_ticker():
    tickers = ['EURUSD', 'GBPUSD', 'USDCHF', 'USDJPY', 'USDCAD', 'AUDUSD',
                'EURCHF', 'EURJPY', 'EURGBP', 'EURCAD', 'GBPCHF', 'GBPJPY', 
                'AUDJPY', 'GOLD', 'SILVER']
    ticker = random.choice(tickers)

    return ticker
# E saber as infos do ticker, assim como mandar pro CSV
# media precos
def media(precos):
    return float(sum(precos)) / max(len(precos), 1)

def infos_ticker(ticker):
    infos_ticker = remote_send(reqSocket, 'INFO_TICKER|' + ticker)
    infos_ticker = infos_ticker.split(',')

    preco_venda = infos_ticker[0]
    preco_compra = infos_ticker[1]
    preco_buy_volume = infos_ticker[2]
    preco_sell_volume = infos_ticker[3]
    preco_tick_volume = infos_ticker[4]
    preco_real_volume = infos_ticker[5]
    preco_buy_volume_market = infos_ticker[6]
    preco_sell_volume_market = infos_ticker[7]
    data = infos_ticker[8]
    #data = datetime.datetime.fromtimestamp(int(data)).strftime('%Y-%m-%d %H:%M:%S')

    # Compatibilizar com historico

    preco_abertura  = media([float(preco_venda), float(preco_compra)])
    preco_fechamento = preco_abertura

    header_csv = ['data', 'preco_abertura', 'preco_fechamento', 'preco_venda', 'preco_compra']
    body_csv = [data, preco_abertura, preco_fechamento, preco_venda, preco_compra]

    # Verificando se o csv já existe
    if os.path.exists('./dados/historico_{}.csv'.format(ticker)):
        # Se existir apenda
        with open('./dados/historico_{}.csv'.format(ticker), 'a', newline='\n') as csvfile:
            writer = csv.writer(csvfile, delimiter=',')
            writer.writerow(body_csv)        
            csvfile.close()
    else:
        # Se não existir cria
        with open('./dados/historico_{}.csv'.format(ticker), 'w', newline='') as csvfile:
            writer = csv.writer(csvfile, delimiter=',')
            writer.writerow(header_csv)
            writer.writerow(body_csv)
            csvfile.close()

    return infos_ticker
# Como não temos nossos CSV's populados vamos popular eles
def popular_csv_infos_ticker(ticker, numero_velas):
    # TODO: Melhorar e muito esta parte
    # Como o MT5 não sabe que o que queremos é o preço para cada vela,
    # e não o preço da vela em questão temos de iterar
    for i in reversed(range(numero_velas + 1)):
        if i == 0:
            pass
        else:
            # OK, agora vamos pedir o preço para cada vela
            preco_velas = remote_send(reqSocket, 'HISTORICO|' + str(i) + '|' + ticker)
            preco_velas = preco_velas.split(',')
            preco_abertura = preco_velas[0]
            preco_fechamento = preco_velas[1]
            preco_compra = preco_fechamento # TODO aqui
            data_vela = preco_velas[2]
            #data_vela = datetime.datetime.fromtimestamp(int(data_vela)).strftime('%Y-%m-%d %H:%M:%S')

            # Compatibilizar com cotacoes

            preco_venda = media([float(preco_abertura), float(preco_fechamento)])
            preco_compra = preco_venda

            header_csv = ['data', 'preco_abertura', 'preco_fechamento', 'preco_venda', 'preco_compra']
            body_csv = [data_vela, preco_abertura, preco_fechamento, preco_venda, preco_compra]

            # Verificando se o csv já existe
            if os.path.exists('./dados/historico_{}.csv'.format(ticker)):
                # Se existir apenda
                with open('./dados/historico_{}.csv'.format(ticker), 'a', newline='\n') as csvfile:
                    writer = csv.writer(csvfile, delimiter=',')
                    writer.writerow(body_csv)        
                    csvfile.close()
            else:
                # Se não existir cria
                with open('./dados/historico_{}.csv'.format(ticker), 'w', newline='') as csvfile:
                    writer = csv.writer(csvfile, delimiter=',')
                    writer.writerow(header_csv)
                    writer.writerow(body_csv)
                    csvfile.close()
# 
def contar_linhas_csv(ticker):
    with open('./dados/historico_{}.csv'.format(ticker)) as f:
        return sum(1 for linha in f)
        f.close()

# Continua no estado.py ...