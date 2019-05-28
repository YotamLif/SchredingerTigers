#!/usr/bin/env python
# coding: utf-8

# In[208]:


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


# In[ ]:


# ------------- Mains ---------------- #


# In[370]:


# initialize input circuit
num_qbits=2; num_cbits=1;
qr_in= QuantumRegister(num_qbits, 'qr')
cr_in = ClassicalRegister(num_cbits, 'cr')
circ_in = QuantumCircuit(qr_in, cr_in)

# add gates to input circuit
circ_in.h(qr_in[0])
# circ_in.cx(qr_in[0], qr_in[1])


# In[359]:


# print circuit and sub-circuit
num_gates=1;
circ_out=sub_circuit(circ_in,num_gates);
print(circ_in.draw())
print(circ_out.draw())


# In[371]:


# get state_vector from circuit
print(circ_in.draw())
statevector=plot_statevector(circ_in)
print(statevector)
plot_state_city(statevector, title='state vector')


# In[ ]:


# ------------- functions ------------ #


# In[333]:


# get state_vector from circuit
def plot_statevector(circ):
    simulator = Aer.get_backend('statevector_simulator')
    result=execute(circ,simulator).result()
    statevector = result.get_statevector(circ)
    statevector=statevector**2;
    # plot_state_city(statevector, title='state vector')
    return statevector;


# In[332]:


# add measurements at the end of the circle
def Add_Measurements(circ):
    circ.measure(circ.qregs[0],circ.cregs[0])
    return circ;


# In[352]:


def sub_circuit(circ_in,num_gates):
    # initialize output circuit
    qr_out = QuantumRegister(circ_in.qregs[0].size, 'qr')
    cr_out = ClassicalRegister(circ_in.cregs[0].size, 'cr')
    circ_out = QuantumCircuit(qr_out, cr_out)

    for i in range(0,num_gates):
        circ_out.append(circ_in.data[i][0],circ_in.data[i][1])
        
    return circ_out;


# In[381]:


def diff_vec(vec1,vec2):
    diff_vec=vec1-vec2;
    return diff_vec;

def all_diff(vec1,vec2,vec3):
    diff_vec12=abs(vec1-vec2);
    diff_vec13=abs(vec1-vec3);
    diff_vec23=abs(vec2-vec3);
    return vec1,vec2,vec3;

vec1=np.array([1,0,0]); 
vec2=np.array([0,5,0]);
vec3=np.array([0,0,1]);
print(diff_vec(vec1,vec2))


# In[ ]:


# --------------- future ideas ------------------ #


# In[ ]:


# Goal: different initial state vector

# Construct an empty quantum circuit
qr = QuantumRegister(2)
cr = ClassicalRegister(2)
circ = QuantumCircuit(qr, cr)
# circ.measure(qr, cr)

# Set the initial state
opts = {"initial_statevector": np.array([1, 0, 0, 1] / np.sqrt(2))}

# Select the QasmSimulator from the Aer provider
simulator = Aer.get_backend('statevector_simulator')

# Execute and get counts
result = execute(circ, simulator, backend_options=opts).result()
counts = result.get_counts(circ)
plot_histogram(counts, title="Bell initial statevector")


# In[ ]:


# Goal: snapshot a bell state in the middle of circuit"""

# it builds circuit and snap at the right time
qr = QuantumRegister(2)
cr = ClassicalRegister(2)
circuit = QuantumCircuit(qr, cr)
circuit.h(qr[0])
circuit.snapshot('1')
circuit.cx(qr[0], qr[1])
circuit.snapshot('2')
circuit.cx(qr[0], qr[1])
circuit.h(qr[1])

sim = Aer.get_backend('statevector_simulator')
result = execute(circuit, sim).result()
# TODO: rely on Result.get_statevector() postprocessing rather than manual
snap1 = result.data(0)['snapshots']['statevector']['1']
snap2=result.data(0)['snapshots']['statevector']['2']
snapshot = format_statevector(snapshots[0])

print(snap1)
print(snap2)

