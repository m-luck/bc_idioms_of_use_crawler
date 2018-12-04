import pandas as pd
import numpy as np
import json
from pprint import pprint

def check_all():
    with open('TX_COMPLETE.json') as file:
        data = json.load(file)
        inputsLessThanOutputs(data)
        doubleSpend(data)
        duplicateInUTXO(data)
        duplicateOutUTXO(data)
        # duplicateAddressFromCoinbase(data)
        noOutputs(data)
        noInputs(data)

def inputsLessThanOutputs(data):
    count = 1
    for tx in data['all']:
        if tx["cb"]==0:
            input_sum = 0
            output_sum = 0
            for inp in tx["input_values"]:
                input_sum += inp
            for out in tx["output_values"]:
                output_sum += out

            if input_sum < output_sum:
                print(f'TX {count} in block {tx["block"]} has erroneous inputs because {input_sum} < {output_sum}. cb is {tx["cb"]}.')
        count+=1

def doubleSpend(data):
    count = 1
    inputs = {}
    for tx in data['all']:
        if tx["cb"]==0:
            for UTXO in tx["inputs"]:
                inputs[UTXO] = 'unspent'
    for tx in data['all']:
        if tx["cb"]==0:
            for UTXO in tx["inputs"]:
                if inputs[UTXO] == 'spent':
                    print(f'TX {count} in block {tx["block"]} may be a double spend.')
                else:
                    inputs[UTXO] = 'spent'
        count+=1

def duplicateOutUTXO(data):
    count = 1
    outputs = {}
    for tx in data['all']:
        for UTXO in tx["outputs"]:
            outputs[UTXO] = 'unseen'
    for tx in data['all']:
        for UTXO in tx["outputs"]:
            if outputs[UTXO] == 'seen':
                print(f'TX {count} in block {tx["block"]} hosts an output seen multiple times.')
            else:
                outputs[UTXO] = 'seen'
        count+=1

def duplicateInUTXO(data):
    count = 1
    outputs = {}
    for tx in data['all']:
        for UTXO in tx["inputs"]:
            outputs[UTXO] = 'unseen'
    for tx in data['all']:
        for UTXO in tx["inputs"]:
            if outputs[UTXO] == 'seen':
                print(f'TX {count} in block {tx["block"]} hosts an input seen multiple times.')
            else:
                outputs[UTXO] = 'seen'
        count+=1

def duplicateAddressFromCoinbase(data):
    count = 1
    output_addresses = {}
    for tx in data['all']:
        if tx["cb"]==1:
            for pk_id in tx["output_addresses"]:
                output_addresses[pk_id] = 'unseen'
    for tx in data['all']:
        if tx["cb"]==1:
            for pk_id in tx["output_addresses"]:
                if output_addresses[pk_id] == 'seen':
                    print(f'TX {count} in block {tx["block"]} is a coinbase tx but with an old pk_id.')
                else:
                    output_addresses[pk_id] = 'seen'
        count+=1

def noOutputs(data):
    count = 1
    for tx in data['all']:
        out_count = 0
        for out in tx['outputs']:
            out_count+=1
        if out_count == 0:
            print('No outputs.')
        count+=1

def noInputs(data):
    count = 1
    for tx in data['all']:
        if tx["cb"]==0:
            in_count = 0
            for inp in tx['outputs']:
                in_count+=1
            if in_count == 0:
                print('No inputs.')
        count+=1

def aboveLegalLimit(data):
    legalLimit = 21
    count = 1
    for tx in data['all']:
        if tx["cb"]==0:
            input_sum = 0
            output_sum = 0
            for inp in tx["input_values"]:
                input_sum += inp
            for out in tx["output_values"]:
                output_sum += out

            if output_sum > 210:
                print(f'TX {count} in block {tx["block"]} has erroneous inputs because {input_sum} < {output_sum}. cb is {tx["cb"]}.')
        count+=1

def txStagger(data):
    count = 1
    for tx in data['all']:
        if tx["txid"]!=count:
            print(f'TX {count} in block {tx["block"]} staggers.')
        count+=1

def coinbaseWithInput(data):
    count = 1
    for tx in data['all']:
        if tx["cb"] == 1:
            inp_count = 0
            for inp in tx["inputs"]:
                inp_count+=1
            if inp_count > 0:
                print(f'TX {count} in block {tx["block"]} should not have any inputs.')
        count+=1

def coinbaseWithWrongReward(data):
    count = 1
    for tx in data['all']:
        if tx["cb"] == 1:
            if tx["value"] != 0:
                print(f'TX {count} in block {tx["block"]} should not have any inputs.')
        count+=1

check_all()
