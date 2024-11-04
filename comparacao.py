import numpy as np
from neuro_fuzzy import SistemaNeuroFuzzy
from sklearn.metrics import mean_squared_error

def gerar_dados_simulados(num_samples):
    angulos = np.random.uniform(-10, 10, num_samples)
    velocidades = np.random.uniform(-5, 5, num_samples)
    empurros = angulos * 0.5 + velocidades * 1.5 + np.random.normal(0, 1, num_samples)
    return np.column_stack((angulos, velocidades, empurros))

def comparar_sistemas(sistema_fuzzy, sistema_neuro_fuzzy, angulos, velocidades):
    mse_fuzzy = []
    mse_neuro_fuzzy = []

    for angulo in angulos:
        for velocidade in velocidades:
            empurro_fuzzy = sistema_fuzzy.simular(angulo, velocidade)
            empurro_neuro_fuzzy = sistema_neuro_fuzzy.prever([angulo], [velocidade])[0]

            if empurro_fuzzy is not None and empurro_neuro_fuzzy is not None:
                mse_fuzzy.append(empurro_fuzzy)
                mse_neuro_fuzzy.append(empurro_neuro_fuzzy)

    if len(mse_fuzzy) > 0 and len(mse_neuro_fuzzy) > 0:
        mse_value = mean_squared_error(mse_fuzzy, mse_neuro_fuzzy)
        return mse_value
    else:
        return None

if __name__ == "__main__":
    sistema_neuro_fuzzy = SistemaNeuroFuzzy()

    dados = gerar_dados_simulados(1000)
    num_train = int(0.8 * len(dados))
    dados_treino = dados[:num_train]

    sistema_neuro_fuzzy.treinar(dados_treino)

    angulos = np.linspace(-10, 10, 20)
    velocidades = np.linspace(-5, 5, 20)
    mse = comparar_sistemas(sistema_neuro_fuzzy, sistema_neuro_fuzzy, angulos, velocidades)

    if mse is not None:
        print("MSE entre Fuzzy e Neuro-Fuzzy:", mse)
    else:
        print("Não foram feitas previsões válidas para calcular o MSE.")
