from conexao import *
from time import time
import os, csv, random, datetime
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
def escolher_ticker():
    tickers = ['EURUSD', 'GBPUSD', 'USDCHF', 'USDJPY', 'USDCAD', 'AUDUSD', 'EURCHF', 'EURJPY', 'EURGBP', 'EURCAD', 'GBPCHF', 'GBPJPY', 'AUDJPY']
    ticker = random.choice(tickers)

    return ticker
# E saber as infos do ticker, assim como mandar pro CSV
def infos_ticker(ticker):
    infos_ticker = remote_send(reqSocket, 'INFO_TICKER|' + ticker)
    infos_ticker = infos_ticker.split(',')
    preco_venda = infos_ticker[0]
    preco_compra = infos_ticker[1]
    data = infos_ticker[8]
    data = datetime.datetime.fromtimestamp(int(data)).strftime('%Y-%m-%d %H:%M:%S')

    header_csv = ['data', 'preco_compra']
    body_csv = [data, preco_compra]

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
            data_vela = datetime.datetime.fromtimestamp(int(data_vela)).strftime('%Y-%m-%d %H:%M:%S')

            # depois vamos criar o header e o body do CSV
            header_csv = ['data', 'preco_compra']
            body_csv = [data_vela, preco_compra]

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
# Continua no estado.py ...