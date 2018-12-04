import csv
import pandas as pd
import numpy as np

txs = pd.read_csv('transactions.csv');
# 0 id 1 block_id 2 is_coinbase
ins = pd.read_csv('inputs.csv');
# 0 id 1 tx_id 2 output_id
outs = pd.read_csv('outputs.csv');
# 0 id 1 tx_id 2 pk_id 3 value

def generate():
    '''
    Generate a full transaction for every transaction (including inputs and outputs), for easier parsing
    '''
    transactions = {}
    # For every transaction
    for index,row in txs.iterrows():
        #Find the outputs of that transaction:
        subOuts = outs.query(f'partOfTX == {row[0]}')
        subIns = ins.query(f'partOfTX == {row[0]}')
        placeholder = subIns

        subIns = pd.DataFrame()
        for indexp,rowp in placeholder.iterrows():
            subIns = subIns.append(outs.query(f'UTXO_ID == {rowp[2]}'))

        tx_outs = subOuts['UTXO_ID'].tolist()
        tx_out_values = subOuts['value'].tolist()
        tx_out_address = subOuts['pk_id'].tolist()

        if not subIns.empty:
            tx_ins = subIns['UTXO_ID'].tolist()
            tx_in_values = subIns['value'].tolist()
            tx_in_address = subIns['pk_id'].tolist()
            transactions[row[0]] = {'txid':row[0], 'block': row[1], 'cb':row[2],'inputs':tx_ins, 'input_addresses': tx_in_address, 'input_values':tx_in_values, 'outputs':tx_outs, 'output_addresses':tx_out_address, 'output_values':tx_out_values}
        else:
            transactions[row[0]] = {'txid':row[0], 'block': row[1], 'cb':row[2], 'inputs':[], 'input_values':[], 'input_addresses': [],'outputs':tx_outs, 'output_addresses':tx_out_address, 'output_values': tx_out_values}

        print(transactions[row[0]])

generate()
