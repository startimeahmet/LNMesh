import argparse

TIME_PERIOD = 10  # how often we get the locations of the nodes from bonnmotion data. e.g., every 10 minutes
SIM_DURATION = 360  # how long is the simulation in minutes
NUM_NODES = 100  # number of nodes extracted from bonnmotion
LN_CUTOFF = 5  # the metric to choose how to open LN channels based on node distances
COVERAGE = 90  # wireless coverage of the nodes

# uncomment below for simulations

# parser = argparse.ArgumentParser()
#
# parser.add_argument('--N_TRANSACTIONS', type=int, required=True)
# parser.add_argument('--TOTAL_INVESTMENT', type=int, required=True)
# args = parser.parse_args()
# print('N_TRANSACTIONS,', args.N_TRANSACTIONS)
# N_TRANSACTIONS = args.N_TRANSACTIONS
# print('TOTAL_INVESTMENT,', args.TOTAL_INVESTMENT)
# TOTAL_INVESTMENT = args.TOTAL_INVESTMENT
