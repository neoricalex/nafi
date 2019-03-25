from core.ambiente import Ambiente
import random

if __name__ == "__main__":
    ambiente = Ambiente()
    recompensa_total = 0.0
    total_passos = 0

    while True:
        acoes = ambiente.acoes()
        acao, recompensa  = ambiente.acao(random.choice(acoes))
        concluido = ambiente.concluido()

        recompensa_total = recompensa
        total_passos += 1
        
        if concluido == True:
            break

    print("Circuito efetuado em %d passos, com uma recompensa total de %.2f" % (total_passos, recompensa_total))
