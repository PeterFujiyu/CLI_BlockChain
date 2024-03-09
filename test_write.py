from block import *

def tamper_with_blockchain(blockchain_name, tampered_block_index, new_data):
    blockchain = Blockchain(blockchain_name)
    
    if tampered_block_index >= len(blockchain.chain) or tampered_block_index < 0:
        print(f"无效的区块索引: {tampered_block_index}. 请确保它在区块链范围内.")
        return
    
    tampered_block = blockchain.chain[tampered_block_index]
    tampered_block.data = new_data
    tampered_block.hash = tampered_block.calculate_hash()

    blockchain.save_blockchain()

    print(f"成功篡改了区块{tampered_block_index}的数据为: {new_data}")

    if not blockchain.is_chain_valid():
        print("篡改后区块链不再有效！")
    else:
        print("篡改后区块链仍然有效，但数据已更改。")

def test_tampering():
    blockchain_name = input("请输入要篡改的区块链名称:")
    tampered_block_index = int(input("请输入要篡改的区块索引（从0开始）: "))
    new_data = input("请输入新的区块数据: ")

    tamper_with_blockchain(blockchain_name, tampered_block_index, new_data)

if __name__ == "__main__":
    test_tampering()