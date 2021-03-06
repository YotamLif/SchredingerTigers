from qiskit import execute
from qiskit.providers.ibmq import least_busy, IBMQ
from qiskit.tools.monitor import job_monitor


def RunTrue(circ,APItoken,maxCred=10,Shots=1024):
    IBMQ.save_account(APItoken,overwrite=True)
    IBMQ.load_accounts(hub=None)

    large_enough_devices = IBMQ.backends(filters=lambda x: x.configuration().n_qubits < 10 and not x.configuration().simulator)
    backend = least_busy(large_enough_devices)
    print("The best backend is " + backend.name())

    shots = Shots  # Number of shots to run the program (experiment); maximum is 8192 shots.
    max_credits = maxCred  # Maximum number of credits to spend on executions.

    circ.measure(circ.qregs[0],circ.cregs[0])
    job_exp = execute(circ, backend=backend, shots=shots, max_credits=max_credits)
    job_monitor(job_exp)
    return job_exp
