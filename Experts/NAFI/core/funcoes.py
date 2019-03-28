import datetime, random
import socket
from core.conexao import *

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

def abrir_posicao(ticker, volume):
    abre_posicao = remote_send(reqSocket, 'TRADE|OPEN|TICKER|VOLUME')
    abre_posicao = abre_posicao.split(',')

    return abre_posicao

# Starting adaptation from https://prakhartechviz.blogspot.com/2019/02/epsilon-greedy-reinforcement-learning.html
counts = [0,0,0,0,0,0]
values = [0,0,0,0,0,0]
value = 0

def explore(values):  
    '''  
    Returns the index of maximum average value   
    for an acao  
    '''  
    return values.index(max(values))

def exploit(values):  
    '''  
    Returns random average value for an acao  
    '''  

    return random.randrange(len(values))

def select_acao(epsilon, values):  
    '''  
    If the random number is greater than epsilon  
    then we exploit else we explore.  
    '''  

    if random.random() > epsilon:
        print('[DEBUG] Decisão:', exploit(values))  
        return exploit(values)  
    else: 
        print('[DEBUG] Explorar:', exploit(values))  
        return explore(values)

def update_counts(acao):  
    '''  
    Update the value of count corresponding   
    to the acao that is taken.  
    '''  

    counts[acao] = counts[acao] + 1 

    return counts

def update_values(acao, reward, counts):  
    '''  
    Calculates the estimated value for the chosen  
    acao. If this is the first experience ever with   
    the chosen arm, we set the estimated value directly   
    to the reward we just received from playing that arm.  
    If we had played the arm in the past, i.e n != 0,   
    we update the estimated value of the chosen arm to   
    be a weighted average of the previously estimated   
    value and the reward we just received.  
    '''  
    current_value = values[acao]  
    n = counts[acao]  
    values[acao] = ((n-1)/float(n))*value + (1/float(n))*reward  
    return values

def update_all(acao, reward):  
    counts = update_counts(acao)  
    values = update_values(acao, reward, counts)  
    return counts, values  
# End adaptation

def pingar_mt5(ip,porta):
   pingar = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
   try:
      pingar.connect((ip, int(porta)))
      pingar.shutdown(2)
      return True
   except:
      return False