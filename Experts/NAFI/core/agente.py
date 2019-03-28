import numpy as np
from collections import deque
import matplotlib.pyplot as plt
import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
from torch.distributions import Categorical
import sys, random
from random import randrange
from core.ambiente import Ambiente
from core.funcoes import *

device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
# Definindo o epsilon
epsilon = sys.float_info.epsilon

# Instanciando o Ambiente
ambiente = Ambiente()

# Instanciando as Ações
acoes = ambiente.acoes()
indices_acoes = randrange(len(acoes))
selecionar_acao_inicial = select_acao(epsilon, acoes)
acao_inicial = acoes[selecionar_acao_inicial]
atualizar_contagem = update_counts(indices_acoes) # TODO: Entender melhor esta "contagem"

class Policy(nn.Module):
    def __init__(self, s_size=4, h_size=16, a_size=2):
        super(Policy, self).__init__()
        self.fc1 = nn.Linear(s_size, h_size)
        self.fc2 = nn.Linear(h_size, a_size)

    def forward(self, x):
        x = F.relu(self.fc1(x))
        x = self.fc2(x)
        return F.softmax(x, dim=1)
    @staticmethod
    def act(self, acao):
        print(acao)
        acao = torch.from_numpy(acao).float().unsqueeze(0).to(device)
        probs = self.forward(acao).cpu()
        m = Categorical(probs)
        acao = m.sample()
        return acao.item(), m.log_prob(acao)


policy = Policy().to(device)
optimizer = optim.Adam(policy.parameters(), lr=1e-2)

def reinforce(n_episodes=1000, max_t=1000, gamma=1.0, print_every=100):
    scores_deque = deque(maxlen=100)
    scores = []
    for i_episode in range(1, n_episodes+1):
        saved_log_probs = []
        recompensas = []
        acao = ambiente.reset()
        print(acao)
        for t in range(max_t):
            acao, log_prob = Policy.act(acao)
            saved_log_probs.append(log_prob)
            acao, recompensa = ambiente.acao(acao_inicial)
            concluido = ambiente.concluido()
            recompensas.append(recompensa)
            if concluido:
                break 
        scores_deque.append(sum(recompensas))
        scores.append(sum(recompensas))
        
        discounts = [gamma**i for i in range(len(recompensas)+1)]
        R = sum([a*b for a,b in zip(discounts, recompensas)])
        
        policy_loss = []
        for log_prob in saved_log_probs:
            policy_loss.append(-log_prob * R)
        policy_loss = torch.cat(policy_loss).sum()
        
        optimizer.zero_grad()
        policy_loss.backward()
        optimizer.acao()
        
        if i_episode % print_every == 0:
            print('Episode {}\tAverage Score: {:.2f}'.format(i_episode, np.mean(scores_deque)))
        if np.mean(scores_deque)>=195.0:
            print('Environment solved in {:d} episodes!\tAverage Score: {:.2f}'.format(i_episode-100, np.mean(scores_deque)))
            break
        
    return scores
