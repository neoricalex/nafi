from modelo import *

class Ambiente:
    def __init__(
        self, neuronios, funcao_recompensa, tecido_nervoso, sigma, taxa_aprendizado
    ):
        self.neuronios = neuronios
        self.funcao_recompensa = funcao_recompensa
        self.tecido_nervoso = tecido_nervoso
        self.sigma = sigma
        self.taxa_aprendizado = taxa_aprendizado

    def _chamar_neuronio_do_tecido(self, neuronios, tecido):
        neuronios_tecido = []
        for index, i in enumerate(tecido):
            ionizar = self.sigma * i # Agitar (de -58mV para +40mV segundo a Wikipédia)
            neuronios_tecido.append(neuronios[index] + ionizar)
        return neuronios_tecido

    def criar_neuronios(self):
        return self.neuronios

    def treinamento(self, epoch = 100, printar_cada = 1):
        tempo_duracao = time.time()
        for cada_epoca in range(epoch):
            tecido = []
            recompensas = np.zeros(self.tecido_nervoso)
            for k in range(self.tecido_nervoso):
                x = []
                for w in self.neuronios:
                    x.append(np.random.randn(*w.shape))
                tecido.append(x)
            for k in range(self.tecido_nervoso):
                neuronios_tecido = self._chamar_neuronio_do_tecido(
                    self.neuronios, tecido[k]
                )
                recompensas[k] = self.funcao_recompensa(neuronios_tecido)
            recompensas = (recompensas - np.mean(recompensas)) / np.std(recompensas)
            for index, w in enumerate(self.neuronios):
                A = np.array([p[index] for p in tecido])
                self.neuronios[index] = (
                    w
                    + self.taxa_aprendizado
                    / (self.tecido_nervoso * self.sigma)
                    * np.dot(A.T, recompensas).T
                )
            if (cada_epoca + 1) % printar_cada == 0:
                print(
                    'Checkagem da Iteração %d. Recompensa: %f'
                    % (cada_epoca + 1, self.funcao_recompensa(self.neuronios))
                )
        print('Tempo total do treinamento:', time.time() - tempo_duracao, 'segundos')

class Agente:
    
    POPULATION_SIZE = 50
    SIGMA = 0.1
    LEARNING_RATE = 0.001
    
    def __init__(self, modelo, saldo, comprar_volume_maximo, vender_volume_maximo, alvo, numero_velas_para_prever, ignorar):
        self.numero_velas_para_prever = numero_velas_para_prever
        self.ignorar = ignorar
        self.alvo = alvo
        self.modelo = modelo
        self.saldo = saldo
        self.comprar_volume_maximo = comprar_volume_maximo
        self.vender_volume_maximo = vender_volume_maximo
        self.estrategia = Ambiente(self.modelo.criar_neuronios(), self.receber_recompensa, self.POPULATION_SIZE, self.SIGMA, self.LEARNING_RATE)
    
    def agir(self, sequence):
        decisao, comprar = self.modelo.previsao(np.array(sequence))
        return np.argmax(decisao[0]), int(comprar[0])
    
    def receber_recompensa(self, neuronios):
        saldo = self.saldo
        orcamento = saldo
        tamanho_alvo = len(self.alvo) - 1
        
        self.modelo.neuronios = neuronios
        estado = estado_atual(self.alvo, 0, self.numero_velas_para_prever + 1)
        carteira = []
        quantidade = 0
        for tecido_nervoso in range(0, tamanho_alvo, self.ignorar):
            acao, comprar = self.agir(estado)
            estado_seguinte = estado_atual(self.alvo, tecido_nervoso + 1, self.numero_velas_para_prever + 1)
            if acao == 1 and saldo >= self.alvo[tecido_nervoso]:
                if comprar < 0:
                    comprar = 1
                if comprar > self.comprar_volume_maximo:
                    comprar_unidades = self.comprar_volume_maximo
                else:
                    comprar_unidades = comprar
                total_compra = comprar_unidades * self.alvo[tecido_nervoso]
                saldo -= total_compra
                carteira.append(total_compra)
                quantidade += comprar_unidades
            elif acao == 2 and len(carteira) > 0:
                if quantidade > self.vender_volume_maximo:
                    vender_unidades = self.vender_volume_maximo
                else:
                    vender_unidades = quantidade
                quantidade -= vender_unidades
                total_venda = vender_unidades * self.alvo[tecido_nervoso]
                saldo += total_venda
                
            estado = estado_seguinte
        return ((saldo - orcamento) / orcamento) * 100
    
    def treinar(self, iteracoes, checkagem):
        self.estrategia.treinamento(iteracoes, printar_cada=checkagem)
        
    def comprar(self):
        saldo = self.saldo
        tamanho_alvo = len(self.alvo) - 1
        estado = estado_atual(self.alvo, 0, self.numero_velas_para_prever + 1)
        orcamento = saldo
        estado_vender = []
        estado_comprar = []
        carteira = []
        quantidade = 0
        for tecido_nervoso in range(0, tamanho_alvo, self.ignorar):
            acao, comprar = self.agir(estado)
            estado_seguinte = estado_atual(self.alvo, tecido_nervoso + 1, self.numero_velas_para_prever + 1)
            if acao == 1 and saldo >= self.alvo[tecido_nervoso]:
                if comprar < 0:
                    comprar = 1
                if comprar > self.comprar_volume_maximo:
                    comprar_unidades = self.comprar_volume_maximo
                else:
                    comprar_unidades = comprar
                total_compra = comprar_unidades * self.alvo[tecido_nervoso]
                saldo -= total_compra
                carteira.append(total_compra)
                quantidade += comprar_unidades
                estado_comprar.append(tecido_nervoso)
                print('Dia %d: comprou %d unidades ao preço %f. Saldo %f' \
                      %(tecido_nervoso, comprar_unidades, total_compra,saldo))
            elif acao == 2 and len(carteira) > 0:
                preco_de_compra = carteira.pop(0)
                if quantidade > self.vender_volume_maximo:
                    vender_unidades = self.vender_volume_maximo
                else:
                    vender_unidades = quantidade
                if vender_unidades < 1:
                    continue
                quantidade -= vender_unidades
                total_venda = vender_unidades * self.alvo[tecido_nervoso]
                saldo += total_venda
                estado_vender.append(tecido_nervoso)
                try:
                    investimento = ((total_venda - preco_de_compra) / preco_de_compra) * 100
                except:
                    investimento = 0
                print('Dia %d, vendeu %d unidades %f, investimento de %f %%, Saldo %f,'%(tecido_nervoso, vender_unidades, total_venda, investimento, saldo))
            estado = estado_seguinte
        
        investimento = ((saldo - orcamento) / orcamento) * 100
        print('\nLucro/Prejuízo total: %f ROI: %f %%'%(saldo - orcamento,investimento))
        #plt.figure(figsize=(20,10))
        #plt.plot(alvo, label='true alvo',c='g')
        #plt.plot(alvo, 'X', label='previsao comprar',markevery=estado_comprar, c='b')
        #plt.plot(alvo, 'o', label='previsao vender',markevery=estado_vender,c='r')
        #plt.legend()
        #plt.show()
