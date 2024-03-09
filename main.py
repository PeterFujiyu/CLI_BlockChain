from block import *
def main():
    blockchain = None

    while True:
        blockchains = list_blockchains()

        if not blockchains:
            print("当前没有可用的区块链，我们将为您创建一个新区块链(q退出)。")
            blockchain_name = input("请输入新的区块链名称:")
            if blockchain_name == 'q':
                user_exit(0)
            blockchain = Blockchain(blockchain_name)
        else:
            if blockchain is None:
                selected_blockchain = select_or_create_blockchain()
                blockchain = Blockchain(selected_blockchain)

            print("\n当前区块链: ", blockchain.name)
            Blockchain.is_chain_valid(blockchain)

        print("\n1. 添加新数据")
        print("2. 查看数据")
        print("3. 切换区块链")
        print("4. 删除指定区块链")
        print("5. 检查区块链完整性")
        print("6. 退出程序")

        choice = input("请选择要执行的操作编号: ")

        if choice == "1":
            data = input("请输入区块的数据: ")
            try:
                blockchain.add_block(data)
            except ValueError as e:
                print(f"错误: {e}")

        elif choice == "2":
            blockchain.print_blockchain()

        elif choice == "3":
            # 当用户选择切换区块链时，重新调用select_or_create_blockchain函数
            selected_blockchain = select_or_create_blockchain()
            blockchain = Blockchain(selected_blockchain)
            continue

        elif choice == "4":
            select_blockchain_for_deletion()
            continue  # Refresh the list of blockchains after deletion
        
        elif choice == "5":
            blockchain.is_chain_valid()
            blockchain.check_and_repair()

        elif choice == "6":
            user_exit(0)

        else:
            print("无效的选择。请输入 1、2、3、4、5 或 6。")

if __name__ == "__main__":
    main()