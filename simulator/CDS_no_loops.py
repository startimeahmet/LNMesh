import csv
import matplotlib.pyplot as plt
import networkx as nx
import networkx.algorithms.approximation as nxaa
from collections import OrderedDict, deque
import copy
import operator
import pandas as pd


class DominatingSets:
    @classmethod
    def get_dominating_sets(cls, G, weight=None):
        """get a dominating sets"""
        dominating_sets = nxaa.min_weighted_dominating_set(G, weight=weight)

        return dominating_sets

    @classmethod
    def min_connected_dominating_sets_non_distributed(cls, G):
        assert nx.is_connected(G)

        G2 = copy.deepcopy(G)

        # Step 1: initialization
        # take the node with maximum degree as the starting node
        starting_node = max(dict(G2.degree()).items(), key=operator.itemgetter(1))[0]
        fixed_nodes = {starting_node}

        # Enqueue the neighbor nodes of starting node to Q in descending order by their degree
        neighbor_nodes = G2.neighbors(starting_node)
        neighbor_nodes_sorted = OrderedDict(sorted(dict(G2.degree(neighbor_nodes)).items(), key=operator.itemgetter(1), reverse=True)).keys()

        priority_queue = deque(neighbor_nodes_sorted)  # a priority queue is maintained centrally to decide whether an element would be a part of CDS.

        inserted_set = set(list(neighbor_nodes_sorted) + [starting_node])

        # Step 2: calculate the cds
        while priority_queue:
            u = priority_queue.pop()

            # check if the graph after removing u is still connected
            rest_graph = copy.deepcopy(G2)
            rest_graph.remove_node(u)

            if nx.is_connected(rest_graph):
                G2.remove_node(u)
            else:  # is not connected
                fixed_nodes.add(u)

                # add neighbors of u to the priority queue, which never are inserted into Q
                inserted_neighbors = set(G2.neighbors(u)) - inserted_set
                inserted_neighbors_sorted = OrderedDict(sorted(dict(G2.degree(inserted_neighbors)).items(),
                                                               key=operator.itemgetter(1), reverse=True)).keys()

                priority_queue.extend(inserted_neighbors_sorted)
                inserted_set.update(inserted_neighbors_sorted)

        # Step 3: verify the result
        assert nx.is_dominating_set(G, fixed_nodes) and nx.is_connected(G.subgraph(fixed_nodes))

        return fixed_nodes


def add_more_channels(G, H):
    H2 = nx.Graph(H)
    for node in sorted(G.nodes):
        if not H.has_node(node):  # selecting a node that's not in CDS

            neighbors = list(G.neighbors(node))  # neighbors of a non-CDS node
            possibilities = list(set(neighbors).intersection(H.nodes))  # possible nodes to open a channel to
            # print(f"possibilities for node {node}: {possibilities}")

            H2.add_edge(node, possibilities[0])

    return H2


def main():
    for j in range(1, 41):
        filename = "100nodes_6hr/scenario" + str(j) + ".csv"
        # filename = "200nodes_6hr/scenario" + str(j) + ".csv"
        # filename = "300nodes_6hr/scenario" + str(j) + ".csv"
        print(f"filename: {filename}")
        try:
            data = pd.read_csv("data/LN_topology_baseline/" + filename)
            G = nx.Graph()
            for index, row in data.iterrows():
                G.add_edge(int(row['source']), int(row['target']))

            # calculate a connected dominating set
            H = DominatingSets.min_connected_dominating_sets_non_distributed(G)
            CDS = G.subgraph(H)
            print(f"CDS with possible loops is a {CDS}")
            # print(list(H.edges))
            print(f"Edges of CDS with possible loops are: {sorted(list(CDS.edges))}")
            CDS_no_loops = nx.minimum_spanning_tree(CDS)
            print(f"CDS with no loops is a {CDS_no_loops}")
            print(f"Edges of CDS with no loops are: {sorted(list(CDS_no_loops.edges))}")

            pos_G = nx.spring_layout(G)
            nx.draw(G, pos=pos_G, with_labels=True)
            nx.draw(CDS_no_loops, pos=pos_G, node_color="red")
            plt.show()

            LN_CDS = add_more_channels(G, CDS_no_loops)
            print(f"LN_CDS is a {LN_CDS}")
            print(f"Edges of LN_CDS are: {sorted(list(LN_CDS.edges))}")

            file = open("data/LN_topology_CDS_no_loops/" + filename, 'w+', newline='')

            with file:
                write = csv.writer(file)
                write.writerow(["source", "target"])
                write.writerows(sorted(list(LN_CDS.edges)))

        except:
            print(f"couldn't find a CDS for file {filename}")
            continue


if __name__ == '__main__':
    main()
