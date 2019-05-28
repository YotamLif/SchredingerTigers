def CircBreak(circ,max_layer):
    new_qr = qiskit.QuantumRegister(circ.qregs[0].size, circ.qregs[0].name)
    new_cr = qiskit.ClassicalRegister(circ.cregs[0].size, circ.cregs[0].name)
    new_circ = qiskit.QuantumCircuit(new_qr, new_cr)

    qubit_layers = [0]*new_qr.size
    gate_layers = []
    
    for gate in circ.data:
    
        current_qubits = [register[1] for register in gate[1]]
        current_layers = [qubit_layers[q] for q in current_qubits]
        gate_layer = max(current_layers) + 1
        for qubit in current_qubits:
            qubit_layers[qubit] = gate_layer
        
        gate_layers.append(gate_layer)
        if gate_layer <= max_layer:
            new_circ.append(gate[0], gate[1], gate[2])
        
        #print('Current qubits: {0}, Current layers: {1}, Gate layer: {2}'.format(current_qubits, current_layers, gate_layer))

    return new_circ