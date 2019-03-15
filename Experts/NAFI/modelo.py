from estado import *

class Modelo:
    def __init__(self, tamanho_dendritos, tamanho_axonios, tamanho_terminal_axonios):
        self.neuronios = [
            np.random.randn(tamanho_dendritos, tamanho_axonios),
            np.random.randn(tamanho_axonios, tamanho_terminal_axonios),
            np.random.randn(tamanho_axonios, 1),
            np.random.randn(1, tamanho_axonios),
        ]

    def previsao(self, dendritos):
        alimentar = np.dot(dendritos, self.neuronios[0]) + self.neuronios[-1]
        decisao = np.dot(alimentar, self.neuronios[1])
        comprar = np.dot(alimentar, self.neuronios[2])
        return decisao, comprar

    def criar_neuronios(self):
        return self.neuronios

    def criar_neuronio(self, neuronios):
        self.neuronios = neuronios

def agir(modelo, sequencia):
    decisao, comprar = modelo.previsao(np.array(sequencia))
    return np.argmax(decisao[0]), int(comprar[0])

numero_velas_para_prever = 7
modelo = Modelo(numero_velas_para_prever, 100, 3)
neuronio = modelo
saldo = 100
orcamento = 100
tamanho_alvo = len(alvo) - 1
ignorar = 1
estado = estado_atual(alvo, 0, numero_velas_para_prever + 1)
carteira = []
quantidade = 0
comprar_volume_maximo = 5
vender_volume_maximo  = 5

for tecido_nervoso in range(0, tamanho_alvo, ignorar):
    acao, comprar = agir(neuronio, estado)
    estado_seguinte = estado_atual(alvo, tecido_nervoso + 1, numero_velas_para_prever + 1)
    if acao == 1 and orcamento >= alvo[tecido_nervoso]:
        if comprar < 0:
            comprar = 1
        if comprar > comprar_volume_maximo:
            comprar_unidades = comprar_volume_maximo
        else:
            comprar_unidades = comprar
        total_compra = comprar_unidades * alvo[tecido_nervoso]
        orcamento -= total_compra
        carteira.append(total_compra)
        quantidade += comprar_unidades
    elif acao == 2 and len(carteira) > 0:
        if quantidade > vender_volume_maximo:
            vender_unidades = vender_volume_maximo
        else:
            vender_unidades = quantidade
        quantidade -= vender_unidades
        total_venda = vender_unidades * alvo[tecido_nervoso]
        orcamento += vender_unidades

    estado = estado_seguinte

resultado_modelo = ((saldo - orcamento) / orcamento) * 100
