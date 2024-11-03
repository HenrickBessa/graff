import numpy as np
import matplotlib.pyplot as plt
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

print(f"Média Fuzzy: {media_fuzzy:.4f}, Desvio Fuzzy: {desvio_fuzzy:.4f}")
print(f"Média Genético: {media_genetico:.4f}, Desvio Genético: {desvio_genetico:.4f}")
print(f"Média Sistema Fuzzy: {media_sistema_fuzzy:.4f}, Desvio Sistema Fuzzy: {desvio_sistema_fuzzy:.4f}")

labels = ['Fuzzy', 'Genético', 'Sistema Fuzzy']
medias = [media_fuzzy, media_genetico, media_sistema_fuzzy]
desvios = [desvio_fuzzy, desvio_genetico, desvio_sistema_fuzzy]

x = np.arange(len(labels))
largura = 0.35

fig, ax = plt.subplots()
barras1 = ax.bar(x - largura/2, medias, largura, label='Média', yerr=desvios, capsize=5)
ax.set_ylabel('Valor')
ax.set_title('Comparação das Médias e Desvios Padrão dos Empurrões')
ax.set_xticks(x)
ax.set_xticklabels(labels)
ax.legend()

plt.tight_layout()
plt.show()
