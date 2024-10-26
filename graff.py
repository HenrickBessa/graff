import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
import matplotlib.pyplot as plt

# Definindo as variáveis fuzzy de entrada
angulo = ctrl.Antecedent(np.arange(-10, 11, 1), 'angulo')
velocidade_angular = ctrl.Antecedent(np.arange(-5, 6, 1), 'velocidade_angular')

# Definindo a variável fuzzy de saída
empurrao_carro = ctrl.Consequent(np.arange(-10, 11, 1), 'empurrao_carro')

# Definindo conjuntos de pertinência para ângulo
angulo['N'] = fuzz.trimf(angulo.universe, [-10, -5, 0])  # Inclinado para a esquerda
angulo['Z'] = fuzz.trimf(angulo.universe, [-1, 0, 1])    # Vertical
angulo['P'] = fuzz.trimf(angulo.universe, [0, 5, 10])    # Inclinado para a direita

# Definindo conjuntos de pertinência para velocidade angular
velocidade_angular['N'] = fuzz.trimf(velocidade_angular.universe, [-5, -2, 0])  # Deslocando-se para a esquerda
velocidade_angular['Z'] = fuzz.trimf(velocidade_angular.universe, [-1, 0, 1])   # Parado
velocidade_angular['P'] = fuzz.trimf(velocidade_angular.universe, [0, 2, 5])    # Deslocando-se para a direita

# Definindo conjuntos de pertinência para empurrão do carro
empurrao_carro['forte_esquerda'] = fuzz.trimf(empurrao_carro.universe, [-10, -7, -3])
empurrao_carro['leve_esquerda'] = fuzz.trimf(empurrao_carro.universe, [-5, -3, 0])
empurrao_carro['neutro'] = fuzz.trimf(empurrao_carro.universe, [-1, 0, 1])
empurrao_carro['leve_direita'] = fuzz.trimf(empurrao_carro.universe, [0, 3, 5])
empurrao_carro['forte_direita'] = fuzz.trimf(empurrao_carro.universe, [3, 7, 10])

# Visualização dos conjuntos fuzzy (opcional)
def plot_memberships():
    fig, (ax0, ax1, ax2) = plt.subplots(nrows=3, figsize=(8, 10))

    ax0.plot(angulo.universe, angulo['N'].mf, 'b', label='Inclinado Esquerda')
    ax0.plot(angulo.universe, angulo['Z'].mf, 'g', label='Vertical')
    ax0.plot(angulo.universe, angulo['P'].mf, 'r', label='Inclinado Direita')
    ax0.set_title('Ângulo')
    ax0.legend()

    ax1.plot(velocidade_angular.universe, velocidade_angular['N'].mf, 'b', label='Esquerda')
    ax1.plot(velocidade_angular.universe, velocidade_angular['Z'].mf, 'g', label='Parado')
    ax1.plot(velocidade_angular.universe, velocidade_angular['P'].mf, 'r', label='Direita')
    ax1.set_title('Velocidade Angular')
    ax1.legend()

    ax2.plot(empurrao_carro.universe, empurrao_carro['forte_esquerda'].mf, 'b', label='Forte Esquerda')
    ax2.plot(empurrao_carro.universe, empurrao_carro['leve_esquerda'].mf, 'g', label='Leve Esquerda')
    ax2.plot(empurrao_carro.universe, empurrao_carro['neutro'].mf, 'r', label='Neutro')
    ax2.plot(empurrao_carro.universe, empurrao_carro['leve_direita'].mf, 'c', label='Leve Direita')
    ax2.plot(empurrao_carro.universe, empurrao_carro['forte_direita'].mf, 'm', label='Forte Direita')
    ax2.set_title('Empurrão no Carro')
    ax2.legend()

    plt.tight_layout()
    plt.show()

# Chame esta função para visualizar os conjuntos
plot_memberships()

# Definindo as regras fuzzy
rule1 = ctrl.Rule(angulo['N'] & velocidade_angular['N'], empurrao_carro['forte_esquerda'])
rule2 = ctrl.Rule(angulo['N'] & velocidade_angular['Z'], empurrao_carro['leve_esquerda'])
rule3 = ctrl.Rule(angulo['N'] & velocidade_angular['P'], empurrao_carro['neutro'])
rule4 = ctrl.Rule(angulo['Z'] & velocidade_angular['N'], empurrao_carro['leve_esquerda'])
rule5 = ctrl.Rule(angulo['Z'] & velocidade_angular['Z'], empurrao_carro['neutro'])
rule6 = ctrl.Rule(angulo['Z'] & velocidade_angular['P'], empurrao_carro['leve_direita'])
rule7 = ctrl.Rule(angulo['P'] & velocidade_angular['N'], empurrao_carro['neutro'])
rule8 = ctrl.Rule(angulo['P'] & velocidade_angular['Z'], empurrao_carro['leve_direita'])
rule9 = ctrl.Rule(angulo['P'] & velocidade_angular['P'], empurrao_carro['forte_direita'])

# Configurando o sistema de controle FIS
pendulo_ctrl = ctrl.ControlSystem([rule1, rule2, rule3, rule4, rule5, rule6, rule7, rule8, rule9])
pendulo_simulacao = ctrl.ControlSystemSimulation(pendulo_ctrl)

# Testando o sistema com valores de exemplo
pendulo_simulacao.input['angulo'] = -3  # Exemplo de ângulo inclinado para a esquerda
pendulo_simulacao.input['velocidade_angular'] = -1  # Exemplo de velocidade angular

# Calculando a saída
pendulo_simulacao.compute()
print("Empurrão no carro:", pendulo_simulacao.output['empurrao_carro'])

# Visualizando a saída
empurrao_carro.view(sim=pendulo_simulacao)
plt.show()
