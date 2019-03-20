#!/home/neo/anaconda3/bin/python
print('Bem-vindo(a) ao NIFA!')
print('---------------------')
print('Importando as bibliotecas...')
from subprocess import Popen
import sys

arquivo = sys.argv[1]
while True:
    print("\nExecutando o processo: " + arquivo)
    p = Popen("python " + arquivo, shell=True)
    p.wait()