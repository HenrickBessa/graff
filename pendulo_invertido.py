import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
import matplotlib.pyplot as plt

# Definindo variáveis fuzzy
def criar_sistema_fuzzy():
    angulo = ctrl.Antecedent(np.arange(-10, 11, 1), 'angulo')
    velocidade_angular = ctrl.Antecedent(np.arange(-5, 6, 1), 'velocidade_angular')
    empurrao_carro = ctrl.Consequent(np.arange(-10, 11, 1), 'empurrao_carro')

    # Funções de pertinência para ângulo
    angulo['Inclinado Esquerda'] = fuzz.trimf(angulo.universe, [-10, -5, 0]) 
    angulo['Vertical'] = fuzz.trimf(angulo.universe, [-1, 0, 1])  
    angulo['Inclinado Direita'] = fuzz.trimf(angulo.universe, [0, 5, 10])   

    # Funções de pertinência para velocidade angular
    velocidade_angular['Deslocando-se Esquerda'] = fuzz.trimf(velocidade_angular.universe, [-5, -2, 0])  
    velocidade_angular['Parado'] = fuzz.trimf(velocidade_angular.universe, [-1, 0, 1])   
    velocidade_angular['Deslocando-se Direita'] = fuzz.trimf(velocidade_angular.universe, [0, 2, 5])    

    # Funções de pertinência para empurrão no carro
    empurrao_carro['Forte Esquerda'] = fuzz.trimf(empurrao_carro.universe, [-10, -7, -3])
    empurrao_carro['Leve Esquerda'] = fuzz.trimf(empurrao_carro.universe, [-5, -3, 0])
    empurrao_carro['Neutro'] = fuzz.trimf(empurrao_carro.universe, [-1, 0, 1])
    empurrao_carro['Leve Direita'] = fuzz.trimf(empurrao_carro.universe, [0, 3, 5])
    empurrao_carro['Forte Direita'] = fuzz.trimf(empurrao_carro.universe, [3, 7, 10])

    # Regras fuzzy
    rule1 = ctrl.Rule(angulo['Inclinado Esquerda'] & velocidade_angular['Deslocando-se Esquerda'], empurrao_carro['Forte Esquerda'])
    rule2 = ctrl.Rule(angulo['Inclinado Esquerda'] & velocidade_angular['Parado'], empurrao_carro['Leve Esquerda'])
    rule3 = ctrl.Rule(angulo['Inclinado Esquerda'] & velocidade_angular['Deslocando-se Direita'], empurrao_carro['Neutro'])
    rule4 = ctrl.Rule(angulo['Vertical'] & velocidade_angular['Deslocando-se Esquerda'], empurrao_carro['Leve Esquerda'])
    rule5 = ctrl.Rule(angulo['Vertical'] & velocidade_angular['Parado'], empurrao_carro['Neutro'])
    rule6 = ctrl.Rule(angulo['Vertical'] & velocidade_angular['Deslocando-se Direita'], empurrao_carro['Leve Direita'])
    rule7 = ctrl.Rule(angulo['Inclinado Direita'] & velocidade_angular['Deslocando-se Esquerda'], empurrao_carro['Neutro'])
    rule8 = ctrl.Rule(angulo['Inclinado Direita'] & velocidade_angular['Parado'], empurrao_carro['Leve Direita'])
    rule9 = ctrl.Rule(angulo['Inclinado Direita'] & velocidade_angular['Deslocando-se Direita'], empurrao_carro['Forte Direita'])

    pendulo_ctrl = ctrl.ControlSystem([rule1, rule2, rule3, rule4, rule5, rule6, rule7, rule8, rule9])
    return pendulo_ctrl

