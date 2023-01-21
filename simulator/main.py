
import config
from node import *
import networkx as nx
import matplotlib.pyplot as plt
import random

from itertools import tee
from math import sqrt
import itertools
import numpy as np
import pandas as pd
import time

allChannels = []
G_ln = nx.Graph()
G_mesh = nx.Graph()

success_rate = [0, 0]


def pairwise(iterable):
    """s -> (s0,s1), (s1,s2), (s2, s3), ..."""
    a, b = tee(iterable)
    next(b, None)
    return zip(a, b)


# functions creating LN and mesh network

def ln_network(ln_file):
    data = pd.read_csv(ln_file)
    print(f'ln path {ln_file}')
    print(f'shape of the data {data.shape}')

    for index, row in data.iterrows():
        G_ln.add_edge(int(row['source']), int(row['target']))

    print(f"ln nodes data: {G_ln}")
    return G_ln


def mesh_network(mesh_file, t):
    data = pd.read_csv(mesh_file)

    data2 = data[(data['time'] == t) & (data['distance'] <= config.COVERAGE)]

    for index, row in data2.iterrows():
        G_mesh.add_edge(int(row['source']), int(row['target']))

    return G_mesh


def transaction_list(num_tx, sub_round, main_round):
    list_nodes = list(range(config.NUM_NODES))
    combinations = pd.DataFrame(list(itertools.combinations(list_nodes, 2)))
    tx_list = combinations.sample(n=num_tx, replace=True, random_state=42+sub_round+main_round)
    tx_list = tx_list.values.tolist()
    # print(f"Transaction list {transaction_list}")
    return tx_list


def check_ln_path(item):
    try:
        path = nx.dijkstra_path(G_ln, item[0], item[1])
    except:
        path = []
    return path


def check_mesh_path(item):
    path_ln = check_ln_path(item)
    path = []
    if len(path_ln) != 0:
        for v, w in pairwise(path_ln):
            try:
                path2 = nx.dijkstra_path(G_mesh, v, w)
                path.append(path2)
            except:
                return []
    return path


def transaction(item, amount):
    path_ln = check_ln_path(item)
    path_mesh = check_mesh_path(item)

    if len(path_ln) != 0:
        print(f"The LN path found between {item[0]} and {item[1]} is {path_ln}")
        if len(path_mesh) != 0:
            print(f"The mesh path found between {item[0]} and {item[1]} is {path_mesh}")
            payment_status = try_payment(path_ln, amount)
            if payment_status == 0:
                return 0
            else:
                print(f"The transaction between {item[0]} and {item[1]} in the amount of {amount} was successful at {time.time()}")
                return 1
        else:
            print(f"The transaction between {item[0]} and {item[1]} in the amount of {amount} satoshi failed at {time.time()}. There is no mesh path between the nodes")
            return 0
    else:
        print(f"The transaction between {item[0]} and {item[1]} in the amount of {amount} satoshi failed at {time.time()}. There is no LN path between the nodes")
        return 0


def try_payment(path, amount):
    flag = 1
    for v, w in pairwise(path):
        for channel in allChannels:
            if channel.nodeA == v and channel.nodeB == w:
                if channel.capacityA >= float(amount):
                    channel.capacityA = channel.capacityA - amount
                    channel.capacityB = channel.capacityB + amount
                else:
                    print(f"The transaction between {v} and {w} in the amount of {amount} satoshi failed at {time.time()}. There is not enough capacity")
                    flag = 0
                    return flag
            elif channel.nodeB == v and channel.nodeA == w:
                if channel.capacityB >= float(amount):
                    channel.capacityA = channel.capacityA + amount
                    channel.capacityB = channel.capacityB - amount
                else:
                    print(f"The transaction between {v} and {w} in the amount of {amount} satoshi failed at {time.time()}. There is not enough capacity")
                    flag = 0
                    return flag
            else:
                pass
    if flag == 1:
        return flag


