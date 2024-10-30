import numpy as np
from pendulo_invertido_fuzzy import PenduloInvertido 

def calcular_fitness(pendulo, angulo, velocidade):
    empurro = pendulo.simular(angulo, velocidade)
    return -np.abs(empurro)  

def gerar_populacao(tamanho_populacao, num_regras):
    return np.random.rand(tamanho_populacao, num_regras)

def cruzar(pai1, pai2):
    ponto = np.random.randint(1, len(pai1) - 1)
    filho1 = np.concatenate((pai1[:ponto], pai2[ponto:]))
    filho2 = np.concatenate((pai2[:ponto], pai1[ponto:]))
    return filho1, filho2

def mutar(individuo, taxa_mutacao):
    for i in range(len(individuo)):
        if np.random.rand() < taxa_mutacao:
            individuo[i] += np.random.normal(0, 0.1)
    return individuo

def algoritmo_genetico(num_geracoes, tamanho_populacao, taxa_mutacao, angulos, velocidades):
    pendulo = PenduloInvertido()
    populacao = gerar_populacao(tamanho_populacao, len(pendulo.regras))
    
    for geracao in range(num_geracoes):
        fitness = []
        for individuo in populacao:
            fitness_individuo = 0
            for angulo in angulos:
                for velocidade in velocidades:
                    fitness_individuo += calcular_fitness(pendulo, angulo, velocidade)
            fitness.append(fitness_individuo)
        
        fitness = np.array(fitness)
        indices = np.argsort(fitness)[-tamanho_populacao // 2:]
        nova_populacao = populacao[indices]

        while len(nova_populacao) < tamanho_populacao:
            idx_pais = np.random.choice(len(nova_populacao), 2, replace=False)
            pai1, pai2 = nova_populacao[idx_pais[0]], nova_populacao[idx_pais[1]]
            filho1, filho2 = cruzar(pai1, pai2)
            nova_populacao = np.vstack((nova_populacao, mutar(filho1, taxa_mutacao), mutar(filho2, taxa_mutacao)))

        populacao = nova_populacao

    melhor_individuo = populacao[np.argmax(fitness)]
    return melhor_individuo

if __name__ == "__main__":
    angulos = np.linspace(-0.15, 0.15, 10)
    velocidades = np.linspace(-0.15, 0.15, 10)
    melhores_regras = algoritmo_genetico(num_geracoes=50, tamanho_populacao=20, taxa_mutacao=0.1, angulos=angulos, velocidades=velocidades)
    print("Melhor conjunto de regras:", melhores_regras)
