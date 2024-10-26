import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl

# Definindo as variáveis fuzzy de entrada
angulo = ctrl.Antecedent(np.arange(-10, 11, 1), 'angulo')
velocidade_angular = ctrl.Antecedent(np.arange(-5, 6, 1), 'velocidade_angular')

# Variável de saída
empurrao_carro = ctrl.Consequent(np.arange(-10, 11, 1), 'empurrao_carro')

# Definindo conjuntos de pertinência
angulo['N'] = fuzz.trimf(angulo.universe, [-10, -5, 0])
angulo['Z'] = fuzz.trimf(angulo.universe, [-1, 0, 1])
angulo['P'] = fuzz.trimf(angulo.universe, [0, 5, 10])

velocidade_angular['N'] = fuzz.trimf(velocidade_angular.universe, [-5, -2, 0])
velocidade_angular['Z'] = fuzz.trimf(velocidade_angular.universe, [-1, 0, 1])
velocidade_angular['P'] = fuzz.trimf(velocidade_angular.universe, [0, 2, 5])

empurrao_carro['forte_esquerda'] = fuzz.trimf(empurrao_carro.universe, [-10, -7, -3])
empurrao_carro['leve_esquerda'] = fuzz.trimf(empurrao_carro.universe, [-5, -3, 0])
empurrao_carro['neutro'] = fuzz.trimf(empurrao_carro.universe, [-1, 0, 1])
empurrao_carro['leve_direita'] = fuzz.trimf(empurrao_carro.universe, [0, 3, 5])
empurrao_carro['forte_direita'] = fuzz.trimf(empurrao_carro.universe, [3, 7, 10])
