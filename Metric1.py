from qiskit import execute, QuantumCircuit, QuantumRegister, ClassicalRegister
from qiskit.providers.aer import QasmSimulator
from qiskit.providers.aer.noise import NoiseModel
from qiskit.providers.aer.noise.errors import pauli_error, reset_error

from circ_break import circ_break
from run_clean_model import plot_statevector, diff_vec
from noise_modeling import get_noise_prob_vector, make_noise_model
from run_true_comp import RunTrue

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
errors = [(err1, ['X', 'Z'], [0, 1, 2]), (err2, ['ID'], [0, 1, 2]), (err3, ['CX'], [0, 1, 2])]
noiseModel = (make_noise_model(errors))



dpt = range(1,circuit.depth())
diffCN = []
diffCR = []
diffNR = []
for lyr in dpt:
    nCirc = circ_break(circuit, lyr)
    cleanVec = plot_statevector(nCirc)
    noiseVec = get_noise_prob_vector(nCirc, noiseModel)
    # realVec = RunTrue(nCirc,"9c4474dc9592228326651bd77bae7df998ffb5def6296d85789635df576a6b6004b19ba14b41224c0b60ce99bbb340c838f14ffb25af037c980ede48eef2d6e5")
    diffCN.append(diff_vec(cleanVec, noiseVec))
    #diffCR.append(diff_vec(cleanVec, realVec))
    #diffNR.append(diff_vec(noiseVec, realVec))

plt.plot(dpt, diffCN, diffCR, diffNR)








