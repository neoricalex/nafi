#!/home/neo/anaconda3/bin/python
print('Bem-vindo(a) ao NAFI!')
print('---------------------')
print('Importando as bibliotecas...')
from subprocess import Popen
import sys, socket

print('Checkar se o servidor tá online...')
ip = 'localhost'
porta = '5555'
pingar = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    pingar.connect((ip, int(porta)))
    pingar.shutdown(2)
except:
    print('A porta {} do {} está fechada.'.format(porta, ip))
    exit()

# Iniciando o main loop ...   
arquivo = sys.argv[1]
while True:

    print("\nExecutando o processo: " + arquivo)
    p = Popen("python " + arquivo, shell=True)
    p.wait()