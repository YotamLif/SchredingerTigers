import numpy as np
from qiskit import execute, QuantumCircuit, ClassicalRegister, Aer, QuantumRegister
from qiskit.providers.aer.noise import NoiseModel
from qiskit.providers.aer.noise.errors import pauli_error
from qiskit.providers.aer.noise.errors import QuantumError
from qiskit.qobj import qobj, QasmQobj, QasmQobjConfig
from typing import List


def make_noise_model(errors: List[(QuantumError, List[str], List[int])]):
    noise = NoiseModel()
    for error in errors:
        q_error, instruction, qbits = error
        noise.add_quantum_error(q_error, instruction, qbits)


def apply_noise_model(num_qbits: int, noise_model: NoiseModel, layers: QasmQobj, shots=1024):
    backend = Aer.get_backend('qasm_simulator')

    qr = QuantumRegister(num_qbits)
    cr = ClassicalRegister(num_qbits)
    circle = QuantumCircuit(qr, cr)

    for experiment in layers.experiments:
        circle.append(experiment)

    # circle.x(qr[0])
    circle.measure(qr, cr)

    # error = pauli_error([('X', 0.2), ('I', 0.8)])

    res = execute(circle, backend, noise_model=noise_model, shots=shots).result()
    return res
