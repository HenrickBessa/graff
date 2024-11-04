import numpy as np
from neuro_fuzzy import SistemaNeuroFuzzy
from sklearn.metrics import mean_squared_error

def gerar_dados_simulados(num_samples):
    angulos = np.random.uniform(-10, 10, num_samples)
    velocidades = np.random.uniform(-5, 5, num_samples)
    empurros = angulos * 0.5 + velocidades * 1.5 + np.random.normal(0, 1, num_samples)
    return np.column_stack((angulos, velocidades, empurros))

if __name__ == "__main__":
    sistema = SistemaNeuroFuzzy()
    dados = gerar_dados_simulados(1000)

    num_train = int(0.8 * len(dados))
    dados_treino = dados[:num_train]
    dados_teste = dados[num_train:]

    sistema.treinar(dados_treino)

    X_test = dados_teste[:, :2]
    y_test = dados_teste[:, 2]
    previsoes = sistema.prever(X_test[:, 0], X_test[:, 1])

    mse = mean_squared_error(y_test, previsoes)

    print(f"Treinamento concluído com {num_train} amostras.")
    print(f"Média dos erros quadráticos (MSE) no conjunto de teste: {mse:.2f}")

    for i in range(5):
        print(f"Previsão {i+1}: Angulo: {X_test[i, 0]}, Velocidade: {X_test[i, 1]} => Empurro Previsto: {previsoes[i]:.2f}")
