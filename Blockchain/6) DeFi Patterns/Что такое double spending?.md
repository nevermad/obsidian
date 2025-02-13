## Короткий ответ

Double spending - это атака, при которой одни и те же средства используются более одного раза. В контексте блокчейна это может происходить при форках цепи, в смарт-контрактах при reentrancy атаках, а также при некорректной обработке nonce транзакций или неправильной реализации механизмов учета балансов.

---

## Подробный разбор

### **1. Типы Double Spending**

1. **На уровне блокчейна:**
   ```solidity
   // Пример состояния в разных форках
   Fork A: balance[user] = 100 - 50 (sent) = 50
   Fork B: balance[user] = 100 - 50 (sent to different address) = 50
   
   // После резолюции форка только одна транзакция будет валидной
   Final Chain: balance[user] = 50 (одна из транзакций)
   ```

2. **На уровне смарт-контрактов:**
   ```solidity
   contract VulnerableContract {
       mapping(address => uint256) public balances;
       
       function withdraw() external {
           uint256 balance = balances[msg.sender];
           // Уязвимость: баланс не обнуляется до отправки
           (bool success,) = msg.sender.call{value: balance}("");
           balances[msg.sender] = 0;
       }
   }
   ```

### **2. Механизмы предотвращения**

1. **Nonce транзакций:**
   ```solidity
   contract NonceProtection {
       mapping(address => uint256) public nonces;
       mapping(bytes32 => bool) public executedTxs;
       
       function executeWithNonce(uint256 nonce) external {
           require(nonce == nonces[msg.sender], "Invalid nonce");
           nonces[msg.sender]++;
           
           // Выполнение операции
       }
       
       function executeWithHash(bytes32 txHash) external {
           require(!executedTxs[txHash], "Already executed");
           executedTxs[txHash] = true;
           
           // Выполнение операции
       }
   }
   ```

2. **Checks-Effects-Interactions паттерн:**
   ```solidity
   contract SecureContract {
       mapping(address => uint256) public balances;
       
       function withdraw() external {
           // 1. Checks
           uint256 balance = balances[msg.sender];
           require(balance > 0, "No balance");
           
           // 2. Effects
           balances[msg.sender] = 0;
           
           // 3. Interactions
           (bool success,) = msg.sender.call{value: balance}("");
           require(success, "Transfer failed");
       }
   }
   ```

### **3. Защита в DeFi протоколах**

1. **Atomic Swaps:**
   ```solidity
   contract AtomicSwap {
       struct Swap {
           address initiator;
           uint256 amount;
           bool executed;
           uint256 expiry;
       }
       
       mapping(bytes32 => Swap) public swaps;
       
       function initiateSwap(
           bytes32 hash,
           uint256 amount,
           uint256 timelock
       ) external {
           require(!swaps[hash].executed, "Already executed");
           
           swaps[hash] = Swap({
               initiator: msg.sender,
               amount: amount,
               executed: false,
               expiry: block.timestamp + timelock
           });
           
           // Перевод токенов на контракт
       }
       
       function executeSwap(bytes32 hash, bytes32 secret) external {
           Swap storage swap = swaps[hash];
           require(!swap.executed, "Already executed");
           require(block.timestamp < swap.expiry, "Expired");
           require(
               keccak256(abi.encodePacked(secret)) == hash,
               "Invalid secret"
           );
           
           swap.executed = true;
           // Выполнение свопа
       }
   }
   ```

2. **Liquidity Pool Protection:**
   ```solidity
   contract SecurePool {
       mapping(address => uint256) public balances;
       mapping(address => uint256) public lastWithdrawBlock;
       
       uint256 public constant WITHDRAWAL_DELAY = 10; // blocks
       
       function withdraw(uint256 amount) external {
           require(
               block.number >= lastWithdrawBlock[msg.sender] + WITHDRAWAL_DELAY,
               "Too soon"
           );
           
           require(balances[msg.sender] >= amount, "Insufficient balance");
           balances[msg.sender] -= amount;
           lastWithdrawBlock[msg.sender] = block.number;
           
           (bool success,) = msg.sender.call{value: amount}("");
           require(success, "Transfer failed");
       }
   }
   ```

### **4. Мониторинг и обнаружение**

1. **Event Logging:**
   ```solidity
   contract MonitoredTransactions {
       event Transfer(
           address indexed from,
           address indexed to,
           uint256 amount,
           uint256 nonce
       );
       
       mapping(address => uint256) public nonces;
       
       function transfer(address to, uint256 amount) external {
           uint256 nonce = nonces[msg.sender]++;
           
           // Выполнение перевода
           
           emit Transfer(msg.sender, to, amount, nonce);
       }
   }
   ```

2. **Транзакционный мониторинг:**
   ```javascript
   // Web3 код для мониторинга
   web3.eth.subscribe('pendingTransactions')
       .on('data', async (txHash) => {
           const tx = await web3.eth.getTransaction(txHash);
           
           // Проверка на дубликаты nonce
           if (isDoubleSpendAttempt(tx)) {
               alertDoubleSpend(tx);
           }
       });
   ```

### **5. Восстановление после атак**

1. **Механизм паузы:**
   ```solidity
   contract PausableContract {
       bool public paused;
       mapping(address => uint256) public balances;
       
       modifier whenNotPaused() {
           require(!paused, "Contract paused");
           _;
       }
       
       function pause() external onlyOwner {
           paused = true;
       }
       
       function withdraw() external whenNotPaused {
           uint256 balance = balances[msg.sender];
           require(balance > 0, "No balance");
           
           balances[msg.sender] = 0;
           (bool success,) = msg.sender.call{value: balance}("");
           require(success, "Transfer failed");
       }
   }
   ```

---

## Связанные темы
- [[6. Список вопросов]]
- [[Что такое reentrancy attack?]]
- [[Почему Nonce увеличивается после каждой транзакции?]]
- [[Какие потенциальные проблемы / уязвимости могут произойти при наличии механизма обратных вызовов?]]

---

## Источники
- [Bitcoin Double Spending](https://en.bitcoin.it/wiki/Double-spending)
- [Ethereum Yellow Paper](https://ethereum.github.io/yellowpaper/paper.pdf)
- [Smart Contract Security Best Practices](https://consensys.github.io/smart-contract-best-practices/) 