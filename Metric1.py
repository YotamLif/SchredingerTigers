from qiskit import execute, QuantumCircuit, QuantumRegister, ClassicalRegister
from qiskit.providers.aer import QasmSimulator
from qiskit.providers.aer.noise import NoiseModel
from qiskit.providers.aer.noise.errors import pauli_error, reset_error

from MeasureCompareBar import MeasureCompareBar
from circ_break import circ_break
from run_clean_model import plot_statevector, diff_vec
from noise_modeling import get_noise_prob_vector, make_noise_model
from run_true_comp import RunTrue
import numpy as np
import pickle
from noise_modeling import get_prob_vector

import matplotlib.pyplot as plt

print("Starting...")

# circuit init
qr = QuantumRegister(3)
cr = ClassicalRegister(3)
circuit = QuantumCircuit(qr, cr)

circuit.h(qr[0])
circuit.cx(qr[0], qr[1])
circuit.x(qr[1])
circuit.z(qr[2])
circuit.x(qr[2])
circuit.h(qr[2])
circuit.x(qr[2])
circuit.iden(qr[0])
circuit.iden(qr[1])
circuit.iden(qr[2])

err1 = pauli_error([('X', 0.2), ('I', 0.8)])
err2 = pauli_error([('X', 0.3), ('I', 0.7)])
err3 = reset_error(0.1)
# errors = [(err1, ['X', 'Z'], [0, 1, 2]), (err2, ['ID'], [0, 1, 2]), (err3, ['CX'], [0, 1, 2])]

noiseModel = NoiseModel()
noiseModel.add_quantum_error(err1, ['x'], [1])
noiseModel.add_quantum_error(err2, ['id'], [0])
noiseModel.add_quantum_error(err2, ['id'], [1])
noiseModel.add_quantum_error(err2, ['id'], [2])
noiseModel.add_quantum_error(err3, ['z'], [2])

dpt = range(0, circuit.depth())
diffCN = []
diffCR = []
diffNR = []
for lyr in dpt:
    if lyr == 0:
        diffCN.append(0)
        diffCR.append(0)
        diffNR.append(0)
        continue
    nCirc = circ_break(circuit, lyr)
    cleanVec = np.real(plot_statevector(nCirc))
    noiseVec = get_noise_prob_vector(nCirc, noiseModel)
    real_job = RunTrue(nCirc,
                       "79323d781b5f9aa51c83e04a522fdd8d3eeebeb7f21977bec8a64ce3bfb494d32c423e8cb7bc75a8eae679a97d498f3c69662fa2344fbcc8a751f2fd82e0ccb4")
    real_res = get_prob_vector(real_job.result().get_counts(), circuit) / 1024
    pickle.dump(real_res, open("real_res{}.p", "ab"))
    diffCN.append(diff_vec(cleanVec, noiseVec))
    diffCR.append(diff_vec(cleanVec, real_res))
    diffNR.append(diff_vec(noiseVec, real_res))
    MeasureCompareBar(real_res,noiseVec, cleanVec)

legend = ((diffCN, diffCR, diffNR), ('diffCN', 'diffCR', 'diffNR'))
plt.plot(dpt, diffCN)
plt.plot(dpt, diffCR)
plt.plot(dpt, diffNR)
plt.legend(legend)
plt.show()


pickle.dump(diffCN, open("diffCN.p", "wb"))
pickle.dump(diffCR, open("diffCR.p", "wb"))
pickle.dump(diffNR, open("diffNR.p", "wb"))
