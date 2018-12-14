import pandas as pd
import numpy as np
import json
from pprint import pprint
import operator

invalid_blocks = []
seen_ib = []
valid_txs = []
identities = {}
address_balances = {}
remaining_UTXOs = []
remaining_UTXOs_owners = {}
rc = 0

with open('TX_COMPLETE.json') as file:
    data = json.load(file)

def check_all():
        check(data)
        count = 1

        for block in range(1,len(invalid_blocks)):
            if invalid_blocks[block] == 97423:
                invalid_blocks[block] = -1
                print("I have forgiven block 97423 because its double spent input was from a block that I found to be invalid (204751). So I will consider 97423's spend valid.")
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
        # origCount(data)
        print("Blocks invalidated:",seen_ib)

def serialControlPure(data):
    identity_index = 0
    for tx in data['all']:
        for output in tx["output_addresses"]:
            identities[output] = -1
            address_balances[output] = 0
    for tx in data['all']:
        positive_out_count = 0
        linked_address = 0
        out_index = -1
        for output in tx["outputs"]:
            out_index += 1
            if output != 0:
                positive_out_count += 1
                linked_address = tx["output_addresses"][out_index]
        if positive_out_count == 1:
            address_balances[tx["output_addresses"][out_index]] += tx["output_values"][out_index]
            for input in tx["input_addresses"]:
                if identities[input] != -1:
                    identities[linked_address] = identities[input]
                elif identities[linked_address] != -1:
                    identities[input] = identities[linked_address]
                else:
                    identities[linked_address] = identity_index
                    identities[input] = identity_index
                    identity_index += 1
    unique = []
    for address in identities:
        if identities[address] not in unique:
            unique.append(identities[address])
    print(unique)

outputTransactionDict = {}
AddressOfUTXOs = {}
balanceOfUTXOs = {}
accounts = {}
aliasesToMainAccounts = {}
account_balances = {}

def findEntity():
    addresses =[139024,138183,139024,138183,139024,138183,139024,138183,139024,138183,139024,138183,139024,138183,139024,138183,139024,138183]

    with open('TX_COMPLETE.json') as file:
        data = json.load(file)
    ValueOfAddresses = {} # The balance of particular addresses (address: value)
    # UTXO { id, balance, address paid toward}
    for UTXO in remaining_UTXOs: # Address of UTXO remaining.
        address = UTXO[2]
        ValueOfAddresses[address] = 0
        AddressOfUTXOs[UTXO[0]] = UTXO[2]
    for UTXO in remaining_UTXOs: # Total value of an address.
        address = UTXO[2]
        ValueOfAddresses[address] += UTXO[1]

    for tx in valid_txs:
        for output_address in tx["output_addresses"]:
            outputTransactionDict[output_address] = tx["txid"]

    for address in ValueOfAddresses:
        accounts[address] = []
        addToAccount(address, accounts[address])

    for address in ValueOfAddresses:
        txid = outputTransactionDict[address]
        tx = data["all"][txid-1]
        outcount = 0
        for output_val in tx["output_values"]:
            if output_val > 0:
                outcount += 1
        if outcount == 1:
            for input_address in tx["input_addresses"]:
                    addToAccount(input_address, accounts[address])

    for address in accounts:
        account_balances[address] = 0
        for alias in accounts[address]:
            if alias in ValueOfAddresses:
                account_balances[address] += ValueOfAddresses[alias]

    for address in accounts:
        for alias in accounts[address]:
            aliasesToMainAccounts[alias] = address

    for address in addresses:
        if address in aliasesToMainAccounts:
            print(aliasesToMainAccounts[address])

