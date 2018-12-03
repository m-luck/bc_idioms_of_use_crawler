import csv
import pandas as pd

txs = pd.read_csv('transactions.csv');
# 0 id 1 block_id 2 is_coinbase
ins = pd.read_csv('inputs.csv');
# 0 id 1 tx_id 2 output_id
outs = pd.read_csv('outputs.csv');
# 0 id 1 tx_id 2 pk_id 3 value


def testLegalLimit():
    for index,row in txs.iterrows():
        if row[2]==0: # Production code, same indent.
            totalOut = 0
        # if row[2]==0 and 505 == row[0]: # Truncate arguments for testing.

            # print(f'\nTesting transaction {row[0]}')

            # Get a subset of inputs that belong to the current transaction.
            tx_id = row[0]
            # These are the outputs of the transaction.
            subOuts = outs.query(f'partOfTX == {tx_id}')


            for indexo,rowo in subOuts.iterrows():
                # Add the value of the output to the totalOutput.
                totalOut += rowo[3]

            if (totalOut>2100000000000000):
                print(f'\nTransaction {row[0]} above legal limit')



testLegalLimit()
