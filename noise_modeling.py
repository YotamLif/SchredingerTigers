import numpy as np
from qiskit import execute, QuantumCircuit, ClassicalRegister, Aer, QuantumRegister
from qiskit.providers.aer.noise import NoiseModel
from qiskit.providers.aer.noise.errors import pauli_error
from qiskit.providers.aer.noise.errors import QuantumError
from qiskit.qobj import qobj, QasmQobj, QasmQobjConfig
from typing import List, Tuple, Dict
from math import pow
from run_clean_model import add_measurements


def make_expanded_error(quantum_error: QuantumError, gate_types_to_apply_error: List[str],
                        qregs_to_apply_error: List[int]):
    return quantum_error, gate_types_to_apply_error, qregs_to_apply_error


def make_expanded_error_list(quantum_error_list: List[QuantumError], gate_types_to_apply_error_list: List[List[str]],
                             qregs_to_apply_error_list: List[List[int]]):
    assert len(quantum_error_list) == len(gate_types_to_apply_error_list) and len(quantum_error_list) == len(
        qregs_to_apply_error_list)
    error_list = []
    for error, gates, qregs in quantum_error_list, gate_types_to_apply_error_list, qregs_to_apply_error_list:
        error_list.append((error, gates, qregs))
    return error_list


def make_noise_model(expanded_errors: List[Tuple[QuantumError, List[str], List[int]]]) -> NoiseModel:
    noise_model = NoiseModel()
    for error in expanded_errors:
        q_error, instruction, qbits = error
        noise_model.add_quantum_error(q_error, instruction, qbits)
    return noise_model


def apply_noise_model(noise_model: NoiseModel, circuit: QuantumCircuit, shots=1024, backend='qasm_simulator'):
    backend = Aer.get_backend(backend)
    add_measurements(circuit)
    res = execute(circuit, backend, noise_model=noise_model, shots=shots).result()
    return res


def apply_model(circuit: QuantumCircuit, n_shots=1024, backend='qasm_simulator'):
    backend = Aer.get_backend(backend)
    add_measurements(circuit)
    res = execute(circuit, backend, shots=n_shots).result()
    return res


def get_prob_vector(result: Dict, circuit: QuantumCircuit):
    num_reg = circuit.qregs[0].size
    vec_length = int(pow(2, num_reg))
    prob_vector = np.zeros(vec_length)
    for i in range(vec_length):
        index = int('{0:b}'.format(i).zfill(num_reg), 2)
        try:
            value = result[bin(i)[2:].zfill(num_reg)]
        except:
            continue
        prob_vector[index] = value
    return prob_vector


def get_difference(noise_model: NoiseModel, circuit: QuantumCircuit, n_shots=1024, backend='qasm_simulator'):
    res_noise = apply_noise_model(noise_model, circuit, n_shots, backend).get_counts()
    res_no_noise = apply_model(circuit, n_shots, backend).get_counts()
    print(res_no_noise)
    print(res_noise)
    return (get_prob_vector(res_noise, circuit) - get_prob_vector(res_no_noise, circuit)) / n_shots


def get_noise_prob_vector(circuit: QuantumCircuit, noise_model: NoiseModel, n_shots=1024, backend='qasm_simulator'):
    res_noise = apply_noise_model(noise_model, circuit, n_shots, backend).get_counts()
    return get_prob_vector(res_noise, circuit) / n_shots


def test():
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

    difference = get_difference(noise_model, circle)
    print(difference)


if __name__ == '__main__':
    test()