def single_run(mesh_path, ln_path, data_round):

    ln_network(ln_path)

    capacityA = round(config.TOTAL_INVESTMENT / len(G_ln.edges))
    capacityB = round(config.TOTAL_INVESTMENT / len(G_ln.edges))

    for i in range(len(G_ln.edges)):
        allChannels.append(Channel(list(G_ln.edges)[i][0], list(G_ln.edges)[i][1], capacityA, capacityB))

    for j in range(int(config.SIM_DURATION/config.TIME_PERIOD)):  # j is the subrounds, or current SIM TIME

        current_sim_time = (j+1)*60*config.TIME_PERIOD
        mesh_network(mesh_path, current_sim_time)

        tr_list = transaction_list(config.N_TRANSACTIONS, j, data_round)
        print(f'The transaction list: {tr_list}')

        for item in tr_list: 
            try:
                amount_list = [1, 5, 10, 20, 50, 100]
                random.seed(item[0])
                amount = random.choice(amount_list)
                result = transaction(item, amount)
                if result == 0:
                    success_rate[0] += 1
                else:
                    success_rate[1] += 1
            except:
                success_rate[0] += 1
                print(f"Transaction failed, the transaction amount or the transactions nodes are incorrect!")


def main():
    my_list = list(range(1, 41))
    # uncomment for 100 nodes
    # list.remove(my_list, 28)
    # list.remove(my_list, 34)
    # list.remove(my_list, 37)
    # uncomment for 200 nodes
    # list.remove(my_list, 1)
    # list.remove(my_list, 2)
    # list.remove(my_list, 13)
    # uncomment for 300 nodes
    # list.remove(my_list, 1)
    # list.remove(my_list, 2)
    # list.remove(my_list, 3)
    
    for k in my_list:
        allChannels.clear()
        G_ln.clear()
        G_mesh.clear()
        ln_files = "data/LN_topology_baseline/100nodes_6hr/scenario" + str(k) + ".csv"  # baseline
        # ln_files = "data/LN_topology_baseline/200nodes_6hr/scenario" + str(k) + ".csv"  # baseline
        # ln_files = "data/LN_topology_baseline/300nodes_6hr/scenario" + str(k) + ".csv"  # baseline
        # ln_files = "data/LN_topology_CDS_no_loops/100nodes_6hr/scenario" + str(k) + ".csv"   # CDS
        # ln_files = "data/LN_topology_CDS_no_loops/200nodes_6hr/scenario" + str(k) + ".csv"   # CDS
        # ln_files = "data/LN_topology_CDS_no_loops/300nodes_6hr/scenario" + str(k) + ".csv"   # CDS
        # ln_files = "data/LN_topology_UST/100nodes_6hr/scenario" + str(k) + "/UST1"    # UST
        # ln_files = "data/LN_topology_UST/200nodes_6hr/scenario" + str(k) + "/UST1"    # UST
        # ln_files = "data/LN_topology_UST/300nodes_6hr/scenario" + str(k) + "/UST1"    # UST

        mesh_files = "data/distances/100nodes_6hr/scenario" + str(k) + ".csv"
        # mesh_files = "data/distances/200nodes_6hr/scenario" + str(k) + ".csv"
        # mesh_files = "data/distances/300nodes_6hr/scenario" + str(k) + ".csv"

        single_run(mesh_files, ln_files, k)
        print(f'+--------------DATA ROUND {k} IS COMPLETED SUCCESSFULLY----------------------+')

    print('+---------------SIMULATION COMPLETED----------------+')
    print('+--------------------------------------+')
    print('+--------------------------------------+')
    print('|Lightning Network Simulator|')
    print('+--------------------------------------+')
    print('Version v3.1')
    print('Hadi Sahin')
    print('Ahmet Kurt')
    print('Kemal Akkaya')
    print('+--------------------------------------+')

    print(f"Result: {success_rate}, with success rate %{100*success_rate[1]/(success_rate[0]+success_rate[1])}")


if __name__ == '__main__':
    main()
