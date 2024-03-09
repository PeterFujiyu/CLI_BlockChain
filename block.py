import hashlib
import time
import json
import os
import pickle

import sys

class Block:
    def __init__(self, data, index=0, timestamp=None, previous_hash=""):
        """
        初始化区块对象。

        :param data: 区块中存储的数据。
        :param index: 区块的索引号。
        :param timestamp: 区块的时间戳，默认为当前时间。
        :param previous_hash: 前一个区块的哈希值，默认为空字符串。
        """
        self.index = index
        self.timestamp = timestamp or time.time()
        self.data = data
        self.previous_hash = previous_hash
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        """
        计算区块的哈希值。

        :return: 返回计算得到的哈希值。
        """
        block_data = pickle.dumps((self.index, self.timestamp, self.data, self.previous_hash))
        return hashlib.sha3_512(block_data).hexdigest()

class Blockchain:
    def __init__(self, name='default'):
        """
        初始化区块链对象。

        :param name: 区块链的唯一标识符，默认为'default'。
        """
        self.name = name  # 区块链的唯一标识符
        self.chain = []  # 初始化为空的区块链
        self.load_blockchain()  # 尝试从存储中加载区块链

    def create_genesis_block(self):
        """
        创建创世区块。

        :return: 返回创建的创世区块。
        """
        return Block("Genesis Block", 0, time.time(), "0")

    def add_block(self, data):
        """
        向区块链中添加一个区块。

        :param data: 要添加到区块中的数据。
        """
        # 对输入数据进行基本验证
        if not isinstance(data, str):
            raise ValueError("数据必须是字符串。")
        
        if not self.chain:
            self.chain.append(self.create_genesis_block())
        else:
            previous_block = self.chain[-1]
            new_block = Block(data, len(self.chain), time.time(), previous_block.hash)
            self.chain.append(new_block)
        self.save_blockchain()

    def print_blockchain(self):
        """
        打印整个区块链的信息。
        """
        for block in self.chain:
            print(f"区块 {block.index}:")
            print(f"数据: {block.data}")
            print(f"哈希: {block.hash}")
            print(f"前一哈希: {block.previous_hash}\n")
            print(f"时间戳: {block.timestamp}")
            
    def save_blockchain(self):
        """
        将区块链保存到JSON文件中。
        """
        chain_data = [block.__dict__ for block in self.chain]

        filename = f'blockchain_{self.name}.json'

        try:
            with open(filename, 'w') as f:  # 使用'w'模式以覆盖方式写入整个区块链
                json.dump(chain_data, f, indent=4)

        except IOError as e:
            print(f"保存区块链失败: {e}")

    def load_blockchain(self):
        """
        从JSON文件加载区块链。
        """
        filename = f'blockchain_{self.name}.json'

        try:
            if os.path.exists(filename):
                with open(filename, 'r') as f:
                    chain_data = json.load(f)

                loaded_chain = []
                for block_data in chain_data:
                    block = Block(block_data['data'], block_data['index'], block_data['timestamp'], block_data['previous_hash'])
                    loaded_chain.append(block)

                self.chain = loaded_chain

                # 检查区块链的有效性
                if not self.is_chain_valid():
                    print(f"警告：{self.name} 区块链在读取时发现被篡改或损坏！")
                else:
                    print(f"{self.name} 区块链成功加载。")

            else:
                # 只有在文件不存在时才创建并保存创世区块
                self.chain.append(self.create_genesis_block())
                self.save_blockchain()

        except IOError as e:
            print(f"加载区块链失败: {e}")

        except Exception as e:
            print(f"加载过程中发生错误: {e}")
            
    def is_chain_valid(self):
        """
        检查区块链是否有效。

        :return: 如果区块链有效返回True，否则返回False。
        """
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i - 1]

            if current_block.hash != current_block.calculate_hash():
                return False

            if current_block.previous_hash != previous_block.hash:
                return False

        return True
    
    def recompute_hashes(self):
        """
        重新计算整个区块链的哈希值。
        """
        import tqdm 
        with tqdm.tqdm(total=len(self.chain) - 1, desc="重新计算区块链哈希进度：") as pbar:
            for i in range(1, len(self.chain)):
                current_block = self.chain[i]
                previous_block = self.chain[i - 1]

                current_block.previous_hash = previous_block.hash
                current_block.hash = current_block.calculate_hash()
                # 更新进度条
                pbar.update(1)

        # 将修复后的区块链数据写回JSON文件
        self.write_to_json()

    def write_to_json(self):
        """
        将区块链数据写入JSON文件。
        """
        # 转换区块链为可写入JSON的字典列表
        block_data = [block.__dict__ for block in self.chain]
        filename = f'blockchain_{self.name}.json'
        # 将字典列表写入JSON文件
        with open(filename, 'w') as file:
            json.dump(block_data, file, indent=4)
    def check_and_repair(self):
        """
        检查并修复区块链的完整性。
        """
        # 检查整个区块链的有效性
        if not self.is_chain_valid():
            print("尝试全局修复区块链...")
            self.recompute_hashes()
            # 这里可能需要执行一些复杂操作，比如回滚到最近的有效状态或重建区块链等
            # 根据具体应用需求设计相应的修复策略

        print("区块链完整性检查和修复完成。")

