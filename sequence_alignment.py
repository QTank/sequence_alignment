from qiskit import QuantumCircuit, execute, Aer
from math import *
import random
import numpy as np
import operator
import circuit
import time
import sys

N = 16
w = "0332313022120110"  # Reference Genome: "ATTGTCTAGGCGACCA"
nucledite = {"A": 0, "C": 1, "G": 2, "T": 3}
M = 2  # Short Read size
p = "32"  # Short Read: "AA"
A = 4
Q_A = ceil(log2(A))  # Number of qubits to encode one character
Q_D = Q_A * M  # Number of data qubits
Q_T = ceil(log2(N - M))  # Tag Qubits
Q_anc = 1  # + 5	    			# Number of ancilla qubits
anc = Q_D + Q_T  # Ancilla qubit id
total_qubits = Q_D + Q_T + Q_anc


def QAM():
    # print(qc.draw())
    # print(qc.qasm())
    # test = run_circuit(get_qc(), Q_A)
    qc = get_qc()
    # output_state(qc)
    return qc


def get_qc():
    qc = QuantumCircuit(total_qubits)
    cir1(qc)
    cir2(qc)
    cir3(qc)
    cir4(qc)
    cir5(qc)
    cir4(qc)
    for i in range(3):
        cir3(qc)
        cir4(qc)
    return qc


def randStr(szA, sz):
    # Generates a random string of length 'sz' over the alphabet of size 'szA' in decimal
    bias = 1 / szA  # IMPROVE: add bias here
    rb = ""
    for i in range(0, sz):
        rn = random.random()
        for j in range(0, szA):
            if rn < (j + 1) * bias:
                rb = rb + str(j)  # IMPROVE: BCD version
                break
    return


def cir1(qc):
    for i in range(Q_T):
        qc.h(i)
    nc = [ci for ci in range(Q_T)]
    for i in range(N - M + 1):
        Qis = format(i, '0' + str(Q_T) + 'b')
        for j in range(Q_T):
            if Qis[j] == '0':
                qc.x(j)
        wMi = w[i:i + M]
        # print([i, wMi])
        for wi in range(M):
            w_a = format(int(wMi[wi]), '0' + str(Q_A) + 'b')
            for wj in range(Q_A):
                if w_a[wj] == '1':
                    # nCX(qc, nc, Q_T+wi*Q_A+wj, anc)  # cnot
                    # nCX_new(qc, nc, Q_T+wi*Q_A+wj, anc)  # cnot
                    qc.mcx(nc, Q_T + wi * Q_A + wj)
        for j in range(Q_T):
            if Qis[j] == '0':
                qc.x(j)

    wMi = p
    for i in range(N - M + 1, 2 ** Q_T):
        w_a = format(i, '0' + str(Q_T) + 'b')
        for wj in range(Q_T):
            if w_a[wj] == '0':
                qc.x(wj)
        for wj in range(M):
            w_str = format(int(wMi[wj]), '0' + str(Q_A) + 'b')
            for wh in range(Q_A):
                if w_str[wh] == '0':
                    # nCX(qc, nc, Q_T+wj*Q_A+wh, anc)
                    # nCX_new(qc, nc, Q_T+wj*Q_A+wh, anc)
                    qc.mcx(nc, Q_T + wj * Q_A + wh)
        for wj in range(Q_T):
            if w_a[wj] == '0':
                qc.x(wj)
    return


def cir2(qc):
    for i in range(M):
        w_a = format(int(p[i]), '0' + str(Q_A) + 'b')
        for j in range(Q_A):
            if w_a[j] == '1':
                qc.x(Q_T + i * Q_A + j)

    return


def cir3(qc):
    return circuit.cir3(qc)


def cir4(qc):
    for i in range(Q_D + Q_T):
        qc.h(i)
        qc.x(i)

    qc.h(Q_D + Q_T - 1)
    nc = [ci for ci in range(Q_D + Q_T - 1)]
    # nCX(qc, nc, Q_D+Q_T-1, anc)
    # nCX_new(qc, nc, Q_D+Q_T-1, anc)
    qc.mcx(nc, Q_T + Q_T - 1)
    qc.h(Q_D + Q_T - 1)
    # this could be h gate then x gate
    for i in range(Q_D + Q_T):
        qc.x(i)
        qc.h(i)


