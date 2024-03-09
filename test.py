import random
import string
from block import Block, Blockchain
from tqdm import tqdm

def generate_random_data(length=32):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

def test_blockchain_performance(blockchain_name='test'):
    blockchain = Blockchain(blockchain_name)
    num=int(input('测试数量：'))
    print(f"开始在{blockchain.name}区块链上添加个{num}随机区块...")
    
    with tqdm(total=num) as pbar:
        for i in range(num):
            data = generate_random_data()
            blockchain.add_block(data)
            pbar.update(1)

    print("\n区块添加完成。")
    print(f"{blockchain.name}区块链当前包含 {len(blockchain.chain)} 个区块。")
    print("验证区块链的有效性...")
    if blockchain.is_chain_valid():
        print(f"{blockchain.name} 区块链有效且未被篡改。")
    else:
        print(f"警告：{blockchain.name} 区块链无效或已被篡改！")

if __name__ == "__main__":
    test_blockchain_performance()