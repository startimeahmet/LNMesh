import itertools
import matplotlib.pyplot as plt
import os

SMALL_SIZE = 13
MEDIUM_SIZE = 13
BIGGER_SIZE = 13

plt.rc('font', size=SMALL_SIZE)          # controls default text sizes
plt.rc('axes', titlesize=SMALL_SIZE)     # fontsize of the axes title
plt.rc('axes', labelsize=MEDIUM_SIZE)    # fontsize of the x and y labels
plt.rc('xtick', labelsize=SMALL_SIZE)    # fontsize of the tick labels
plt.rc('ytick', labelsize=SMALL_SIZE)    # fontsize of the tick labels
plt.rc('legend', fontsize=SMALL_SIZE)    # legend fontsize
plt.rc('figure', titlesize=BIGGER_SIZE)  # fontsize of the figure title

plt.rcParams.update({'font.size': 12})
plt.rcParams['font.weight'] = 'bold'
plt.rcParams['axes.labelweight'] = 'bold'
plt.rcParams['axes.titleweight'] = 'bold'
plt.rcParams['figure.titleweight'] = 'bold'
# print(plt.rcParams.keys())


N_TRANSACTIONS = [20, 30, 40, 50, 60, 70, 80, 90, 100]
TOTAL_INVESTMENT = [50000, 100000, 200000, 300000, 400000]


def get_success_rates(d, e):
    SUCCESS_RATE = []

    for i in TOTAL_INVESTMENT:
        temp = []
        for j in N_TRANSACTIONS:
            f_name = "N_TRANSACTIONS_" + str(j) + "_TOTAL_INVESTMENT_" + str(i) + ".log"

            with open('experiment_results/' + d + e + '/' + f_name, 'rb') as f:
                try:  # catch OSError in case of a one line file
                    f.seek(-2, os.SEEK_END)
                    while f.read(1) != b'\n':
                        f.seek(-2, os.SEEK_CUR)
                except OSError:
                    f.seek(0)
                last_line = f.readline().decode()

            temp.append(round(float(last_line.split("%")[1]), 2))

        SUCCESS_RATE.append(temp)

    return SUCCESS_RATE


def actually_plot(rates):
    # num_nodes = 100
    # num_nodes = 200
    num_nodes = 300
    for i in range(len(TOTAL_INVESTMENT)):
        fig, ax = plt.subplots()
        colors = itertools.cycle(["red", "black", "blue"])
        markers = itertools.cycle(["o", "^", "s"])
        # for j in [0, 1, 2]:  # for 100 nodes
        # for j in [3, 4, 5]:  # for 200 nodes
        for j in [6, 7, 8]:    # for 300 nodes
            ax.text(51.8, 33.5, str(num_nodes) + ' NODES\nTOTAL INVESTMENT=' + str(TOTAL_INVESTMENT[i]),
                    fontsize=13, bbox={'edgecolor': 'lightgrey', 'facecolor': 'white'})
            # ax.text(49.5, 33.5, str(num_nodes) + ' NODES\nTOTAL INVESTMENT=' + str(TOTAL_INVESTMENT[i]),
            #         fontsize=13, bbox={'edgecolor': 'lightgrey', 'facecolor': 'white'})
            ax.plot(N_TRANSACTIONS, rates[j][i], color=next(colors), linewidth=2, marker=next(markers))

        ax.set_xticks(N_TRANSACTIONS)
        plt.ylim(30, 100)

        save_file = 'TOTAL_INVESTMENT_' + str(TOTAL_INVESTMENT[i]) + '_' + str(num_nodes) + 'nodes.pdf'

        # Adding the labels
        plt.ylabel("SUCCESS RATE %", labelpad=-3)
        plt.xlabel("NUMBER OF PAYMENTS", labelpad=6)

        plt.legend(['CDS',
                    'UST',
                    'baseline'])

        # plt.tight_layout()
        plt.grid()
        plt.savefig(save_file, bbox_inches='tight', pad_inches=0.15)
        plt.show()
        plt.close()


if __name__ == '__main__':
    directories = ['100nodes_6hr_', '200nodes_6hr_', '300nodes_6hr_']
    exp_types = ['CDS_no_loops', 'UST', 'baseline']

    success_rates = []
    for a in directories:
        for b in exp_types:
            success_rates.append(get_success_rates(a, b))

    print(success_rates)
    actually_plot(success_rates)
