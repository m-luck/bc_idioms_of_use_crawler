import csv
import pandas as pd

txs = pd.read_csv('transactions.csv');
# 0 id 1 block_id 2 is_coinbase
ins = pd.read_csv('inputs.csv');
# 0 id 1 tx_id 2 output_id
outs = pd.read_csv('outputs.csv');
# 0 id 1 tx_id 2 pk_id 3 value
def inputsMatchOutputs():
    for index,row in txs.iterrows():
        #if row[2]==0: # Production code, same indent.
        if row[2]==0 and 200 < row[0] < 300: # Truncate arguments for testing.

            print(f'\nTesting transaction {row[0]}')

            # Get a subset of inputs that belong to the current transaction.
            subIns = ins.query(f'partOfTX == {row[0]}')

            # Keep it in a key.
            placeholder = subIns

            # We are going to match these inputs to the referred outputs.
            for indexp,rowp in placeholder.iterrows():

                # Get a subset of outputs that are referred to by these inputs. Put these back into new subIns.
                subIns = outs.query(f'UTXO_ID == {rowp[2]}')

            # These are the outputs of the transaction.
            subOuts = outs.query(f'partOfTX == {row[1]}')

            # Counters to add to, making sure the input is never more than the output.
            totalIn = 0
            totalOut = 0

            for indexi,rowi in subIns.iterrows():
                # Add the value of the input to the totalInput.
                totalIn += rowi[3]


            for indexo,rowo in subOuts.iterrows():
                # Add the value of the output to the totalOutput.
                totalOut += rowo[3]

            print("Input sum:",totalIn, "vs", "Output sum:",totalOut)

            if (totalIn < totalOut):
                print('Aha!')

inputsMatchOutputs()