def cir5(qc):
    nc = [ci for ci in range(Q_D + Q_T - 1)]
    for i in range(N - M + 1):
        w_a = format(i, '0' + str(Q_T) + 'b')
        wMi = w[i:i + M]
        wt = w_a

        for j in range(M):
            hd = int(format(int(wMi[j]), '0' + str(Q_A) + 'b'), 2) ^ int(format(int(p[j]), '0' + str(Q_A) + 'b'), 2)
            w_hd = format(hd, '0' + str(Q_A) + 'b')
            wt = wt + w_hd
        for j in range(Q_T + Q_D):
            if wt[j] == '0':
                qc.x(j)
            qc.h(Q_D + Q_T - 1)
            # nCX(qc, nc, Q_D+Q_T-1, anc)
            # nCX_new(qc, nc, Q_D+Q_T-1, anc)
            qc.mcx(nc, Q_T + Q_T - 1)
            qc.h(Q_D + Q_T - 1)
            if wt[j] == '0':
                qc.x(j)


def nCX(qc, c, t, anc):
    qc.mcx(c, t)
    return
    nc = len(c)
    if nc == 1:
        qc.cx(c[0], t)
    elif nc == 2:
        qc.ccx(c[0], c[1], t)
    else:
        qc.ccx(c[0], c[1], t)
        for i in range(2, nc):
            qc.ccx(c[i], anc + i - 2, anc + i - 1)
        qc.cx(anc + nc - 2, t)
        for i in range(nc - 1, 1, -1):
            qc.ccx(c[i], anc + i - 2, anc + i - 1)
        qc.ccx(c[0], c[1], t)


def nCX_new(qc, c, t, b):
    nc = len(c)
    if nc == 1:
        qc.cx(c[0], t)
    elif nc == 2:
        qc.ccx(c[0], c[1], t)
    else:
        nch = ceil(nc / 2)
        c1 = c[:nch]
        c2 = c[nch:]
        c2.append(b)
        nCX_new(qc, c1, b, nch + 1)
        nCX_new(qc, c2, t, nch - 1)
        nCX_new(qc, c1, b, nch + 1)
        nCX_new(qc, c2, t, nch - 1)
    return


def run_circuit(qc, s):
    qc.measure_all()
    aa = Aer.get_backend("qasm_simulator")
    shots = 1000
    a1 = execute(qc, backend=aa, shots=shots)
    res = a1.result()
    counts = res.get_counts()
    sorted_counts = dict(sorted(counts.items(), key=operator.itemgetter(1), reverse=True))
    test = {}
    for state in sorted_counts:
        # print(state, '\t\t', sorted_counts[state])
        index_res = state[:4:-1]
        if index_res in test:
            test[index_res] = test[index_res] + sorted_counts[state]
        else:
            test[index_res] = sorted_counts[state]

    # for k in test:
    #    print("%s, probability:%s" % (k, str(test[k])))

    # for k in sorted_counts:
    #    print("%s, count:%f" % (k, sorted_counts[k]*1.0/shots))
    res = []
    # print("================This result on qiskit for qubits with noise==============================")
    test = sorted(test.items(), key=operator.itemgetter(1), reverse=True)
    for k in test:
        # print("%s, probability:%s%s" % (k[0], str(round(k[1]*100.0/shots,2)), "%"))
        res.append("%s:%s" % (k[0], str(round(k[1] * 100.0 / shots, 2))))
    # print("res_qiskit='%s'" % ",".join(res))
    return res  # "res_qiskit='%s'" % ",".join(res)


