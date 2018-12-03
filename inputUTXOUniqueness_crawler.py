import csv
import pandas as pd

txs = pd.read_csv('transactions.csv');
# 0 id 1 block_id 2 is_coinbase
ins = pd.read_csv('inputs.csv');
# 0 id 1 tx_id 2 output_id
outs = pd.read_csv('outputs.csv');
# 0 id 1 tx_id 2 pk_id 3 value


def UTXOUnique():
    checkboxes = {}
    for index,row in ins.iterrows():
            checkboxes[f"{row[2]}"] = -1
    for index,row in outs.iterrows():
            checkboxes[f"{row[0]}"] = 0
    for index,row in ins.iterrows():
        if checkboxes[f"{row[2]}"] == 1:
            print(f"Ah! {row[2]} spent twice")
        else:
            checkboxes[f"{row[2]}"] = 1
        if checkboxes[f"{row[2]}"] == -1:
            print(f"Ah! {row[2]} Doesn't exist")


UTXOUnique()
