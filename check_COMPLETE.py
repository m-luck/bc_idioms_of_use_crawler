import pandas as pd
import numpy as np
import json
from pprint import pprint
import operator

invalid_blocks = []
seen_ib = []

def check_all():
    with open('TX_COMPLETE.json') as file:
        data = json.load(file)
        inputsLessThanOutputs(data)
        duplicateInUTXO(data)
        duplicateOutUTXO(data)
        # duplicateAddressFromCoinbase(data)
        noOutputs(data)
        noInputs(data)
        coinbaseWithInput(data)
        coinbaseWithWrongReward(data)
        multipleRewardsPerBlock(data)
        inputCreatedBeforeOutput(data)
        # addressNull(data)
        valueNull(data)
        count = 1

        for block in range(1,len(invalid_blocks)):
            if invalid_blocks[block] == 97423:
                invalid_blocks[block] = -1
        #
        comingFromInvalidBlock(data)
        # comingFromInvalidBlock(data)
        # comingFromInvalidBlock(data)
        # comingFromInvalidBlock(data)

        for block in invalid_blocks:
            if block not in seen_ib and block != -1:
                print(f'{count}. {block}')
                seen_ib.append(block)
                count += 1

        f = open("invalidBlocks.out","w+")
        for block in seen_ib:
            f.write(f"{block}\r\n")
        f.close()

        lastBlockCount(data)
        origCount(data)
        print(seen_ib)

def lastBlockCount(data):
    valid_txs = []
    for tx in data['all']:
        if tx["block"] not in seen_ib:
            valid_txs.append(tx)
    seen_UTXOs = {}
    for tx in valid_txs:
        count = 0
        for output in tx["outputs"]:
            seen_UTXOs[output] = tx["output_values"][count]
            count += 1
    print(len(seen_UTXOs), "UTXOs remaining...")

    max_UTXO = max(seen_UTXOs.items(), key=operator.itemgetter(1))
    print("Max", max_UTXO)

def origCount(data):
    seen_UTXOs = {}
    for tx in data['all']:
        count = 0
        for output in tx["outputs"]:
            seen_UTXOs[output] = tx["output_values"][count]
            count += 1
    print(len(seen_UTXOs), "originally.")
    max_UTXO = max(seen_UTXOs.items(), key=operator.itemgetter(1))
    print("Max", max_UTXO)

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
                invalid_blocks.append(tx["block"])
        count+=1

def duplicateOutUTXO(data):
    count = 1
    outputs = {}
    for tx in data['all']:
        for UTXO in tx["outputs"]:
            outputs[UTXO] = 'unseen'
        for UTXO in tx["inputs"]:
            outputs[UTXO] = 'unseen'
    for tx in data['all']:
        for UTXO in tx["outputs"]:
            if outputs[UTXO] == 'seen':
                print(f'TX {count} in block {tx["block"]} hosts an output seen multiple times.')
                invalid_blocks.append(tx["block"])
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
                print(f'TX {count} in block {tx["block"]} hosts an input seen multiple times (double spend) (input {UTXO}).')
                invalid_blocks.append(tx["block"])
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
                    invalid_blocks.append(tx["block"])
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
            invalid_blocks.append(tx["block"])
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
                invalid_blocks.append(tx["block"])
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
                invalid_blocks.append(tx["block"])
        count+=1

def txStagger(data):
    count = 1
    for tx in data['all']:
        if tx["txid"]!=count:
            print(f'TX {count} in block {tx["block"]} staggers.')
            invalid_blocks.append(tx["block"])
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
                invalid_blocks.append(tx["block"])
        count+=1

def coinbaseWithWrongReward(data):
    count = 1
    for tx in data['all']:
        if tx["cb"] == 1:
            value_total = 0
            for value in tx["output_values"]:
                value_total += value
            if value_total < 5000000000:
                print(f'TX {count} in block {tx["block"]} is a coinbase tx with a reward smaller than it should be.')
                invalid_blocks.append(tx["block"])
        count+=1


def multipleRewardsPerBlock(data):
    count = 1
    blocks = {}
    for tx in data['all']:
        if tx["cb"] == 1:
            blocks[tx["block"]] = 'unseen'
    for tx in data['all']:
        if tx["cb"] == 1:
            if blocks[tx["block"]] == 'seen':
                print(f'TX {count} in block {tx["block"]} is a duplicate coinbase reward of a block.')
                invalid_blocks.append(tx["block"])
            else:
                blocks[tx["block"]] = 'seen'
        count+=1

def addressNull(data):
    count = 1
    for tx in data['all']:
        for address in tx["output_addresses"]:
            if address > 0:
                ok = 1
            else:
                print(f'TX {count} in block {tx["block"]} goes to a null address.')
                invalid_blocks.append(tx["block"])
        for address in tx["input_addresses"]:
            if address > 0:
                ok = 1
            else:
                print(f'TX {count} in block {tx["block"]} comes from a null address.')
                invalid_blocks.append(tx["block"])
        count += 1

def valueNull(data):
    count = 1
    for tx in data['all']:
        for address in tx["output_values"]:
            if address >= 0:
                ok = 1
            else:
                print(f'TX {count} in block {tx["block"]} has an output that is invalid.')
                invalid_blocks.append(tx["block"])
        count += 1

def inputCreatedBeforeOutput(data):
    count = 1
    outputs = {}
    for tx in data['all']:
        for UTXO in tx["inputs"]:
            outputs[UTXO] = 'unseen'
    for tx in data['all']:
        for UTXO in tx["outputs"]:
            outputs[UTXO] = 'seen'
        for UTXO in tx["inputs"]:
            if outputs[UTXO] == 'unseen':
                print(f'TX {count} in block {tx["block"]} uses an input that has not been created in a previous transaction.')
                invalid_blocks.append(tx["block"])
        count += 1


def comingFromInvalidBlock(data):
    count = 1
    invalidated_inputs = []
    new_invalidated_blocks = []
    for tx in data['all']:
        if tx["block"] in invalid_blocks:
            for UTXO in tx["outputs"]:
                invalidated_inputs.append([UTXO,tx["block"]])
    for tx in data['all']:
        for UTXO in tx["inputs"]:
            for invalidInput in invalidated_inputs:
                if invalidInput[0] == UTXO:
                    new_invalidated_blocks.append([tx["block"], invalidInput[1], invalidInput[0]])
    tracker = -1
    for block in new_invalidated_blocks:
        if block != tracker and block[0]!=block[1]:
            print(f'Block {block[0]} is downstream of an invalid block ({block[1]}) because it uses output {block[2]} as input.')
            invalid_blocks.append(block[0])
            tracker = block

check_all()
