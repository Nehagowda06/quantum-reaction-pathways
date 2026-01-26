import numpy as np
from scipy.linalg import expm
import matplotlib.pyplot as plt

def build_hamiltonian(tunnel=1.0, bias=0.0):
    """
    tunnel : controls tunneling strength (barrier height)
    bias   : controls energetic preference for product
    """
    H_kin = np.array([
        [0, -tunnel, 0, 0],
        [-tunnel, 0, -tunnel, 0],
        [0, -tunnel, 0, -tunnel],
        [0, 0, -tunnel, 0]
    ])
    V = np.diag([
        0.0,          # reactant
        2.0,          # barrier left
        2.0 - bias,   # barrier right
        -bias         # product stabilized
    ])

    return H_kin + V

H = build_hamiltonian(
    tunnel=0.5,   # try 0.5 or 2.0 later
    bias=0.0      # 0.0 = symmetric, >0 = catalytic bias
)

psi0 = np.zeros(4, dtype=complex)
psi0[0] = 1.0

times = np.linspace(0, 10, 200)
populations = []

for t in times:
    U = expm(-1j * H * t)
    psi_t = U @ psi0
    populations.append(np.abs(psi_t)**2)

populations = np.array(populations)

plt.figure(figsize=(8, 5))
for i in range(4):
    plt.plot(times, populations[:, i], label=f"State |{i}⟩")

plt.xlabel("Time")
plt.ylabel("Population")
plt.title("Parameterized Quantum Reaction Pathway")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()