# Função para plotar as funções de pertinência
def plot_memberships(angulo, velocidade_angular, empurrao_carro):
    fig, (ax0, ax1, ax2) = plt.subplots(nrows=3, figsize=(8, 10))

    ax0.plot(angulo.universe, angulo['Inclinado Esquerda'].mf, 'b', label='Inclinado Esquerda')
    ax0.plot(angulo.universe, angulo['Vertical'].mf, 'g', label='Vertical')
    ax0.plot(angulo.universe, angulo['Inclinado Direita'].mf, 'r', label='Inclinado Direita')
    ax0.set_title('Ângulo')
    ax0.legend()

    ax1.plot(velocidade_angular.universe, velocidade_angular['Deslocando-se Esquerda'].mf, 'b', label='Deslocando-se Esquerda')
    ax1.plot(velocidade_angular.universe, velocidade_angular['Parado'].mf, 'g', label='Parado')
    ax1.plot(velocidade_angular.universe, velocidade_angular['Deslocando-se Direita'].mf, 'r', label='Deslocando-se Direita')
    ax1.set_title('Velocidade Angular')
    ax1.legend()

    ax2.plot(empurrao_carro.universe, empurrao_carro['Forte Esquerda'].mf, 'b', label='Forte Esquerda')
    ax2.plot(empurrao_carro.universe, empurrao_carro['Leve Esquerda'].mf, 'g', label='Leve Esquerda')
    ax2.plot(empurrao_carro.universe, empurrao_carro['Neutro'].mf, 'r', label='Neutro')
    ax2.plot(empurrao_carro.universe, empurrao_carro['Leve Direita'].mf, 'c', label='Leve Direita')
    ax2.plot(empurrao_carro.universe, empurrao_carro['Forte Direita'].mf, 'm', label='Forte Direita')
    ax2.set_title('Empurrão no Carro')
    ax2.legend()

    plt.tight_layout()
    plt.savefig('membership_functions_combined.png') 
    plt.close()

# Função para simular o pêndulo
def simular_pendulo(tempo_total, dt):
    tempos = np.arange(0, tempo_total, dt)
    angulos = []
    velocidades = []

    angulo_atual = 0  # Ângulo inicial
    velocidade_atual = 0  # Velocidade angular inicial

    pendulo_ctrl = criar_sistema_fuzzy()
    pendulo_simulacao = ctrl.ControlSystemSimulation(pendulo_ctrl)

    for t in tempos:
        # Atualizar as entradas do sistema fuzzy
        pendulo_simulacao.input['angulo'] = angulo_atual
        pendulo_simulacao.input['velocidade_angular'] = velocidade_atual

        # Computar a saída do sistema fuzzy
        pendulo_simulacao.compute()
        empurro = pendulo_simulacao.output['empurrao_carro']

        # Atualizar os estados do pêndulo
        angulo_atual += velocidade_atual * dt
        velocidade_atual += empurro * dt  

        angulos.append(angulo_atual)
        velocidades.append(velocidade_atual)

    return tempos, angulos, velocidades

# Simular o pêndulo
tempos, angulos, velocidades = simular_pendulo(10, 0.1)

# Plotar resultados
plt.figure(figsize=(10, 5))
plt.subplot(2, 1, 1)
plt.plot(tempos, angulos, label='Ângulo do Pêndulo')
plt.title('Simulação do Pêndulo Invertido')
plt.ylabel('Ângulo (graus)')
plt.legend()

plt.subplot(2, 1, 2)
plt.plot(tempos, velocidades, label='Velocidade Angular', color='orange')
plt.ylabel('Velocidade Angular (graus/s)')
plt.xlabel('Tempo (s)')
plt.legend()

plt.tight_layout()
plt.savefig('simulacao_pendulo.png')
plt.show()

# Plotar funções de pertinência
plot_memberships(ctrl.Antecedent(np.arange(-10, 11, 1), 'angulo'),
                 ctrl.Antecedent(np.arange(-5, 6, 1), 'velocidade_angular'),
                 ctrl.Consequent(np.arange(-10, 11, 1), 'empurrao_carro'))
