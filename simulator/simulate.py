import numpy as np
from scipy.linalg import expm

def simulate(H, times, psi0):
    """
    Time-evolve an initial quantum state under Hamiltonian H.

    Parameters
    ----------
    H : np.ndarray
        Hamiltonian matrix
    times : np.ndarray
        Time grid
    psi0 : np.ndarray
        Initial state vector

    Returns
    -------
    populations : np.ndarray
        Population of each basis state over time
    """

    n_states = len(psi0)
    populations = np.zeros((len(times), n_states))

    for i, t in enumerate(times):
        U = expm(-1j * H * t)
        psi_t = U @ psi0
        populations[i] = np.abs(psi_t) ** 2

    return populations
