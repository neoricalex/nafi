from agente import *
from modelo import *

modelo = Modelo(
    tamanho_dendritos = numero_velas_para_prever,
    tamanho_axonios = 10000,
    tamanho_terminal_axonios = 3
    )
agente = Agente(
    modelo = modelo,
    saldo = saldo,
    comprar_volume_maximo = comprar_volume_maximo,
    vender_volume_maximo = vender_volume_maximo,
    alvo = alvo,
    numero_velas_para_prever = numero_velas_para_prever,
    ignorar = 1,
)

print('Ticker ', ticker, ': o resultado do modelo é ', resultado_modelo)
agente.treinar(iteracoes = 500, checkagem = 100)
#agente.comprar()