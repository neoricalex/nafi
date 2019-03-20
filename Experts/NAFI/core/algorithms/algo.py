print('Importando as bibliotecas do algoritmo...')
from datetime import date
from datetime import time
from datetime import datetime
print('Importando as funções do algoritmo...')
from core.funcoes.ping import *

def checkar_dia_semana_local():
    hoje = datetime.now()
    dia_da_semana = date.weekday(hoje)
    retorno = dia_da_semana

    return retorno

def checkar_hora_local():
    print('[TODO]: Checkar a hora local e rodar a melhor Exchange ')

    hoje = datetime.now()

    dia_da_semana = date.weekday(hoje)
    dias_da_semana = ['Segunda-Feira','Terça-Feira','Quarta-Feira','Quinta-Feira','Sexta-Feira','Sábado','Domingo']

    horas = datetime.time(datetime.now())
    horas = datetime.time(datetime.now())

    print('Hoje é', dias_da_semana[dia_da_semana] , 'e são' , horas , 'horas') 
    pass