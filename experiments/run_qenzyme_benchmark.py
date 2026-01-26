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

times = np.linspace(0, 10, 300)

qenzymes = {
    "Highly efficient": QEnzyme(
        tunneling_strength=1.4,
        product_stabilization=1.8,
        ts_stabilization=0.7,
        environment_perturbation=0.1
    ),
    "Moderate": QEnzyme(
        tunneling_strength=1.0,
        product_stabilization=1.0,
        ts_stabilization=0.3,
        environment_perturbation=0.1
    ),
    "Weak": QEnzyme(
        tunneling_strength=0.8,
        product_stabilization=0.4,
        ts_stabilization=0.0,
        environment_perturbation=0.2
    ),
    "Inhibited": QEnzyme(
        tunneling_strength=0.7,
        product_stabilization=0.2,
        ts_stabilization=-0.3,
        environment_perturbation=0.3
    ),
}

results = {}

for name, enzyme in qenzymes.items():
    H = enzyme.hamiltonian()
    pop = simulate(H, psi0, times)
    results[name] = pop

efficiency = {
    name: pop[-1, 3]   # final product population
    for name, pop in results.items()
}

best = max(efficiency, key=efficiency.get)
worst = min(efficiency, key=efficiency.get)

plt.figure(figsize=(9, 5))

for name, pop in results.items():
    style = "-" if name == best else "--" if name == worst else ":"
    width = 2.5 if name in (best, worst) else 1.5

    plt.plot(
        times,
        pop[:, 3],
        linestyle=style,
        linewidth=width,
        label=f"{name} (final = {efficiency[name]:.2f})"
    )

plt.xlabel("Time")
plt.ylabel("Product population |3⟩")
plt.title(
    "Benchmarking Q-Enzymes by Quantum Reaction Efficiency\n"
    f"Best: {best} | Worst: {worst}"
)
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()