def output(qc, s):
    qc.measure_all()
    aa = Aer.get_backend('qasm_simulator')
    job = execute(qc, aa, shots=1000)
    result = job.result()
    # print(result)
    counts = result.get_counts(qc)
    print('Running on local simulator')
    print('State', '\t\tOccurance')

    sorted_counts = dict(sorted(counts.items(), key=operator.itemgetter(1), reverse=True))
    test = {}
    for quantum_state in sorted_counts:
        print(quantum_state, '\t\t', sorted_counts[quantum_state])
        # a = quantum_state[6:9]
        # print(a)
        # if a not in test:
        #    test[a] = sorted_counts[quantum_state]
        # else:
        #    test[a] = test[a] + sorted_counts[quantum_state]
    # print(test)


def output_state(qc):
    aa = Aer.get_backend('statevector_simulator')
    job = execute(qc, backend=aa, shots=1000)
    result = job.result()
    res = result.get_statevector(qc)
    res_array = np.asarray(res)
    length = len(res_array)
    test = {}
    for a in range(length):
        # print("%s: %f" % (str(format(a, '0'+str(total_qubits)+'b')), np.real(res[a] * np.conj(res[a]))))
        state = str(format(a, '0' + str(total_qubits) + 'b'))
        val = np.real(res[a] * np.conj(res[a]))
        index_res = state[:4:-1]
        if index_res in test:
            test[index_res] = test[index_res] + val
        else:
            test[index_res] = val
    res = []
    # print("================This result on qiskit for perfect qubits==============================")
    test = sorted(test.items(), key=operator.itemgetter(1), reverse=True)
    for k in test:
        # print("%s, probability:%s%s" % (k[0], str(round(k[1]*100,2)), "%"))
        res.append("%s:%s" % (k[0], str(round(k[1], 5))))
    # print("res_qiskit_perfect='%s'" % ",".join(res))
    return res  # ",".join(res)


def test_mcx():
    qc = QuantumCircuit(5)
    for i in range(4):
        qc.x(i)

    qc.mcx([0, 1, 2, 3], 4)
    output(qc, 1)


def get_output(res):
    prob = 'prob'
    test = {}
    for k in res:
        index_res = k[:4:-1]
        if index_res in test:
            test[index_res] += res[k][prob]
        else:
            test[index_res] = res[k][prob]

    # print("================This result on QBee Simulator for perfect qubits==============================")
    test = sorted(test.items(), key=operator.itemgetter(1), reverse=True)
    count = 0
    res = []
    for k in test:
        # print()
        # print("%s, probility:%s" % (k, test[k]))
        # print("%s, probability:%s%s" % (k[0], str(round(k[1]*100,2)), "%"))
        count += k[1]
        res.append("%s:%s" % (k[0], str(round(k[1], 5))))
    # print("res_qbee = '%s'" % ",".join(res))
    return res  # "res_qbee = '%s'" % ",".join(res)


def decode_sequence(code):
    nucledite = ["A", "C", "G", "T"]
    res = []
    for i in range(len(code)):
        res.append(str(nucledite[int(code[i])]))
    return "".join(res)


def code_sequence(code):
    nucledite = {"A": "0", "C": "1", "G": "2", "T": "3", "a": "0", "c": "1", "g": "2", "t": "3"}
    res = []
    for i in range(len(code)):
        res.append(nucledite[code[i]])
    return "".join(res)


def sequence_alignment(p_input_code):
    p = p_input_code
    # print("=============Start search short read %s========" % p_input_code)
    start_time_qiskit = time.time()
    test = run_circuit(get_qc(), Q_A)
    executing_qiskit = time.time() - start_time_qiskit

    start_time_qiskit_statevector = time.time()
    res_qiskit = output_state(get_qc())
    time_qiskit = time.time() - start_time_qiskit_statevector

    return [test, res_qiskit], [executing_qiskit, time_qiskit]


if __name__ == '__main__':
    # a = "a"
    # p = sys.argv[1]
    p = "CT"
    p = code_sequence(p)
    result_array, time_array = sequence_alignment(p)

    for i in range(len(result_array)):
        print(result_array[i])
        print(f"executing time {time_array[i]} s")
