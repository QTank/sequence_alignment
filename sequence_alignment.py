from qiskit import QuantumCircuit, execute, Aer
from math import *
import random
import numpy as np
import operator
import time
import sys

N = 16
w = "0332313022120110"  # Reference Genome: "ATTGTCTAGGCGACCA"
nucledite = {"A": 0, "C": 1, "G": 2, "T": 3}
M = 2  # Short Read size
# p = "32"  # Short Read: "AA"
A = 4
Q_A = ceil(log2(A))  # Number of qubits to encode one character
Q_D = Q_A * M  # Number of data qubits
Q_T = ceil(log2(N - M))  # Tag Qubits
Q_anc = 1  # + 5	    			# Number of ancilla qubits
anc = Q_D + Q_T  # Ancilla qubit id
total_qubits = Q_D + Q_T + Q_anc

def QAM():
    qc = get_qc()
    return qc

def get_qc(short_read):
    qc = QuantumCircuit(total_qubits)
    cir1(qc, short_read)
    cir2(qc, short_read)
    cir3(qc)
    cir4(qc)
    cir5(qc, short_read)
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


def cir1(qc, p):
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


def cir2(qc, p):
    for i in range(M):
        w_a = format(int(p[i]), '0' + str(Q_A) + 'b')
        for j in range(Q_A):
            if w_a[j] == '1':
                qc.x(Q_T + i * Q_A + j)

    return


# def cir3(qc):
#     return circuit.cir3(qc)


