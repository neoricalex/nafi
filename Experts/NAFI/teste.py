from core.funcoes import *

carteira = []
#teste = abrir_posicao('EURUSD', '0.01')
#carteira.append(teste)
fechar_posicao = remote_send(reqSocket, 'TRADE|CLOSE|227260282')
fechar_posicao = fechar_posicao.split(',')
carteira.pop(227260282)
print(fechar_posicao)
print(carteira)
