# 项目：简化区块链实现与测试

该项目包含四个核心Python文件，用于创建一个基础的区块链系统并对其进行性能和篡改测试。以下是各文件及其功能概述：

## block.py

- 定义了Block类，用于表示区块链中的单个区块，包括区块索引、前一区块哈希、数据内容以及当前区块哈希等属性。
- 定义了Blockchain类，负责构建区块链结构，包含了添加新区块、验证区块链完整性以及从文件加载和保存区块链的方法。

## main.py

- 提供了一个命令行交互界面，允许用户在不同的区块链间切换、查看和添加数据，并执行诸如删除、检查区块链完整性和退出程序等操作。

## test_write.py

- 实现了tamper_with_blockchain函数，模拟篡改指定区块链中某个区块的数据，并检查篡改后区块链的有效性。
- test_tampering函数作为入口点，通过命令行接收参数并调用tamper_with_blockchain进行篡改测试。

## test.py

- test_blockchain_performance函数用来测试区块链的性能，通过生成一定数量的随机数据并将其添加为新区块，同时使用tqdm库展示进度条。
- 添加完所有区块后，验证整个区块链的有效性，并报告结果。

## 运行项目
- 先克隆存储库，并执行
    ```bash
    pip install -r requirements.txt
    ```
- 若要运行项目的主界面，可直接运行main.py，这将启动一个命令行应用程序，允许您对区块链进行各种管理操作。
- 若要测试区块链在添加大量随机数据时的性能，运行test.py，并输入要测试的区块数量。
- 若需测试篡改区块链及验证区块链完整性的功能，请运行test_write.py，按照提示输入相关参数进行测试。

## 打包📦
- 安装Pyinstaller
  ```bash
  python -m pip install pyinstaller
  ```
- 打包
  ```bash
  python -m pyinstaller -F main.py
  ```
- 使用
  在dist中有最终的程序
  
总之，这个项目提供了一个简单的区块链实现框架，并且带有基本的增删查改、性能测试以及数据篡改与校验功能。
