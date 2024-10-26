import numpy as np
import matplotlib.pyplot as plt

# Exemplo de função de pertinência para o ângulo
x = np.linspace(-90, 90, 100)
# Funções de pertinência para ângulo (modifique conforme necessário)
angle_left = np.maximum(0, (x + 90) / 90)
angle_vertical = np.maximum(0, 1 - np.abs(x) / 45)
angle_right = np.maximum(0, (90 - x) / 90)

plt.plot(x, angle_left, label="Inclinado à Esquerda (N)", color="blue")
plt.plot(x, angle_vertical, label="Vertical (Z)", color="green")
plt.plot(x, angle_right, label="Inclinado à Direita (P)", color="red")

plt.xlabel("Ângulo (graus)")
plt.ylabel("Grau de Pertinência")
plt.title("Funções de Pertinência para o Ângulo do Pêndulo")
plt.legend()
plt.grid(True)
plt.show()
