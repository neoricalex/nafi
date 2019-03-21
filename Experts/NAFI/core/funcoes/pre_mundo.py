# -*- coding: utf-8 -*-
print('Importando as bibliotecas do Pré-Mundo...')
from datetime import date
from datetime import time
from datetime import datetime
from core.algorithms.algo import *
import socket, time, zmq
from core.envs.universo import GridUniverseEnv
from core.funcoes.mundo import *

print('Importando as funções do Pré-Mundo....')

# Adaptado de https://github.com/TheMTank/GridUniverse/blob/master/examples/griduniverse_env_examples.py
def run_griduniverse_from_text_file():
      """
      Run a random agent on an environment that was save via ascii text file.
      Check core/envs/maze_text_files for examples or the _create_custom_world_from_text() function within the environment
      """
      print('\n' + '*' * 10 + ' Criando um Ambiente pré-fabricado a partir de um arquivo de texto e executando um agente aleatório nele ' + '*' * 10 + '\n')
      env = GridUniverseEnv(custom_world_fp='./core/envs/universos/mundo.txt')
      for i_episode in range(1):
         observation = env._reset()
         rodando = True
         jogadas = 0
         while rodando:
               env._render(mode='ansi')
               action = env.action_space.sample()
               #print('go ' + env.action_descriptors[action])
               #time.sleep(1.5) # uncomment to watch slower
               observation, reward, done, info = env._step(action)
               if done:
                     print("O Algoritmo resolveu a equação em {} tentativas".format(jogadas + 1))
                     salvar(observation=observation)
                     print('[TODO]: Ver direito se o circuito da memória do estado inicial ta funcionando.')
                     rodando = False
               jogadas += 1

# Adaptado de https://gist.github.com/betrcode/0248f0fda894013382d7#file-is_port_open-py
def isOpen(ip,port):
   s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
   try:
      s.connect((ip, int(port)))
      s.shutdown(2)
      return True
   except:
      return False

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

# Conectar ao Meta Trader
def remote_send(socket, data):
    try:
        socket.send_string(data)
        msg = socket.recv_string()
        return (msg)
    except zmq.Again as e:
        print ("Aguardando o PUSH do MT5 ...")       

# Obter o contexto do zmq
context = zmq.Context()
# Criar um Socket para as requisições
reqSocket = context.socket(zmq.REQ)
reqSocket.connect("tcp://localhost:5555")

def checkar_pre_mundo():
    # Run random agent on environment variations
    print('Verificando se o Servidor MT5 está Online...')
    pingar = isOpen('127.0.0.1', 5555)

    # Provávelmente o while loop é melhor. Mas para já vamos de IF até termos um MVP :-)
    if pingar == True:

        # Checkar se é dia de semana localmente
        dia_semana = checkar_dia_semana_local()
        final_de_semana = [5, 6]
        if dia_semana in final_de_semana:
            print('[TODO] Final de Semana Local: DeepRL, RNN, NN ... :-) ')
        else:
            checkar_hora_local()
            checkar_algo()
            print('Por agora tudo parece estar certo. Iniciando o Ambiente...')
            #print('Parando o processo...')
            #exit()
            run_griduniverse_from_text_file()
    else:
        print('O Servidor do MT5 está Offline. Saindo ...')