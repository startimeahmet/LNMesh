import csv
import pandas as pd
from matplotlib import pyplot as plt
import networkx as nx
from dppy.exotic_dpps import UST
import os


def draw_UST(mygraph):
    nx.draw(mygraph, with_labels=True, node_size=5, node_color="black", width=0.1, font_color="red", font_size=5)
    # ust.plot()
    plt.savefig('testUST.pdf')
    plt.show()


if __name__ == '__main__':
    for j in range(1, 41):
        main_directory = "100nodes_6hr"
        # main_directory = "200nodes_6hr"
        # main_directory = "300nodes_6hr"
        filename = main_directory + "/scenario" + str(j) + ".csv"

        data = pd.read_csv("data/LN_topology_baseline/" + filename)
        G = nx.Graph()
        for index, row in data.iterrows():
            G.add_edge(int(row['source']), int(row['target']))

        print(G)
        for k in range(1, 31):  # how many UST we want to generate from G
            # Initialize UST object
            ust = UST(G)
            # print(ust.sample(root=6, random_state=np.random))
            ust.sample()
            H = ust.list_of_samples[-1]
            print(H)
            print(sorted(list(H.edges)))

            # draw_UST(G)

            print(f"G is a {G}")
            print(f"One of the Uniform Spanning Trees for G is a {H}")
            print(f"H is: {sorted(H.edges)}")

            # Directory
            directory = "scenario" + str(j)
            # Parent Directory path
            parent_dir = "data/LN_topology_UST/" + main_directory
            # Path
            path = os.path.join(parent_dir, directory)

            isExist = os.path.exists(path)
            if not isExist:
                os.mkdir(path)
                print("Directory '% s' created" % directory)

            file = open("data/LN_topology_UST/" + main_directory + "/scenario" + str(j) + "/UST" + str(k), 'w+', newline='')

            with file:
                write = csv.writer(file)
                write.writerow(["source", "target"])
                write.writerows(sorted(list(sorted(H.edges))))
