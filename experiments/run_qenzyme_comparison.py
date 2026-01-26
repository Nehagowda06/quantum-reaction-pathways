import numpy as np
import matplotlib.pyplot as plt
from scipy.linalg import expm

from hamiltonians.qenzyme import QEnzyme

def simulate(H, psi0, times):
    populations = []
    for t in times:
        U = expm(-1j * H * t)
        psi_t = U @ psi0
        populations.append(np.abs(psi_t)**2)
    return np.array(populations)

psi0 = np.zeros(4, dtype=complex)
psi0[0] = 1.0  # Reactant |0⟩

times = np.linspace(0, 10, 200)

enzyme_A = QEnzyme(
    tunneling_strength=1.3,      # strong barrier lowering
    product_stabilization=1.6,   # strong catalytic bias
    ts_stabilization=0.6,        # TS stabilization
    environment_perturbation=0.1
)

H_A = enzyme_A.hamiltonian()
pop_A = simulate(H_A, psi0, times)

enzyme_B = QEnzyme(
    tunneling_strength=0.8,      # weaker tunneling
    product_stabilization=0.4,   # weak bias
    ts_stabilization=0.0,        # no TS stabilization
    environment_perturbation=0.2
)

H_B = enzyme_B.hamiltonian()
pop_B = simulate(H_B, psi0, times)

plt.figure(figsize=(8, 5))

plt.plot(
    times,
    pop_A[:, 3],
    label="Product |3⟩ — Q-Enzyme A (efficient)",
    linewidth=2
)

plt.plot(
    times,
    pop_B[:, 3],
    label="Product |3⟩ — Q-Enzyme B (weak)",
    linestyle="--",
    linewidth=2
)

plt.xlabel("Time")
plt.ylabel("Product population")
plt.title("Comparison of Q-Enzyme Reaction Pathways")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()
