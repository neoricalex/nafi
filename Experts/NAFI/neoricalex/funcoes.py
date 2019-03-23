from neoricalex.conexao import *
import datetime, random

def infos_ticker(ticker):
    infos_ticker = remote_send(reqSocket, 'INFO_TICKER|' + ticker)
    infos_ticker = infos_ticker.split(',')

    return infos_ticker

def historico_ticker(ticker, numero_velas):
    for i in reversed(range(int(numero_velas) + 1)):
        if i == 0:
            pass
        else:
            pass
            # OK, agora vamos pedir o preço para cada vela
            historico_ticker = remote_send(reqSocket, 'HISTORICO|' + str(i) + '|' + ticker)
            historico_ticker = historico_ticker.split(',')

    return historico_ticker

def infos_conta():
    infos_conta = remote_send(reqSocket, 'INFO_CONTA')
    infos_conta = infos_conta.split(',')

    return infos_conta

def escolher_numero_velas():
    data1 = datetime.datetime(2007, 12, 5)
    data2 = datetime.datetime.now()

    diff = data2 - data1

    days, seconds = diff.days, diff.seconds
    horas = days * 24 + seconds // 3600
    #minutes = (seconds % 3600) // 60
    #seconds = seconds % 60
    numero_velas = random.choice(range(1, horas))

    if numero_velas > 1000:
        numero_velas = 1000
        print('[INFO] O número de velas foi reduzido para', numero_velas)

    numero_velas = 1
    print('[DEBUG] funcoes.py/escolher_numero_velas = 1')

    return numero_velas
