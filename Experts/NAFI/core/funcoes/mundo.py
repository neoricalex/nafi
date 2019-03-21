import os
try:
    import _pickle as pickle
except ImportError:
    import cPickle as pickle

def salvar(observation):
    # setar a memória
    memoria = "./core/memoria.pkl"
    estado_inicial = [observation]
    with open(memoria, "rb") as f:
        estado_inicial.append(pickle.load(f))
        f.close()
