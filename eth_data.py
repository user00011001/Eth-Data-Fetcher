from web3 import Web3

w3 = Web3(Web3.HTTPProvider('https://mainnet.infura.io/v3/Your-Infura-Project-Id'))

latest_block = w3.eth.block_number

for i in range(10):
    block = w3.eth.get_block(latest_block - i)
    print(f"\nBlock {i+1} (Block Number: {block.number})")
    print(f"Number of transactions: {len(block.transactions)}")

    for idx, tx in enumerate(block.transactions, start=1):
        tx_details = w3.eth.get_transaction(tx)

        if tx_details['to']:
            print(
                f"\tTransaction {idx}: {tx_details['hash'].hex()} \n\tFrom: {tx_details['from']} \n\tTo: {tx_details['to']} \n\tAmount: {w3.from_wei(tx_details['value'], 'ether')} Ether\n")
        else:
            print(
                f"\tContract creation transaction {idx}: {tx_details['hash'].hex()} \n\tFrom: {tx_details['from']}\n")
