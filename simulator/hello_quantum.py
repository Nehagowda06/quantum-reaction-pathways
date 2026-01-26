from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector
qc = QuantumCircuit(2)
qc.h(0)
qc.cx(0, 1)

print("Quantum Circuit:")
print(qc)
state = Statevector.from_instruction(qc)

print("\nQuantum Statevector:")
print(state)

print("\nMeasurement probabilities:")
print(state.probabilities_dict())
