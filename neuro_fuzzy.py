import numpy as np
import skfuzzy as fuzz
import skfuzzy.control as ctrl
from sklearn.neural_network import MLPRegressor
import matplotlib.pyplot as plt

class SistemaNeuroFuzzy:
    def __init__(self):
        self.angulo = ctrl.Antecedent(np.arange(-10, 11, 1), 'angulo')
        self.velocidade_angular = ctrl.Antecedent(np.arange(-5, 6, 1), 'velocidade_angular')
        self.empurro_carro = ctrl.Consequent(np.arange(-10, 11, 1), 'empurro_carro')

        self.angulo['Inclinado Esquerda'] = fuzz.trimf(self.angulo.universe, [-10, -5, 0])
        self.angulo['Vertical'] = fuzz.trimf(self.angulo.universe, [-1, 0, 1])
        self.angulo['Inclinado Direita'] = fuzz.trimf(self.angulo.universe, [0, 5, 10])

        self.velocidade_angular['Deslocando-se Esquerda'] = fuzz.trimf(self.velocidade_angular.universe, [-5, -2, 0])
        self.velocidade_angular['Parado'] = fuzz.trimf(self.velocidade_angular.universe, [-1, 0, 1])
        self.velocidade_angular['Deslocando-se Direita'] = fuzz.trimf(self.velocidade_angular.universe, [0, 2, 5])

        self.empurro_carro['Forte Esquerda'] = fuzz.trimf(self.empurro_carro.universe, [-10, -7, -3])
        self.empurro_carro['Leve Esquerda'] = fuzz.trimf(self.empurro_carro.universe, [-5, -3, 0])
        self.empurro_carro['Neutro'] = fuzz.trimf(self.empurro_carro.universe, [-1, 0, 1])
        self.empurro_carro['Leve Direita'] = fuzz.trimf(self.empurro_carro.universe, [0, 3, 5])
        self.empurro_carro['Forte Direita'] = fuzz.trimf(self.empurro_carro.universe, [3, 7, 10])

        self.regras = [
            ctrl.Rule(self.angulo['Inclinado Esquerda'] & self.velocidade_angular['Deslocando-se Esquerda'], self.empurro_carro['Forte Direita']),
            ctrl.Rule(self.angulo['Vertical'] & self.velocidade_angular['Parado'], self.empurro_carro['Neutro']),
            ctrl.Rule(self.angulo['Inclinado Direita'] & self.velocidade_angular['Deslocando-se Direita'], self.empurro_carro['Forte Esquerda'])
        ]

        self.sistema_controle = ctrl.ControlSystem(self.regras)
        self.simulador = ctrl.ControlSystemSimulation(self.sistema_controle)

        self.ml_model = MLPRegressor(hidden_layer_sizes=(10,), max_iter=1000)

    def simular(self, angulo, velocidade_angular):
        self.simulador.input['angulo'] = angulo
        self.simulador.input['velocidade_angular'] = velocidade_angular
        self.simulador.compute()
        return self.simulador.output['empurro_carro'] if 'empurro_carro' in self.simulador.output else None

    def treinar(self, dados):
        X = dados[:, :2]
        y = dados[:, 2]
        self.ml_model.fit(X, y)

    def prever(self, angulos, velocidades):
        return self.ml_model.predict(np.array(list(zip(angulos, velocidades))))

    def plotar_saida(self, angulo, velocidade_angular):
        saida = self.simular(angulo, velocidade_angular)
        plt.figure()
        plt.title("Saída do Sistema Neuro-Fuzzy")
        plt.bar(['Empurro Carro'], [saida], color='blue')
        plt.ylim([-10, 10])
        plt.ylabel('Saída')
        plt.axhline(0, color='gray', linewidth=0.8)
        plt.grid()
        plt.savefig("saida_neuro_fuzzy.png")
        plt.close()

if __name__ == "__main__":
    sistema = SistemaNeuroFuzzy()

    dados_treinamento = np.array([
        [9, 4, 5],
        [10, 5, 7],
    ])

    sistema.treinar(dados_treinamento)

    X_test = np.array([[9, 4], [10, 5]])
    print("Shape of X_test:", X_test.shape)

    previsao = sistema.prever(X_test[:, 0], X_test[:, 1])
    print(f"Previsão: {previsao}")

    sistema.plotar_saida(9, 4)
    print("A saída foi salva como 'saida_neuro_fuzzy.png'.")