def cir3(qc):
    qc.rz(-2.495565,4)
    qc.ry(-1.046381,4)
    qc.rz(-0.634842,4)
    qc.rz(-1.095612,5)
    qc.cnot(4,5)
    qc.rz(-1.574113,5)
    qc.cnot(4,5)
    qc.rz(-0.663604,4)
    qc.ry(-1.337541,4)
    qc.rz(0.663604,4)
    qc.ry(2.180982,5)
    qc.cnot(4,5)
    qc.ry(0.270123,5)
    qc.cnot(4,5)
    qc.rz(-4.560313,4)
    qc.ry(-2.345810,4)
    qc.rz(0.217847,4)
    qc.rz(2.141438,5)
    qc.cnot(4,5)
    qc.rz(-0.835336,5)
    qc.cnot(4,5)
    qc.rz(0.573939,4)
    qc.ry(-1.161760,4)
    qc.rz(-0.573939,4)
    qc.rz(0.265150,6)
    qc.cnot(4,6)
    qc.rz(0.792581,6)
    qc.cnot(5,6)
    qc.rz(-1.778400,6)
    qc.cnot(4,6)
    qc.rz(0.309606,6)
    qc.cnot(5,6)
    qc.rz(0.867198,4)
    qc.ry(-1.020460,4)
    qc.rz(-0.892549,4)
    qc.rz(-0.978970,5)
    qc.cnot(4,5)
    qc.rz(-2.042658,5)
    qc.cnot(4,5)
    qc.rz(-0.771181,4)
    qc.ry(-0.386977,4)
    qc.rz(0.771181,4)
    qc.ry(1.644840,5)
    qc.cnot(4,5)
    qc.ry(0.504899,5)
    qc.cnot(4,5)
    qc.rz(0.662837,4)
    qc.ry(-1.694500,4)
    qc.rz(-3.616169,4)
    qc.rz(0.160840,5)
    qc.cnot(4,5)
    qc.rz(-0.807003,5)
    qc.cnot(4,5)
    qc.rz(-0.523538,4)
    qc.ry(-1.195233,4)
    qc.rz(0.523538,4)
    qc.ry(1.486933,6)
    qc.cnot(4,6)
    qc.ry(0.346126,6)
    qc.cnot(5,6)
    qc.ry(-0.150052,6)
    qc.cnot(4,6)
    qc.ry(0.589344,6)
    qc.cnot(5,6)
    qc.rz(-4.033427,4)
    qc.ry(-2.661051,4)
    qc.rz(-0.217231,4)
    qc.rz(-0.679055,5)
    qc.cnot(4,5)
    qc.rz(1.623385,5)
    qc.cnot(4,5)
    qc.rz(-1.573731,4)
    qc.ry(-0.475009,4)
    qc.rz(1.573731,4)
    qc.ry(2.071674,5)
    qc.cnot(4,5)
    qc.ry(0.764902,5)
    qc.cnot(4,5)
    qc.rz(1.904202,4)
    qc.ry(-1.576334,4)
    qc.rz(3.300418,4)
    qc.rz(0.246450,5)
    qc.cnot(4,5)
    qc.rz(1.446510,5)
    qc.cnot(4,5)
    qc.rz(-3.121304,4)
    qc.ry(-1.150659,4)
    qc.rz(3.121304,4)
    qc.rz(-0.568080,6)
    qc.cnot(4,6)
    qc.rz(-0.678844,6)
    qc.cnot(5,6)
    qc.rz(-0.184890,6)
    qc.cnot(4,6)
    qc.rz(1.600579,6)
    qc.cnot(5,6)
    qc.rz(2.234130,4)
    qc.ry(-2.090960,4)
    qc.rz(1.062383,4)
    qc.rz(0.164323,5)
    qc.cnot(4,5)
    qc.rz(1.743454,5)
    qc.cnot(4,5)
    qc.rz(-1.629366,4)
    qc.ry(-0.512242,4)
    qc.rz(1.629366,4)
    qc.ry(1.152369,5)
    qc.cnot(4,5)
    qc.ry(0.797232,5)
    qc.cnot(4,5)
    qc.rz(-0.651534,4)
    qc.ry(-2.240981,4)
    qc.rz(2.205052,4)
    qc.rz(1.091160,5)
    qc.cnot(4,5)
    qc.rz(0.777808,5)
    qc.cnot(4,5)
    qc.rz(2.741933,4)
    qc.ry(-1.561898,4)
    qc.rz(-2.741933,4)
    qc.rz(-0.392699,7)
    qc.cnot(4,7)
    qc.rz(0.857984,7)
    qc.cnot(5,7)
    qc.rz(-0.392699,7)
    qc.cnot(4,7)
    qc.rz(-0.730732,7)
    qc.cnot(6,7)
    qc.rz(-1.070810,7)
    qc.cnot(4,7)
    qc.rz(-0.849024,7)
    qc.cnot(5,7)
    qc.rz(0.285412,7)
    qc.cnot(4,7)
    qc.rz(-0.849024,7)
    qc.cnot(6,7)
    qc.rz(2.422630,4)
    qc.ry(-1.054241,4)
    qc.rz(-0.670996,4)
    qc.rz(-0.346171,5)
    qc.cnot(4,5)
    qc.rz(-2.395018,5)
    qc.cnot(4,5)
    qc.rz(-2.330937,4)
    qc.ry(-1.254475,4)
    qc.rz(2.330937,4)
    qc.ry(1.739765,5)
    qc.cnot(4,5)
    qc.ry(0.618025,5)
    qc.cnot(4,5)
    qc.rz(-2.169652,4)
    qc.ry(-2.868867,4)
    qc.rz(2.683293,4)
    qc.rz(0.126237,5)
    qc.cnot(4,5)
    qc.rz(-1.920065,5)
    qc.cnot(4,5)
    qc.rz(-1.083853,4)
    qc.ry(-1.399634,4)
    qc.rz(1.083853,4)
    qc.rz(0.040519,6)
    qc.cnot(4,6)
    qc.rz(0.810583,6)
    qc.cnot(5,6)
    qc.rz(1.374535,6)
    qc.cnot(4,6)
    qc.rz(0.527623,6)
    qc.cnot(5,6)
    qc.rz(-5.305886,4)
    qc.ry(-0.764960,4)
    qc.rz(0.785715,4)
    qc.rz(-0.264883,5)
    qc.cnot(4,5)
    qc.rz(1.987388,5)
    qc.cnot(4,5)
    qc.rz(1.990355,4)
    qc.ry(-0.392324,4)
    qc.rz(-1.990355,4)
    qc.ry(1.862818,5)
    qc.cnot(4,5)
    qc.ry(0.827526,5)
    qc.cnot(4,5)
    qc.rz(-1.779818,4)
    qc.ry(-1.301020,4)
    qc.rz(-1.688079,4)
    qc.rz(0.417135,5)
    qc.cnot(4,5)
    qc.rz(-1.817636,5)
    qc.cnot(4,5)
    qc.rz(-0.537353,4)
    qc.ry(-0.105530,4)
    qc.rz(0.537353,4)
    qc.ry(1.025571,6)
    qc.cnot(4,6)
    qc.ry(0.386772,6)
    qc.cnot(5,6)
    qc.ry(0.325953,6)
    qc.cnot(4,6)
    qc.ry(0.964752,6)
    qc.cnot(5,6)
    qc.rz(0.589048,4)
    qc.ry(-2.364848,4)
    qc.rz(4.476448,4)
    qc.rz(-0.862498,5)
    qc.cnot(4,5)
    qc.rz(-1.949294,5)
    qc.cnot(4,5)
    qc.rz(-0.830300,4)
    qc.ry(-0.962399,4)
    qc.rz(0.830300,4)
    qc.ry(1.652079,5)
    qc.cnot(4,5)
    qc.ry(0.567936,5)
    qc.cnot(4,5)
    qc.rz(-3.400688,4)
    qc.ry(-0.392400,4)
    qc.rz(2.556896,4)
    qc.rz(-1.608724,5)
    qc.cnot(4,5)
    qc.rz(0.535112,5)
    qc.cnot(4,5)
    qc.rz(-2.631783,4)
    qc.ry(-1.010089,4)
    qc.rz(2.631783,4)
    qc.rz(-0.749385,6)
    qc.cnot(4,6)
    qc.rz(-0.995045,6)
    qc.cnot(5,6)
    qc.rz(-0.425068,6)
    qc.cnot(4,6)
    qc.rz(1.656585,6)
    qc.cnot(5,6)
    qc.rz(-1.259555,4)
    qc.ry(-1.413129,4)
    qc.rz(-0.376948,4)
    qc.rz(-0.023320,5)
    qc.cnot(4,5)
    qc.rz(0.375551,5)
    qc.cnot(4,5)
    qc.rz(-0.124097,4)
    qc.ry(-0.211290,4)
    qc.rz(0.124097,4)
    qc.ry(1.630461,5)
    qc.cnot(4,5)
    qc.ry(0.680158,5)
    qc.cnot(4,5)
    qc.rz(-5.829541,4)
    qc.ry(-2.443439,4)
    qc.rz(0.018165,4)
    qc.rz(0.242793,5)
    qc.cnot(4,5)
    qc.rz(-1.876220,5)
    qc.cnot(4,5)
    qc.rz(1.413556,4)
    qc.ry(-0.974064,4)
    qc.rz(-1.413556,4)
    qc.ry(0.261799,7)
    qc.cnot(4,7)
    qc.ry(0.261799,7)
    qc.cnot(5,7)
    qc.ry(0.261799,7)
    qc.cnot(4,7)
    qc.ry(0.261799,7)
    qc.cnot(6,7)
    qc.ry(0.261799,7)
    qc.cnot(4,7)
    qc.ry(0.261799,7)
    qc.cnot(5,7)
    qc.ry(0.261799,7)
    qc.cnot(4,7)
    qc.ry(0.261799,7)
    qc.cnot(6,7)
    qc.rz(3.477399,4)
    qc.ry(-1.335230,4)
    qc.rz(1.300499,4)
    qc.rz(1.438258,5)
    qc.cnot(4,5)
    qc.rz(-0.801232,5)
    qc.cnot(4,5)
    qc.rz(-1.104663,4)
    qc.ry(-1.513998,4)
    qc.rz(1.104663,4)
    qc.ry(1.300200,5)
    qc.cnot(4,5)
    qc.ry(0.817306,5)
    qc.cnot(4,5)
    qc.rz(-0.537000,4)
    qc.ry(-2.102438,4)
    qc.rz(-1.622373,4)
    qc.rz(-0.525194,5)
    qc.cnot(4,5)
    qc.rz(0.334422,5)
    qc.cnot(4,5)
    qc.rz(0.438354,4)
    qc.ry(-1.454119,4)
    qc.rz(-0.438354,4)
    qc.rz(-0.785398,6)
    qc.cnot(4,6)
    qc.rz(-0.085948,6)
    qc.cnot(5,6)
    qc.rz(-0.785398,6)
    qc.cnot(4,6)
    qc.rz(-1.484849,6)
    qc.cnot(5,6)
    qc.rz(3.350364,4)
    qc.ry(-2.676777,4)
    qc.rz(2.930095,4)
    qc.rz(0.954045,5)
    qc.cnot(4,5)
    qc.rz(0.745842,5)
    qc.cnot(4,5)
    qc.rz(2.944517,4)
    qc.ry(-1.291884,4)
    qc.rz(-2.944517,4)
    qc.ry(1.438536,5)
    qc.cnot(4,5)
    qc.ry(0.852927,5)
    qc.cnot(4,5)
    qc.rz(1.249836,4)
    qc.ry(-2.002135,4)
    qc.rz(-2.140359,4)
    qc.rz(-0.086264,5)
    qc.cnot(4,5)
    qc.rz(-0.840127,5)
    qc.cnot(4,5)
    qc.rz(-2.964859,4)
    qc.ry(-1.544692,4)
    qc.rz(2.964859,4)
    qc.ry(1.614267,6)
    qc.cnot(4,6)
    qc.ry(0.309438,6)
    qc.cnot(5,6)
    qc.ry(-0.036398,6)
    qc.cnot(4,6)
    qc.ry(1.254285,6)
    qc.cnot(5,6)
    qc.rz(4.735940,4)
    qc.ry(-1.080950,4)
    qc.rz(-1.398253,4)
    qc.rz(0.141644,5)
    qc.cnot(4,5)
    qc.rz(1.581510,5)
    qc.cnot(4,5)
    qc.rz(3.000507,4)
    qc.ry(-1.345787,4)
    qc.rz(-3.000507,4)
    qc.ry(2.303325,5)
    qc.cnot(4,5)
    qc.ry(0.768309,5)
    qc.cnot(4,5)
    qc.rz(-4.022805,4)
    qc.ry(-2.559101,4)
    qc.rz(1.595668,4)
    qc.rz(-1.365775,5)
    qc.cnot(4,5)
    qc.rz(-1.372495,5)
    qc.cnot(4,5)
    qc.rz(-1.209858,4)
    qc.ry(-0.713527,4)
    qc.rz(1.209858,4)
    qc.rz(-0.392699,6)
    qc.cnot(4,6)
    qc.rz(1.718203,6)
    qc.cnot(5,6)
    qc.rz(-0.159657,6)
    qc.cnot(4,6)
    qc.rz(-1.151992,6)
    qc.cnot(5,6)
    qc.rz(-2.103083,4)
    qc.ry(-1.642351,4)
    qc.rz(-1.494416,4)
    qc.rz(-0.071267,5)
    qc.cnot(4,5)
    qc.rz(1.653073,5)
    qc.cnot(4,5)
    qc.rz(-0.387850,4)
    qc.ry(-0.891440,4)
    qc.rz(0.387850,4)
    qc.ry(0.437715,5)
    qc.cnot(4,5)
    qc.ry(0.234582,5)
    qc.cnot(4,5)
    qc.rz(-4.048179,4)
    qc.ry(-2.212950,4)
    qc.rz(-0.379861,4)
    qc.rz(1.259357,5)
    qc.cnot(4,5)
    qc.rz(-0.726894,5)
    qc.cnot(4,5)
    qc.rz(-0.204942,4)
    qc.ry(-1.154988,4)
    qc.rz(0.204942,4)
    qc.rz(-0.000000,7)
    qc.cnot(4,7)
    qc.rz(-1.250684,7)
    qc.cnot(5,7)
    qc.rz(-0.338033,7)
    qc.cnot(4,7)
    qc.rz(0.000000,7)
    qc.cnot(6,7)
    qc.rz(0.000000,7)
    qc.cnot(4,7)
    qc.rz(-0.221786,7)
    qc.cnot(5,7)
    qc.rz(-1.134436,7)
    qc.cnot(4,7)
    qc.rz(0.000000,7)
    qc.cnot(6,7)
    qc.rz(0.311756,4)
    qc.ry(-0.913364,4)
    qc.rz(5.950218,4)
    qc.rz(1.175158,5)
    qc.cnot(4,5)
    qc.rz(0.505238,5)
    qc.cnot(4,5)
    qc.rz(0.562177,4)
    qc.ry(-0.920386,4)
    qc.rz(-0.562177,4)
    qc.ry(1.229257,5)
    qc.cnot(4,5)
    qc.ry(0.351218,5)
    qc.cnot(4,5)
    qc.rz(-0.714317,4)
    qc.ry(-1.273729,4)
    qc.rz(2.687247,4)
    qc.rz(-0.815124,5)
    qc.cnot(4,5)
    qc.rz(1.756678,5)
    qc.cnot(4,5)
    qc.rz(-1.191286,4)
    qc.ry(-1.322072,4)
    qc.rz(1.191286,4)
    qc.rz(-0.392699,6)
    qc.cnot(4,6)
    qc.rz(0.560325,6)
    qc.cnot(5,6)
    qc.rz(0.367070,6)
    qc.cnot(4,6)
    qc.rz(-1.604025,6)
    qc.cnot(5,6)
    qc.rz(3.443813,4)
    qc.ry(-0.528964,4)
    qc.rz(-2.730648,4)
    qc.rz(0.333271,5)
    qc.cnot(4,5)
    qc.rz(2.086082,5)
    qc.cnot(4,5)
    qc.rz(-0.945221,4)
    qc.ry(-0.446899,4)
    qc.rz(0.945221,4)
    qc.ry(1.423641,5)
    qc.cnot(4,5)
    qc.ry(0.452590,5)
    qc.cnot(4,5)
    qc.rz(-3.227600,4)
    qc.ry(-0.800360,4)
    qc.rz(0.895195,4)
    qc.rz(0.879420,5)
    qc.cnot(4,5)
    qc.rz(-1.175390,5)
    qc.cnot(4,5)
    qc.rz(-2.704350,4)
    qc.ry(-1.291475,4)
    qc.rz(2.704350,4)
    qc.ry(1.783616,6)
    qc.cnot(4,6)
    qc.ry(0.493806,6)
    qc.cnot(5,6)
    qc.ry(0.142692,6)
    qc.cnot(4,6)
    qc.ry(0.538500,6)
    qc.cnot(5,6)
    qc.rz(0.074716,4)
    qc.ry(-1.215538,4)
    qc.rz(2.366195,4)
    qc.rz(-0.634980,5)
    qc.cnot(4,5)
    qc.rz(-2.304112,5)
    qc.cnot(4,5)
    qc.rz(-0.827265,4)
    qc.ry(-1.142645,4)
    qc.rz(0.827265,4)
    qc.ry(1.674571,5)
    qc.cnot(4,5)
    qc.ry(0.564013,5)
    qc.cnot(4,5)
    qc.rz(0.557684,4)
    qc.ry(-0.316529,4)
    qc.rz(4.037339,4)
    qc.rz(-1.658384,5)
    qc.cnot(4,5)
    qc.rz(0.946438,5)
    qc.cnot(4,5)
    qc.rz(-1.615404,4)
    qc.ry(-1.423146,4)
    qc.rz(1.615404,4)
    qc.rz(0.785398,6)
    qc.cnot(4,6)
    qc.rz(-1.895989,6)
    qc.cnot(5,6)
    qc.rz(0.785398,6)
    qc.cnot(4,6)
    qc.rz(0.325193,6)
    qc.cnot(5,6)
    qc.rz(3.212053,4)
    qc.ry(-1.388574,4)
    qc.rz(-1.391053,4)
    qc.rz(1.520843,5)
    qc.cnot(4,5)
    qc.rz(0.942892,5)
    qc.cnot(4,5)
    qc.rz(1.229895,4)
    qc.ry(-1.476998,4)
    qc.rz(-1.229895,4)
    qc.ry(1.477189,5)
    qc.cnot(4,5)
    qc.ry(0.636033,5)
    qc.cnot(4,5)
    qc.rz(-1.659093,4)
    qc.ry(-2.163702,4)
    qc.rz(-2.151962,4)
    qc.rz(-0.872758,5)
    qc.cnot(4,5)
    qc.rz(-1.456869,5)
    qc.cnot(4,5)
    qc.rz(-0.779867,4)
    qc.ry(-1.548794,4)
    qc.rz(0.779867,4)
    return qc



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


def cir5(qc, p):
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
        index_res = state[:4:-1]
        if index_res in test:
            test[index_res] = test[index_res] + sorted_counts[state]
        else:
            test[index_res] = sorted_counts[state]

    res = []
    # print("================This result on qiskit for qubits with noise==============================")
    test = sorted(test.items(), key=operator.itemgetter(1), reverse=True)
    for k in test:
        res.append("%s:%s" % (k[0], str(round(k[1] * 100.0 / shots, 2))))
    return res


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
    # print("================This result on qiskit for statevector==============================")
    test = sorted(test.items(), key=operator.itemgetter(1), reverse=True)
    for k in test:
        res.append("%s:%s" % (k[0], str(round(k[1], 5))))
    return res


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
    # p = p_input_code
    # print("=============Start search short read %s========" % p_input_code)
    start_time_qiskit = time.time()
    test = run_circuit(get_qc(p_input_code), Q_A)
    executing_qiskit = round(time.time() - start_time_qiskit, 2)

    start_time_qiskit_statevector = time.time()
    res_qiskit = output_state(get_qc(p_input_code))
    time_qiskit = round(time.time() - start_time_qiskit_statevector, 2)

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
