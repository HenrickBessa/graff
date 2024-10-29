import numpy as np
from pendulo_invertido_simulacao import PenduloInvertido

def calcular_fitness(angulos, velocidades):
    return -np.abs(angulos[-1])  

def gerar_populacao(tamanho):
    return np.random.rand(tamanho, 9)  

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

def algoritmo_genetico(num_geracoes, tamanho_populacao, taxa_mutacao):
    populacao = gerar_populacao(tamanho_populacao)
    pendulo_simulacao = PenduloInvertido()  

    for geracao in range(num_geracoes):
        fitness = np.array([calcular_fitness(*pendulo_simulacao.simular_pendulo(10, 0.1)) for individuo in populacao])
        
        indices = np.argsort(fitness)[-tamanho_populacao // 2:]  
        nova_populacao = populacao[indices]

        while len(nova_populacao) < tamanho_populacao:
            pai1, pai2 = np.random.choice(nova_populacao, 2, replace=False)
            filho1, filho2 = cruzar(pai1, pai2)
            nova_populacao = np.vstack((nova_populacao, mutar(filho1, taxa_mutacao), mutar(filho2, taxa_mutacao)))

        populacao = nova_populacao

    melhor_individuo = populacao[np.argmax([calcular_fitness(*pendulo_simulacao.simular_pendulo(10, 0.1)) for individuo in populacao])]
    return melhor_individuo

if __name__ == '__main__':
    melhor_regras = algoritmo_genetico(num_geracoes=50, tamanho_populacao=20, taxa_mutacao=0.1)
    print("Melhor conjunto de regras:", melhor_regras)
