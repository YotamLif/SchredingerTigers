import matplotlib.pyplot as plt; plt.rcdefaults()
import math
def MeasureCompareBar(true_run,noise_run,sim_run):
    bit_num = math.log(true_run.__len__(),2)
    x_labels = []
    for i in range(true_run.__len__()):
        index = '{0:b}'.format(i).zfill(int(bit_num))
        str_index = str(index)
        x_labels.append(str_index)
    N = true_run.__len__()
    x = np.array(range(N))
    width = 0.2
    plt.bar(x, true_run, width=width)
    plt.bar(x - width, noise_run, width=width)
    plt.bar(x + width, sim_run, width=width)
    plt.xticks(x, x_labels)
    plt.show()
