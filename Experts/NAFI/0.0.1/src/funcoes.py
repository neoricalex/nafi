from conexao import *


# Função para obter a cotação atual
def obter_cotacoes(ticker): # Para chamar: obter_cotacoes('TICKER') :: Ex: obter_rates('EURUSD')
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

    header_csv = ['Bid', 'Ask', 'buy_volume_ticker', 'sell_volume_ticker', 'tick_volume_ticker', 'real_volume_ticker', 'buy_volume_market_ticker', 'sell_volume_market_ticker']
    body_csv = [preco_bid_ticker, preco_ask_ticker, quantidade_buy_volume_ticker, quantidade_sell_volume_ticker, quantidade_tick_volume_ticker, quantidade_real_volume_ticker, quantidade_buy_volume_market_ticker, quantidade_sell_volume_market_ticker]

    # Criando um CSV com as cotações recebidas
    # Verificando se o csv já existe
    import os, csv
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

# Funções operacionais
def comprar_ativo(ticker):
    comprar = remote_send(reqSocket, 'TRADE|OPEN|0.2')
    comprar = comprar.split(',')
    print(comprar)
def vender_ativo(ticker):
    vender = remote_send(reqSocket, 'TRADE|CLOSE|226070973')
    vender = vender.split(',')
    print(vender)