def list_blockchains():
    """
    列出所有存在的区块链名称。

    :return: 返回一个包含所有区块链名称的列表。
    """
    prefix = 'blockchain_'
    suffix = '.json'
    blockchains = [name[len(prefix):-len(suffix)] for name in os.listdir('.') if name.startswith(prefix) and name.endswith(suffix)]
    blockchains.sort()
    return blockchains


def select_blockchain_for_deletion():
    """
    选择要删除的区块链。

    :return: 如果用户选择删除，返回选定的区块链名称；否则返回None。
    """
    blockchains = list_blockchains()

    if not blockchains:
        print("当前没有可用的区块链可供删除。")
        return

    print("\n请选择要删除的区块链编号:")
    for idx, blockchain_name in enumerate(blockchains, start=1):
        print(f"{idx}. {blockchain_name}")

    choice = input("输入编号（q退出）: ")

    if choice == 'q':
        return
    elif choice.isdigit() and 1 <= int(choice) <= len(blockchains):
        blockchain_name_to_delete = blockchains[int(choice) - 1]
        os.remove(f'blockchain_{blockchain_name_to_delete}.json')
        print(f"区块链{blockchain_name_to_delete}已删除")
    else:
        print("无效的选择。请输入有效的编号或按q退出。")
        
def select_or_create_blockchain():
    """
    选择已存在的区块链或创建新的区块链。

    :return: 返回选定或创建的区块链名称。
    """
    blockchains = list_blockchains()

    if not blockchains:
        print("当前没有可用的区块链，我们将为您创建一个新区块链(q退出)。")
        blockchain_name = input("请输入新的区块链名称:")
        if blockchain_name == 'q':
            user_exit(0)
        return blockchain_name
    else:
        print("\n请选择要操作的区块链编号:")
        for idx, blockchain_name in enumerate(blockchains, start=1):
            print(f"{idx}. {blockchain_name}") 

        choice = input("输入编号（或按回车键创建一个新区块链,q退出）:")
        if choice == 'q':
            user_exit(0)
        if choice.isdigit() and 1 <= int(choice) <= len(blockchains):
            return blockchains[int(choice) - 1]
        else:
            blockchain_name = input("请输入新的区块链名称: ")
            while blockchain_name in blockchains:
                print(f"区块链'{blockchain_name}'已存在，请重新输入新的名称或按q退出。")
            return blockchain_name
  
     
            
def user_exit(info):
    """
    优雅地退出程序。
    
    :param info: 退出信息。
    """
    print("退出程序")
    sys.exit(info)