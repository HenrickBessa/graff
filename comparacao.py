# Ao final, o código calcula e exibe a média e o desvio padrão dos empurrões em cada abordagem, permitindo uma comparação entre elas

import numpy as np
from pendulo_invertido_fuzzy import PenduloInvertido
from pendulo_invertido_genetic import algoritmo_genetico
from pendulo_invertido import criar_sistema_fuzzy
from skfuzzy import control as ctrl

angulos = np.linspace(-0.15, 0.15, 10)
velocidades = np.linspace(-0.15, 0.15, 10)

pendulo_fuzzy = PenduloInvertido()
resultados_fuzzy = []
for angulo in angulos:
    for velocidade in velocidades:
        empurro = pendulo_fuzzy.simular(angulo, velocidade)
        resultados_fuzzy.append((angulo, velocidade, empurro))

melhores_regras_genetico = algoritmo_genetico(50, 20, 0.1, angulos, velocidades)
resultados_genetico = []
for angulo in angulos:
    for velocidade in velocidades:
        empurro = pendulo_fuzzy.simular(angulo, velocidade)
        resultados_genetico.append((angulo, velocidade, empurro))

pendulo_ctrl = criar_sistema_fuzzy()
simulador_fuzzy = ctrl.ControlSystemSimulation(pendulo_ctrl)
resultados_sistema_fuzzy = []
for angulo in np.arange(-10, 11, 1):
    for velocidade in np.arange(-5, 6, 1):
        simulador_fuzzy.input['angulo'] = angulo
        simulador_fuzzy.input['velocidade_angular'] = velocidade
        simulador_fuzzy.compute()
        empurro = simulador_fuzzy.output['empurrao_carro']
        resultados_sistema_fuzzy.append((angulo, velocidade, empurro))

resultados_fuzzy = np.array(resultados_fuzzy)
resultados_genetico = np.array(resultados_genetico)
resultados_sistema_fuzzy = np.array(resultados_sistema_fuzzy)

media_fuzzy = np.mean(resultados_fuzzy[:, 2])
media_genetico = np.mean(resultados_genetico[:, 2])
media_sistema_fuzzy = np.mean(resultados_sistema_fuzzy[:, 2])

desvio_fuzzy = np.std(resultados_fuzzy[:, 2])
desvio_genetico = np.std(resultados_genetico[:, 2])
desvio_sistema_fuzzy = np.std(resultados_sistema_fuzzy[:, 2])

print(f"Média Fuzzy: {media_fuzzy}, Desvio Fuzzy: {desvio_fuzzy}")
print(f"Média Genético: {media_genetico}, Desvio Genético: {desvio_genetico}")
print(f"Média Sistema Fuzzy: {media_sistema_fuzzy}, Desvio Sistema Fuzzy: {desvio_sistema_fuzzy}")
