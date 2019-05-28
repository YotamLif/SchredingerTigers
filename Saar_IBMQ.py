import numpy as np
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
from qiskit import Aer, execute
from qiskit.tools.visualization import plot_state_city
from qiskit import compile
from qiskit.tools.visualization import plot_histogram

import qiskit.extensions.simulator

from qiskit.providers.aer import StatevectorSimulator
from qiskit.providers.aer import QasmSimulator

from qiskit.circuit import CompositeGate
from qiskit.circuit import Instruction
from qiskit.extensions.exceptions import ExtensionError


# ------------- functions ------------ #

# get state_vector from circuit
def plot_statevector(circ):
    simulator = Aer.get_backend('statevector_simulator')
    result=execute(circ,simulator).result()
    statevector = result.get_statevector(circ)
    statevector=statevector**2;
    # plot_state_city(statevector, title='state vector')
    return statevector;

# add measurements at the end of the circle
def Add_Measurements(circ):
    circ.measure(circ.qregs[0],circ.cregs[0])
    return circ;


# get sub-circuit
def sub_circuit(circ_in,num_gates):
    # initialize output circuit
    qr_out = QuantumRegister(circ_in.qregs[0].size, 'qr')
    cr_out = ClassicalRegister(circ_in.cregs[0].size, 'cr')
    circ_out = QuantumCircuit(qr_out, cr_out)

    for i in range(0,num_gates):
        circ_out.append(circ_in.data[i][0],circ_in.data[i][1])
        
    return circ_out;

# gives difference of two vectors
def diff_vec(vec1,vec2):
    diff_vec=vec1-vec2;
    return diff_vec;

# gives all three differences
def all_diff(vec1,vec2,vec3):
    diff_vec12=abs(vec1-vec2);
    diff_vec13=abs(vec1-vec3);
    diff_vec23=abs(vec2-vec3);
    return vec1,vec2,vec3;
