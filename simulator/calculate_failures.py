
if __name__ == '__main__':
    N_TRANSACTIONS = [20, 30, 40, 50, 60, 70, 80, 90, 100]
    TOTAL_INVESTMENT = [50000, 100000, 200000, 300000, 400000]

    # directory = "experiment_results/100nodes_6hr_baseline/"
    # directory = "experiment_results/200nodes_6hr_baseline/"
    # directory = "experiment_results/300nodes_6hr_baseline/"
    # directory = "experiment_results/100nodes_6hr_CDS_no_loops/"
    # directory = "experiment_results/200nodes_6hr_CDS_no_loops/"
    # directory = "experiment_results/300nodes_6hr_CDS_no_loops/"
    # directory = "experiment_results/100nodes_6hr_UST/"
    # directory = "experiment_results/200nodes_6hr_UST/"
    directory = "experiment_results/300nodes_6hr_UST/"

    no_mesh_path = 0
    no_ln_path = 0
    not_enough_cap = 0
    successful_payments = 0

    for i in TOTAL_INVESTMENT:
        temp = []
        for j in N_TRANSACTIONS:
            f_name = "N_TRANSACTIONS_" + str(j) + "_TOTAL_INVESTMENT_" + str(i) + ".log"

            with open(directory + f_name, 'r') as f:
                data = f.read()

                no_mesh_path += data.count('no mesh path')
                no_ln_path += data.count('no LN path')
                not_enough_cap += data.count('not enough capacity')
                successful_payments += data.count('was successful')

    total_failed = no_mesh_path + no_ln_path + not_enough_cap
    total_payments = total_failed + successful_payments
    print(total_payments)
    print(f"no mesh path: {no_mesh_path}, no ln path: {no_ln_path},"
          f" not enough cap: {not_enough_cap}, successful: {successful_payments},"
          f" total_failed: {total_failed}, total_payments: {successful_payments+total_failed}")

    print(f"no mesh path: {100*(no_mesh_path/total_failed)}, no ln path: {100*(no_ln_path/total_failed)},"
          f" not enough cap: {100*(not_enough_cap/total_failed)}")

    print(f"new result: no mesh path: {100 * (no_mesh_path / total_payments)}, no ln path: {100 * (no_ln_path / total_payments)},"
          f" not enough cap: {100 * (not_enough_cap / total_payments)}")

