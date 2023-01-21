import config
import numpy as np
import pandas as pd
import csv


def generate_distances(f_name):
    data = pd.read_csv("data/csvfiles_preprocessed/" + f_name)

    myfile = open('data/distances/' + f_name, 'w')
    wr = csv.writer(myfile)
    wr.writerow(("source", "target", "time", "distance"))

    for i in range(config.NUM_NODES):
        for j in range(1, config.NUM_NODES-i):

            x1 = data.loc[data['node'] == i, 'x']
            y1 = data.loc[data['node'] == i, 'y']
            x2 = data.loc[data['node'] == j+i, 'x']
            y2 = data.loc[data['node'] == j+i, 'y']

            piece1 = [i] * int(config.SIM_DURATION/config.TIME_PERIOD)
            piece2 = [j+i] * int(config.SIM_DURATION/config.TIME_PERIOD)
            piece3 = list(range(config.TIME_PERIOD*60, config.SIM_DURATION*60+1, config.TIME_PERIOD*60))
            piece4 = np.sqrt((x1.values-x2.values)**2 + (y1.values-y2.values)**2)

            rcount = 0
            for row in piece1:
                wr.writerow((piece1[rcount], piece2[rcount], piece3[rcount], piece4[rcount]))
                rcount = rcount + 1

    myfile.close()


def get_LN_baseline(f_name):
    data = pd.read_csv("data/distances/" + f_name)

    data2 = data[data['distance'] <= config.COVERAGE][['source', 'target']]

    data3 = data2.groupby(data2.columns.tolist(), as_index=False).size()

    data4 = data3[data3['size'] >= config.LN_CUTOFF][['source', 'target']]

    data4.to_csv('data/LN_topology_baseline/' + f_name, index=False)


if __name__ == '__main__':
    for n in range(1, 41):
        print(f"Scenario {n}")
        filename = "100nodes_6hr/scenario" + str(n) + ".csv"
        # filename = "200nodes_6hr/scenario" + str(n) + ".csv"
        # filename = "300nodes_6hr/scenario" + str(n) + ".csv"
        generate_distances(filename)
        get_LN_baseline(filename)
