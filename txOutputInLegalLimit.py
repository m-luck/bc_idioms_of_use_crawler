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
        # if row[2]==0 and 505 == row[0]: # Truncate arguments for testing.

            # print(f'\nTesting transaction {row[0]}')

            # Get a subset of inputs that belong to the current transaction.
            tx_id = row[0]
            matchingIns = ins.query(f'partOfTX == {tx_id}')
            # print('PREIN',matchingIns)

            # We are going to match these inputs to the referred outputs.
            subIns = pd.DataFrame()
            for indexp,rowp in matchingIns.iterrows():

                # Get a subset of outputs that are referred to by these inputs. Put these back into new subIns.
                outid = rowp[2]
                subIns = subIns.append(outs.query(f'UTXO_ID == {outid}'))

            # These are the outputs of the transaction.
            subOuts = outs.query(f'partOfTX == {tx_id}')

            # Counters to add to, making sure the input is never more than the output.
            totalIn = 0
            totalOut = 0

            for indexi,rowi in subIns.iterrows():
                # Add the value of the input to the totalInput.
                totalIn += rowi[3]


            for indexo,rowo in subOuts.iterrows():
                # Add the value of the output to the totalOutput.
                totalOut += rowo[3]



            if (totalOut>2100000000000000 or totalIn>2100000000000000):
                print(f'\nTransaction {row[0]} above legal limit')



testLegalLimit()