def idiomsBacktrace():
    with open('TX_COMPLETE.json') as file:
        data = json.load(file)
    ValueOfAddresses = {} # The balance of particular addresses (address: value)
    # UTXO { id, balance, address paid toward}
    for UTXO in remaining_UTXOs: # Address of UTXO remaining.
        address = UTXO[2]
        ValueOfAddresses[address] = 0
        AddressOfUTXOs[UTXO[0]] = UTXO[2]
    for UTXO in remaining_UTXOs: # Total value of an address.
        address = UTXO[2]
        ValueOfAddresses[address] += UTXO[1]

    for tx in valid_txs:
        for output_address in tx["output_addresses"]:
            outputTransactionDict[output_address] = tx["txid"]

    for address in ValueOfAddresses:
        accounts[address] = []
        addToAccount(address, accounts[address])

    for address in ValueOfAddresses:
        txid = outputTransactionDict[address]
        tx = data["all"][txid-1]
        outcount = 0
        for output_val in tx["output_values"]:
            if output_val > 0:
                outcount += 1
        if outcount == 1:
            for input_address in tx["input_addresses"]:
                    addToAccount(input_address, accounts[address])


    for address in ValueOfAddresses:
        for n in range(1,300000):
            if len(accounts[address]) > n:
                txid = accounts[address][n]
                tx = data["all"][txid-1]
                outcount = 0
                for output_val in tx["output_values"]:
                    if output_val > 0:
                        outcount += 1
                if outcount == 1:
                    for input_address in tx["input_addresses"]:
                            addToAccount(input_address, accounts[address])

    for address in accounts:
        account_balances[address] = 0
        for alias in accounts[address]:
            if alias in ValueOfAddresses:
                account_balances[address] += ValueOfAddresses[alias]

    maxbalance = 0
    accounthead = 0
    count = 0
    for account in account_balances:
        if account_balances[account] > maxbalance:
            count = 0
            maxbalance = account_balances[account]
            accounthead = account
        elif account_balances[account] == maxbalance:
            count += 1
    if count > 0:
        print("More than one leader.")
    print("Max account header:",accounthead,":",maxbalance)

    minaddress = 99999999
    for alias in accounts[accounthead]:
        if alias < minaddress:
            minaddress = alias
    print("Min address of that account:", minaddress)

    for address in accounts:
        for alias in accounts[address]:
            aliasesToMainAccounts[alias] = address

    bestSender = -1
    currentHigh = 0
    bestTx = -1

    for alias in accounts[accounthead]:
        txid = outputTransactionDict[alias]
        tx = data["all"][txid-1]
        ind = -1
        for output_address in tx["output_addresses"]:
            one_sender = True
            sender = -1
            idx = 0
            ind += 1
            for input_address in tx["input_addresses"]:
                if idx > 0 and sender!=aliasesToMainAccounts[input_address]:
                    one_sender = False
                print(input_address, "->",output_address,"Value:",tx["output_values"][ind])
                sender = aliasesToMainAccounts[input_address]
                idx += 1
            if one_sender == True and sender != aliasesToMainAccounts[output_address] and tx["output_values"][ind] > currentHigh:
                currentHigh = tx["output_values"][ind]
                bestSender = sender
                bestTx = tx

    print(accounts[accounthead])



def addToAccount(address, account):
    account.append(address)

def lastBlockCount(data):
    for tx in data['all']:
        if tx["block"] not in seen_ib:
            valid_txs.append(tx)
    seen_UTXOs = {}
    spentOrNot = {}
    for tx in valid_txs:
        count = 0
        for output in tx["outputs"]:
            seen_UTXOs[output] = tx["output_values"][count]
            spentOrNot[output] = 'unspent'
            remaining_UTXOs_owners[output] = tx["output_addresses"][count]
            count += 1
        count = 0
    # print(len(seen_UTXOs), "UTXOs remaining...")

    # max_UTXO = max(seen_UTXOs.items(), key=operator.itemgetter(1))
    # print("Max", max_UTXO)

    for tx in valid_txs:
        for input in tx["inputs"]:
             spentOrNot[input] = 'spent'
    for UTXO in spentOrNot:
        if spentOrNot[UTXO] == 'unspent':
            remaining_UTXOs.append([UTXO,seen_UTXOs[UTXO],remaining_UTXOs_owners[UTXO]])

    print("There are", len(remaining_UTXOs)," unspent TXOs left as of last block.")
    max_value = 0
    max_set = []
    for utxo in remaining_UTXOs:
        if utxo[1] > max_value:
            max_set = []
            max_set.append(utxo[0])
            max_value = utxo[1]
        elif utxo[1] == max:
            max_set.append(utxo[0])

    print("Max value", max_value, " of UTXOs:", max_set)


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

def check(data):
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

# check_all()

# idiomsBacktrace()

findEntity()
