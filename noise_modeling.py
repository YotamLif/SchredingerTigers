import numpy as np
from qiskit import execute, QuantumCircuit, ClassicalRegister, Aer, QuantumRegister
from qiskit.providers.aer.noise import NoiseModel
from qiskit.providers.aer.noise.errors import pauli_error
from qiskit.providers.aer.noise.errors import QuantumError
from qiskit.qobj import qobj, QasmQobj, QasmQobjConfig
from typing import List, Tuple


def make_noise_model(errors: List[Tuple[QuantumError, List[str], List[int]]]):
    noise_model = NoiseModel()
    for error in errors:
        q_error, instruction, qbits = error
        noise_model.add_quantum_error(q_error, instruction, qbits)
    return noise_model


def apply_noise_model(noise_model: NoiseModel, circuit: QuantumCircuit, shots=1024, backend='qasm_simulator'):
    backend = Aer.get_backend(backend)
    res = execute(circuit, backend, noise_model=noise_model, shots=shots).result()
    return res


def main():
    err1 = pauli_error([('X', 0.2), ('I', 0.8)])
    err2 = pauli_error([('X', 0.3), ('I', 0.7)])
    errors = [(err1, ['x'], [1]), (err2, ['id'], [1])]
    noise_model = make_noise_model(errors)
    qr = QuantumRegister(3)
    cr = ClassicalRegister(3)
    circle = QuantumCircuit(qr, cr)
    circle.iden(qr[0])
    circle.iden(qr[1])
    circle.x(qr[1])
    circle.measure(qr, cr)

    print(apply_noise_model(noise_model, circle).get_counts())


if __name__ == '__main__':
    main()
