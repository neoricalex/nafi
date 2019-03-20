from conexao import *
import datetime

# Função para obter a cotação atual
def obter_cotacoes(ticker): 
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

# Funções operacionais
def comprar_ativo(ticker):
    comprar = remote_send(reqSocket, 'TRADE|OPEN|0.2')
    comprar = comprar.split(',')
    ticket = comprar[0]

    return ticket
def vender_ativo(ticker):
    vender = remote_send(reqSocket, 'TRADE|CLOSE|226070973')
    vender = vender.split(',')
    print(vender)

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

    return infos_conta

def saldo():
    infos_conta = remote_send(reqSocket, 'INFO_CONTA')
    infos_conta = infos_conta.split(',')
    saldo = infos_conta[0]

    return saldo
