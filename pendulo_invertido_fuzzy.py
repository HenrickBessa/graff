import numpy as np
import skfuzzy as fuzz
import skfuzzy.control as ctrl

class PenduloInvertido:
    def __init__(self):
        self.angulo = ctrl.Antecedent(np.arange(-0.15, 0.16, 0.01), 'angulo')
        self.angulo['N'] = fuzz.trapmf(self.angulo.universe, [-0.15, -0.15, -0.1, 0])
        self.angulo['Z'] = fuzz.trapmf(self.angulo.universe, [-0.1, -0.03, 0.03, 0.1])
        self.angulo['P'] = fuzz.trapmf(self.angulo.universe, [0, 0.1, 0.15, 0.15])

        self.velocidade_angular = ctrl.Antecedent(np.arange(-0.15, 0.16, 0.01), 'velocidade_angular')
        self.velocidade_angular['N'] = fuzz.trapmf(self.velocidade_angular.universe, [-0.15, -0.15, -0.1, 0])
        self.velocidade_angular['Z'] = fuzz.trapmf(self.velocidade_angular.universe, [-0.15, -0.03, 0.03, 0.15])
        self.velocidade_angular['P'] = fuzz.trapmf(self.velocidade_angular.universe, [0, 0.1, 0.15, 0.15])

        self.empurro_carro = ctrl.Consequent(np.arange(-200, 201, 1), 'empurrao_carro')
        self.empurro_carro['NL'] = fuzz.trimf(self.empurro_carro.universe, [-200, -100, 0])
        self.empurro_carro['NM'] = fuzz.trimf(self.empurro_carro.universe, [-80, -40, 0])
        self.empurro_carro['NS'] = fuzz.trimf(self.empurro_carro.universe, [-10, -5, 0])
        self.empurro_carro['Z'] = fuzz.trimf(self.empurro_carro.universe, [0, 0, 0])
        self.empurro_carro['PS'] = fuzz.trimf(self.empurro_carro.universe, [0, 5, 10])
        self.empurro_carro['PM'] = fuzz.trimf(self.empurro_carro.universe, [0, 40, 80])
        self.empurro_carro['PL'] = fuzz.trimf(self.empurro_carro.universe, [0, 100, 200])

        self.regras = [
            ctrl.Rule(self.angulo['N'] & self.velocidade_angular['N'], self.empurro_carro['NL']),
            ctrl.Rule(self.angulo['N'] & self.velocidade_angular['Z'], self.empurro_carro['NM']),
            ctrl.Rule(self.angulo['N'] & self.velocidade_angular['P'], self.empurro_carro['Z']),
            ctrl.Rule(self.angulo['Z'] & self.velocidade_angular['N'], self.empurro_carro['NS']),
            ctrl.Rule(self.angulo['Z'] & self.velocidade_angular['Z'], self.empurro_carro['Z']),
            ctrl.Rule(self.angulo['Z'] & self.velocidade_angular['P'], self.empurro_carro['PS']),
            ctrl.Rule(self.angulo['P'] & self.velocidade_angular['N'], self.empurro_carro['Z']),
            ctrl.Rule(self.angulo['P'] & self.velocidade_angular['Z'], self.empurro_carro['PM']),
            ctrl.Rule(self.angulo['P'] & self.velocidade_angular['P'], self.empurro_carro['PL']),
        ]

        self.sistema_controle = ctrl.ControlSystem(self.regras)
        self.simulador = ctrl.ControlSystemSimulation(self.sistema_controle)

    def simular(self, angulo_inicial, velocidade_angular_inicial):
        self.simulador.input['angulo'] = angulo_inicial
        self.simulador.input['velocidade_angular'] = velocidade_angular_inicial
        self.simulador.compute()
        return self.simulador.output['empurrao_carro']

pendulo = PenduloInvertido()
valores_angulo = np.linspace(-0.15, 0.15, 10)
valores_velocidade = np.linspace(-0.15, 0.15, 10)

for angulo in valores_angulo:
    for velocidade in valores_velocidade:
        empurro = pendulo.simular(angulo, velocidade)
        print(f"Ângulo: {angulo:.2f}, Velocidade Angular: {velocidade:.2f}, Empurro no Carro: {empurro:.2f}")
