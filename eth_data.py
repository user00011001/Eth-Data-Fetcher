import os
from web3 import Web3
from web3.exceptions import (
    ConnectionError,
    HTTPError,
    ValidationError,
    InsufficientData,
    BlockNotFound
)

# Get your Infura ID from environment variable
INFURA_PROJECT_ID = os.getenv('INFURA_PROJECT_ID')
if INFURA_PROJECT_ID is None:
    raise ValueError("Missing Infura project ID")

w3 = Web3(Web3.HTTPProvider(f'https://mainnet.infura.io/v3/{INFURA_PROJECT_ID}'))

def get_block_details(block_number):
    try:
        return w3.eth.get_block(block_number)
    except (BlockNotFound, ValidationError):
        print(f"Failed to fetch block {block_number}")
        return None

def get_transaction_details(tx):
    try:
        return w3.eth.get_transaction(tx)
    except (ValidationError, InsufficientData):
        print(f"Failed to fetch transaction {tx}")
        return None

def print_transaction_details(tx_details, idx):
    if tx_details['to']:  # If the transaction was a regular transaction, not a contract creation.
        print(
            f"\tTransaction {idx}: {tx_details['hash'].hex()} \n\tFrom: {tx_details['from']} \n\tTo: {tx_details['to']} \n\tAmount: {w3.from_wei(tx_details['value'], 'ether')} Ether\n")
    else:  # If the transaction was a contract creation.
        print(
            f"\tContract creation transaction {idx}: {tx_details['hash'].hex()} \n\tFrom: {tx_details['from']}\n")

def print_block_details(latest_block, i):
    block = get_block_details(latest_block - i)
    if block is None:
        return

    print(f"\nBlock {i+1} (Block Number: {block.number})")
    print(f"Number of transactions: {len(block.transactions)}")

    # Iterating through all the transactions in the block.
    for idx, tx in enumerate(block.transactions, start=1):
        tx_details = get_transaction_details(tx)
        if tx_details is None:
            continue
        print_transaction_details(tx_details, idx)

def main():
    try:
        # Getting the latest block number in the Ethereum blockchain.
        latest_block = w3.eth.block_number
    except ConnectionError:
        print("Failed to connect to the Ethereum network")
        return

    # Iterating through the last 10 blocks.
    for i in range(10):
        print_block_details(latest_block, i)

if __name__ == "__main__":
    main()
