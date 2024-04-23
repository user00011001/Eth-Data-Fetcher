from web3 import Web3
from web3.exceptions import (
    ValidationError,
    InsufficientData,
    BlockNotFound
)

# Infura Project ID
INFURA_PROJECT_ID = 'your_infura_project_id_here'
w3 = Web3(Web3.HTTPProvider(f'https://mainnet.infura.io/v3/{INFURA_PROJECT_ID}'))

def fetch_block(block_number):
    """Attempt to fetch a block by its number."""
    try:
        return w3.eth.get_block(block_number)
    except (BlockNotFound, ValidationError) as e:
        print(f"Failed to fetch block {block_number}: {str(e)}")
        return None

def fetch_transaction(tx_hash):
    """Attempt to fetch a transaction by its hash."""
    try:
        return w3.eth.get_transaction(tx_hash)
    except (ValidationError, InsufficientData) as e:
        print(f"Failed to fetch transaction {tx_hash.hex()}: {str(e)}")
        return None

def print_transaction_details(tx_details, idx):
    """Prints details of a transaction, distinguishing between regular transactions and contract creations."""
    if tx_details['to']:
        print(f"\tTransaction {idx}: {tx_details['hash'].hex()} \n\tFrom: {tx_details['from']} \n\tTo: {tx_details['to']} \n\tAmount: {w3.from_wei(tx_details['value'], 'ether')} Ether\n")
    else:
        print(f"\tContract creation transaction {idx}: {tx_details['hash'].hex()} \n\tFrom: {tx_details['from']}\n")

def print_block_details(block_number):
    """Prints all transactions in a given block."""
    block = fetch_block(block_number)
    if not block:
        return

    print(f"\nBlock (Block Number: {block.number})")
    print(f"Number of transactions: {len(block.transactions)}")

    for idx, tx_hash in enumerate(block.transactions, start=1):
        tx_details = fetch_transaction(tx_hash)
        if tx_details:
            print_transaction_details(tx_details, idx)

def main():
    """Main function to fetch and print details of the last 10 blocks."""
    try:
        latest_block = w3.eth.block_number
    except ConnectionError:
        print("Failed to connect to the Ethereum network.")
        return

    for i in range(10):
        print_block_details(latest_block - i)

if __name__ == "__main__":
    main()
