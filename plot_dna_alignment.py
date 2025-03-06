import matplotlib.pyplot as plt
import numpy as np
import matplotlib
import warnings
import sequence_alignment


def plot(res_phy, res, short_read, time_data, expected_index="1001"):
    arr = res #res.split(",")
    expected_index = get_index(arr)
    length = len(arr)
    data = [0 for i in range(length)]
    width = 0.2

    warnings.filterwarnings("ignore", category=matplotlib.MatplotlibDeprecationWarning)
    fig, ax = plt.subplots(figsize=(10, 5))
    plt.title("Short Read %s" % short_read)

    for i in range(len(arr)):
        kv = arr[i].split(":")
        data[int(kv[0], 2)] = float(kv[1]) * 100
        if expected_index == str(kv[0]):
            expect_x = int(kv[0], 2)
            expect_y = float(kv[1])

    arr_phy = res_phy #res_phy.split(",")
    data_phy = [0 for i in range(length)]
    for i in range(length):
        kv = arr_phy[i].split(":")
        data_phy[int(kv[0], 2)] = float(kv[1])

    x = np.array([i + width for i in range(length - 1)])
    x_phy = np.array([i for i in range(length - 1)])
    time_qiskit = "running time: %s s " % (str(time_data[0]))
    time_qiskit_statevector = "running time: %s s " % (str(time_data[1]))
    y = np.array(data)
    # ax.bar(x_phy, data_phy[:15], color='b', width=width, label='IBM simulator, ' + time_qiskit)
    ax.bar(x, y[:15], color='g', width=width, label='IBM simulator,' + time_qiskit_statevector)
    ax.set_ylim(4, 10)
    ax.set_xlabel("Index")
    ax.set_ylabel("Probibilty(%)")

    ax.annotate('the expected solution', xy=(expect_x + 0.5, expect_y * 100), xytext=(expect_x + 1.3, 8.5),
                arrowprops=dict(facecolor='red', shrink=0.05), )
    # plt.legend(labels = ['IBM simulator',   'QBee simulator'], loc='upper left')
    ax.legend(loc='upper left')

    # defining display layout
    plt.tight_layout()

    # show plot
    plt.show()


def get_index(res):
    test = 0
    if "1111" in res[0]:
        test = 1
    return res[test].split(":")[0]


def get_string(data):
    # a1 = data.strip()[1:-1]
    # a1 = a1.decode()
    # a1 = a1.replace("'", "")
    return data


def code_sequence(code):
    nucledite = {"A": "0", "C": "1", "G": "2", "T": "3"}
    res = []
    for i in range(len(code)):
        res.append(nucledite[code[i]])
    return "".join(res)


def ssh_python(reads):
    import select
    import subprocess
    import time
    # filename = output_path + output_name
    aa = 'python3 sequence_alignment_ssh.py %s' % reads
    f = subprocess.Popen(['ssh', 'hzhang@192.168.1.21', aa], \
                         stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    p = select.poll()
    p.register(f.stdout)
    time.sleep(5)
    test = []
    count = 0
    while count < 3 * 2:
        count += 1
        if p.poll(1):
            test.append(f.stdout.readline())
    # print(test)
    return test


def get_time_data(test):
    res = []
    for a in range(len(test)):
        res.append(round(float(test[a].decode()), 2))
    return res


warnings.filterwarnings("ignore", category=UserWarning)
print("========================", "0  1  2  3  4  5  6  7  8  9  10 11 12 13 14 ")
print("========================", "|  |  |  |  |  |  |  |  |  |  |  |  |  |  |  ")
print("The reference sequence: ", "A  T  T  G  T  C  T  A  G  G  C  G  A  C  C  A")
p = input("Please input short read: ")
while p not in ['q', "Q"]:
    encode = sequence_alignment.code_sequence(p)
    data = sequence_alignment.sequence_alignment(encode)
    time_data = data[1]
    plot(get_string(data[0][0]), get_string(data[0][1]), p, time_data)
    # print("The reference sequence: ", "ATTGTCTAGGCGACCA")
    print("========================", "0  1  2  3  4  5  6  7  8  9  10 11 12 13 14 ")
    print("========================", "|  |  |  |  |  |  |  |  |  |  |  |  |  |  |  ")
    print("The reference sequence: ", "A  T  T  G  T  C  T  A  G  G  C  G  A  C  C  A")
    p = input("Please input short read: ")
