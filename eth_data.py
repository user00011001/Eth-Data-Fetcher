# Importing the Web3 module from the web3 library.
from web3 import Web3

# Creating a Web3 instance by connecting to the Ethereum mainnet via Infura.
# Replace 'Your-Infura-Project-Id' with your actual Infura project ID.
w3 = Web3(Web3.HTTPProvider('https://mainnet.infura.io/v3/Your-Infura-Project-Id'))

# Getting the latest block number in the Ethereum blockchain.
latest_block = w3.eth.block_number

# Iterating through the last 10 blocks.
for i in range(10):
    # Getting block details of the ith previous block from the latest one.
    block = w3.eth.get_block(latest_block - i)
    print(f"\nBlock {i+1} (Block Number: {block.number})")
    print(f"Number of transactions: {len(block.transactions)}")

    # Iterating through all the transactions in the block.
    for idx, tx in enumerate(block.transactions, start=1):
        # Getting the details of the transaction.
        tx_details = w3.eth.get_transaction(tx)

        # If the transaction was a regular transaction, not a contract creation.
        if tx_details['to']:
            print(
                f"\tTransaction {idx}: {tx_details['hash'].hex()} \n\tFrom: {tx_details['from']} \n\tTo: {tx_details['to']} \n\tAmount: {w3.from_wei(tx_details['value'], 'ether')} Ether\n")
        else:  # If the transaction was a contract creation.
            print(
                f"\tContract creation transaction {idx}: {tx_details['hash'].hex()} \n\tFrom: {tx_details['from']}\n")
