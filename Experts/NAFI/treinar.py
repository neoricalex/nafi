#!/home/neo/anaconda3/bin/python
print('Bem-vindo(a) ao NIFA!')
print('---------------------')
print('Importando as bibliotecas...')
from subprocess import Popen
import sys
from core.funcoes import pingar_mt5

# Checkar se o MT5 tá online
ping = pingar_mt5('localhost',5555)
try:
    ping
except:
    print('[DEBUG] O Servidor MT5 está Offline!')
    
arquivo = sys.argv[1]
while True:

    print("\nExecutando o processo: " + arquivo)
    p = Popen("python " + arquivo, shell=True)
    p.wait()