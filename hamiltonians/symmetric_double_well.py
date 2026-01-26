import numpy as np
from scipy.linalg import expm
import matplotlib.pyplot as plt
N = 4
t = 1.0
V = np.diag([0.0, 2.0, 2.0, 0.0])
H_kin = np.array([
    [0, -t,  0,  0],
    [-t, 0, -t,  0],
    [0, -t,  0, -t],
    [0,  0, -t,  0]
])
H = H_kin + V
psi0 = np.zeros(N, dtype=complex)
psi0[0] = 1.0  # start in left well
times = np.linspace(0, 10, 200)
populations = []

for t in times:
    U = expm(-1j * H * t)
    psi_t = U @ psi0
    populations.append(np.abs(psi_t)**2)

populations = np.array(populations)
plt.figure(figsize=(8, 5))
for i in range(N):
    plt.plot(times, populations[:, i], label=f"State |{i}⟩")

plt.xlabel("Time")
plt.ylabel("Population")
plt.title("Symmetric Quantum Reaction Pathway (Tunneling)")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()
