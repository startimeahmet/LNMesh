import pandas as pd
import config


def preprocess_data(f_name):
    data = pd.read_csv("data/csvfiles/" + f_name)

    new_df = pd.DataFrame()
    for i in range(config.NUM_NODES):
        data2 = data[data['node'] == i]
        for j in range(int(config.SIM_DURATION/config.TIME_PERIOD)):
            row = data2[data2['time'] <= config.TIME_PERIOD*60*(j+1)].tail(1)
            new_df = pd.concat([new_df, row])

    print(new_df)
    new_df.to_csv("data/csvfiles_preprocessed/" + f_name, index=False)


if __name__ == '__main__':
    for n in range(1, 41):
        print(f"Scenario {n}")
        filename = "100nodes_6hr/scenario" + str(n) + ".csv"
        # filename = "200nodes_6hr/scenario" + str(n) + ".csv"
        # filename = "300nodes_6hr/scenario" + str(n) + ".csv"
        preprocess_data(filename)

