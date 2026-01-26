import numpy as np
import matplotlib.pyplot as plt
from scipy.linalg import expm

from hamiltonians.qenzyme import QEnzyme

enzyme = QEnzyme(
    tunneling_strength=1.2,
    product_stabilization=1.5,
    ts_stabilization=0.5,
    environment_perturbation=0.1
)

enzyme.inhibit(strength=0.6)   # simulate inhibitor binding

H = enzyme.hamiltonian()

psi0 = np.zeros(4, dtype=complex)
psi0[0] = 1.0  # reactant

times = np.linspace(0, 10, 200)
populations = []

for t in times:
    U = expm(-1j * H * t)
    psi_t = U @ psi0
    populations.append(np.abs(psi_t)**2)

populations = np.array(populations)

state_labels = {
    0: "Reactant (|0⟩)",
    1: "Transition region (left) (|1⟩)",
    2: "Transition region (right) (|2⟩)",
    3: "Product (|3⟩)"
}

plt.figure(figsize=(8, 5))

for i in range(4):
    plt.plot(times, populations[:, i], label=state_labels[i])

plt.xlabel("Time")
plt.ylabel("Population")
plt.title("Q-Enzyme Reaction Pathway with Inhibition")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()
