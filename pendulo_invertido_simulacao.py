import matplotlib
matplotlib.use('Agg')

import numpy as np
import skfuzzy as fuzz
import skfuzzy.control as ctrl
import matplotlib.pyplot as plt 

class PenduloInvertido:
    def __init__(self):
        self.angulo = ctrl.Antecedent(np.arange(-180, 181, 1), 'angulo')
        self.velocidade_angular = ctrl.Antecedent(np.arange(-50, 51, 1), 'velocidade_angular')

        self.empurro_carro = ctrl.Consequent(np.arange(-10, 11, 1), 'empurrao_carro')

        self.angulo['negativo'] = fuzz.trimf(self.angulo.universe, [-180, -90, 0])
        self.angulo['zero'] = fuzz.trimf(self.angulo.universe, [-90, 0, 90])
        self.angulo['positivo'] = fuzz.trimf(self.angulo.universe, [0, 90, 180])

        self.velocidade_angular['negativa'] = fuzz.trimf(self.velocidade_angular.universe, [-50, -25, 0])
        self.velocidade_angular['zero'] = fuzz.trimf(self.velocidade_angular.universe, [-25, 0, 25])
        self.velocidade_angular['positiva'] = fuzz.trimf(self.velocidade_angular.universe, [0, 25, 50])

        self.empurro_carro['esquerda'] = fuzz.trimf(self.empurro_carro.universe, [-10, -5, 0])
        self.empurro_carro['zero'] = fuzz.trimf(self.empurro_carro.universe, [-5, 0, 5])
        self.empurro_carro['direita'] = fuzz.trimf(self.empurro_carro.universe, [0, 5, 10])

        self.regras = [
            ctrl.Rule(self.angulo['negativo'] & self.velocidade_angular['negativa'], self.empurro_carro['direita']),
            ctrl.Rule(self.angulo['negativo'] & self.velocidade_angular['zero'], self.empurro_carro['direita']),
            ctrl.Rule(self.angulo['negativo'] & self.velocidade_angular['positiva'], self.empurro_carro['direita']),
            ctrl.Rule(self.angulo['zero'] & self.velocidade_angular['negativa'], self.empurro_carro['esquerda']),
            ctrl.Rule(self.angulo['zero'] & self.velocidade_angular['zero'], self.empurro_carro['zero']),
            ctrl.Rule(self.angulo['zero'] & self.velocidade_angular['positiva'], self.empurro_carro['direita']),
            ctrl.Rule(self.angulo['positivo'] & self.velocidade_angular['negativa'], self.empurro_carro['esquerda']),
            ctrl.Rule(self.angulo['positivo'] & self.velocidade_angular['zero'], self.empurro_carro['esquerda']),
            ctrl.Rule(self.angulo['positivo'] & self.velocidade_angular['positiva'], self.empurro_carro['esquerda']),
        ]

        self.sistema_controle = ctrl.ControlSystem(self.regras)
        self.simulador = ctrl.ControlSystemSimulation(self.sistema_controle)

    def controlar_pendulo(self, angulo, velocidade_angular):
        self.simulador.input['angulo'] = angulo
        self.simulador.input['velocidade_angular'] = velocidade_angular
        self.simulador.compute()
        
        if 'empurrao_carro' in self.simulador.output:
            return self.simulador.output['empurrao_carro']
        else:
            return 0 

def simular_pendulo(tempo_total, intervalo):
    pendulo_simulacao = PenduloInvertido()

    angulo = 10
    velocidade_angular = 0 
    tempos = []
    angulos = []
    velocidades = []

    for t in np.arange(0, tempo_total, intervalo):
        empurro = pendulo_simulacao.controlar_pendulo(angulo, velocidade_angular)

        aceleração = empurro
        velocidade_angular += aceleração * intervalo
        angulo += velocidade_angular * intervalo

        tempos.append(t)
        angulos.append(angulo)
        velocidades.append(velocidade_angular)

        print(f"Tempo: {t:.2f}, Ângulo: {angulo:.2f}, Velocidade Angular: {velocidade_angular:.2f}, Empurrão: {empurro:.2f}")

    return tempos, angulos, velocidades

tempos, angulos, velocidades = simular_pendulo(10, 0.1)

plt.figure(figsize=(12, 6))

plt.subplot(2, 1, 1)
plt.plot(tempos, angulos, label='Ângulo do Pêndulo', color='b')
plt.title('Simulação do Pêndulo Invertido')
plt.ylabel('Ângulo (graus)')
plt.grid()
plt.legend()

plt.subplot(2, 1, 2)
plt.plot(tempos, velocidades, label='Velocidade Angular', color='r')
plt.xlabel('Tempo (s)')
plt.ylabel('Velocidade Angular (graus/s)')
plt.grid()
plt.legend()

plt.tight_layout()

plt.savefig('grafico_pendulo.png')  

plt.show() 