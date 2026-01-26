import numpy as np
from scipy.linalg import expm


class QEnzyme:
    """
    Quantum-effective enzyme model.

    Translates chemically evolved enzymatic constraints into an
    effective Hamiltonian acting on a quantum reaction coordinate.
    """

    def __init__(
        self,
        tunneling=None,
        tunneling_strength=None,
        bias=None,
        product_bias=None,
        product_stabilization=None,
        ts_stabilization=0.0,
        environment=None,
        environment_perturbation=None,
    ):
        self.tunnel = (
            tunneling_strength
            if tunneling_strength is not None
            else tunneling if tunneling is not None else 1.0
        )
        self.bias = (
            product_stabilization
            if product_stabilization is not None
            else product_bias
            if product_bias is not None
            else bias if bias is not None else 0.0
        )
        self.env = (
            environment_perturbation
            if environment_perturbation is not None
            else environment if environment is not None else 0.0
        )
        self.ts = ts_stabilization

        self._H = None
    def kinetic_term(self):
        t = self.tunnel
        return np.array([
            [0, -t,  0,  0],
            [-t, 0, -t,  0],
            [0, -t,  0, -t],
            [0,  0, -t,  0],
        ])

    def potential_term(self):
        return np.diag([
            0.0,
            2.0 - self.ts,
            2.0 - self.ts,
            -self.bias,
        ])

    def environment_term(self):
        return self.env * np.diag([0.0, 1.0, 1.0, 0.0])
    def mutate(self, delta_bias=0.0, delta_ts=0.0):
        self.bias += delta_bias
        self.ts += delta_ts
        self._H = None

    def inhibit(self, strength):
        self.ts -= strength
        self._H = None
    def hamiltonian(self):
        if self._H is None:
            self._H = (
                self.kinetic_term()
                + self.potential_term()
                + self.environment_term()
            )
        return self._H

    def simulate(self, times):
        H = self.hamiltonian()
        psi0 = np.array([1, 0, 0, 0], dtype=complex)

        populations = []
        for t in times:
            U = expm(-1j * H * t)
            psi_t = U @ psi0
            populations.append(np.abs(psi_t) ** 2)

        return np.array(populations)
    def summary(self):
        return {
            "tunneling": self.tunnel,
            "product_bias": self.bias,
            "ts_stabilization": self.ts,
            "environment": self.env,
        }
