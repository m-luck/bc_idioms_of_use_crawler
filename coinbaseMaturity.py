import csv
import pandas as pd

txs = pd.read_csv('transactions.csv');
# 0 id 1 block_id 2 is_coinbase
ins = pd.read_csv('inputs.csv');
# 0 id 1 tx_id 2 output_id
outs = pd.read_csv('outputs.csv');
# 0 id 1 tx_id 2 pk_id 3 value


def testMaturity():
    # Find all transactions from coinbase and record inputs/outputs in hash map.
    cbtx = {}
    for index,row in txs.iterrows():
        if row[2]==1:
            if row[0] % 1000 == 0:
                print(row[0])
            cbtx[row[0]] = { 'output_id' : outs.query(f'partOfTX == {row[0]}').iloc[0][0], 'block':row[1] }


    print('Done with cbtx fillout.')

    for index,row in txs.iterrows():
        if row[2]==1:
            if row[0] % 1000 == 0:
                print(row[0])
            outid = cbtx[row[0]].get('output_id')
            inputsUsing = ins.query(f'UTXO_ID == { outid }')
            for indexi, rowi in inputsUsing.iterrows():
                currentTXofInput = txs.query(f'TXID == {rowi[1]}').iloc[0][1]
                creationTXofInput = cbtx[row[0]].get('block')
                print( currentTXofInput - (creationTXofInput + 100))
                if (currentTXofInput <= creationTXofInput + 100):
                    print(f'Check TX {rowi[1]}')


    # cbtx = outs.query('value == 5000000000')

    # Find the transactions that use them as inputs.



    # Check that these transactions are at least 100 blocks after the coinbase transaction.
testMaturity()
