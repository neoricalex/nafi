# -*- coding: utf-8 -*-
"""
Created on Tue Feb 19 18:44:22 2019

@author: [Ricardo Lourenço](https://neoricalex.com)

ACKNOWLEDGEMENTS: At the very end. Too many links .... THANK YOU !
LICENCE: GNU/GPLv2 (Not 3!) You gave me <-> i give you. 
"""

# Conectar ao Meta Trader
import zmq
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

# Continua no dados.py...

'''
  --------------------------------------------
  Artigos Acadêmicos, Postagens em Blog's etc ... que foram usados como referencia:
  --------------------------------------------
1) https://github.com/huseinzol05/Stock-Prediction-Models/blob/master/agent/updated-NES-google.ipynb
2) https://gist.github.com/karpathy/77fbb6a8dac5395f1b73e7a89300318d
3) [D. Wierstra, T. Schaul, J. Peters and J. Schmidhuber (2008)](http://people.idsia.ch/~tom/publications/nes.pdf)
4) [OpenAI's evolutionary strategies](https://blog.openai.com/evolution-strategies/)

[To Remember](https://www.cpuheater.com/deep-learning/introduction-to-recurrent-neural-networks-in-pytorch/)
[To Remember](https://gist.github.com/karpathy/77fbb6a8dac5395f1b73e7a89300318d)

# links bacanos
# https://docs.microsoft.com/en-us/sysinternals/
# https://www.unix.com/shell-programming-and-scripting/262488-ping-test-using-python.html
'''
