[[6. Список вопросов]]

## Короткий ответ

Multisig с конфигурацией 1:2 (одна подпись из двух возможных) имеет серьезные проблемы с безопасностью, так как фактически сводит мультиподпись к единоличному контролю. Основные проблемы включают: отсутствие реальной защиты от несанкционированных действий, риск компрометации одного ключа, возможность единоличного принятия решений и отсутствие механизма сдержек и противовесов.

---

## Подробный разбор

### **1. Основные проблемы**

1. **Отсутствие реальной защиты:**
   ```solidity
   contract Multisig1of2 {
       address[2] public owners;
       
       modifier onlyOwner() {
           require(
               msg.sender == owners[0] || msg.sender == owners[1],
               "Not owner"
           );
           _;
       }
       
       // Проблема: любой владелец может действовать единолично
       function executeTransaction(
           address to,
           uint256 value,
           bytes memory data
       ) external onlyOwner {
           (bool success, ) = to.call{value: value}(data);
           require(success, "Transaction failed");
       }
   }
   ```

2. **Риск компрометации:**
   ```solidity
   contract VulnerableMultisig {
       address[2] public owners;
       mapping(address => bool) public isOwner;
       
       // Проблема: компрометация одного ключа дает полный контроль
       function isValidSignature(
           bytes32 hash,
           bytes memory signature
       ) public view returns (bool) {
           address signer = recoverSigner(hash, signature);
           return isOwner[signer];
       }
   }
   ```

### **2. Сравнение с безопасными конфигурациями**

1. **2:2 конфигурация:**
   ```solidity
   contract SecureMultisig {
       address[2] public owners;
       mapping(bytes32 => mapping(address => bool)) public confirmed;
       
       function executeTransaction(
           address to,
           uint256 value,
           bytes memory data,
           bytes memory signature1,
           bytes memory signature2
       ) external {
           bytes32 txHash = keccak256(
               abi.encodePacked(to, value, data)
           );
           
           address signer1 = recoverSigner(txHash, signature1);
           address signer2 = recoverSigner(txHash, signature2);
           
           require(
               (signer1 == owners[0] && signer2 == owners[1]) ||
               (signer1 == owners[1] && signer2 == owners[0]),
               "Invalid signatures"
           );
           
           (bool success, ) = to.call{value: value}(data);
           require(success, "Transaction failed");
       }
   }
   ```

2. **2:3 конфигурация:**
   ```solidity
   contract BetterMultisig {
       address[3] public owners;
       uint256 public constant REQUIRED_SIGNATURES = 2;
       
       mapping(bytes32 => mapping(address => bool)) public confirmed;
       mapping(bytes32 => uint256) public confirmationCount;
       
       function confirmTransaction(
           bytes32 txHash
       ) external {
           require(isOwner[msg.sender], "Not owner");
           require(!confirmed[txHash][msg.sender], "Already confirmed");
           
           confirmed[txHash][msg.sender] = true;
           confirmationCount[txHash]++;
       }
       
       function executeTransaction(
           address to,
           uint256 value,
           bytes memory data
       ) external {
           bytes32 txHash = keccak256(
               abi.encodePacked(to, value, data)
           );
           
           require(
               confirmationCount[txHash] >= REQUIRED_SIGNATURES,
               "Not enough confirmations"
           );
           
           (bool success, ) = to.call{value: value}(data);
           require(success, "Transaction failed");
       }
   }
   ```

### **3. Потенциальные атаки**

1. **Единоличное управление:**
   ```solidity
   contract AttackExample {
       // Атакующий может:
       // 1. Вывести все средства
       // 2. Изменить конфигурацию
       // 3. Добавить бэкдоры
       // 4. Заблокировать второго владельца
       
       function maliciousAction(
           address multisig,
           address attacker
       ) external {
           // Пример атаки: вывод средств
           (bool success, ) = multisig.call(
               abi.encodeWithSignature(
                   "executeTransaction(address,uint256,bytes)",
                   attacker,
                   address(multisig).balance,
                   ""
               )
           );
       }
   }
   ```

2. **Фронтраннинг:**
   ```solidity
   contract FrontrunningExample {
       // Атакующий может:
       // 1. Перехватить и опередить транзакции второго владельца
       // 2. Заблокировать нежелательные транзакции
       // 3. Манипулировать порядком транзакций
       
       function frontrunAttack(
           address multisig,
           bytes memory targetTx
       ) external {
           // Пример: блокировка транзакции
           (bool success, ) = multisig.call(
               abi.encodeWithSignature(
                   "executeTransaction(address,uint256,bytes)",
                   address(this),
                   0,
                   abi.encodeWithSignature("blockTransaction()")
               )
           );
       }
   }
   ```

### **4. Рекомендации по безопасности**

1. **Минимальные требования:**
   ```solidity
   contract SafeMultisig {
       // 1. Использовать как минимум 2:3 конфигурацию
       uint256 public constant MIN_SIGNATURES = 2;
       uint256 public constant TOTAL_OWNERS = 3;
       
       // 2. Добавить временные задержки
       uint256 public constant EXECUTION_DELAY = 24 hours;
       
       // 3. Ограничить максимальную сумму транзакции
       uint256 public constant MAX_TRANSACTION_VALUE = 100 ether;
       
       // 4. Добавить возможность отмены транзакции
       mapping(bytes32 => bool) public cancelled;
       
       // 5. Реализовать механизм восстановления
       address public recoveryAddress;
   }
   ```

2. **Дополнительные меры:**
   ```solidity
   contract EnhancedSecurity {
       // 1. Whitelist разрешенных адресов
       mapping(address => bool) public whitelist;
       
       // 2. Ограничение частоты транзакций
       mapping(address => uint256) public lastTransactionTime;
       uint256 public constant TRANSACTION_COOLDOWN = 1 hours;
       
       // 3. Мониторинг активности
       event TransactionAttempt(
           address indexed initiator,
           address indexed target,
           uint256 value
       );
       
       // 4. Аварийная остановка
       bool public paused;
       modifier notPaused() {
           require(!paused, "Contract is paused");
           _;
       }
   }
   ```

---

## Связанные темы
- [[Что такое и как работает Multisig?]]
- [[Какие требования следует предъявить к аккаунтам участников Multisig?]]
- [[Что такое DAO?]]

---

## Источники
- [Gnosis Safe Documentation](https://docs.gnosis-safe.io/)
- [ConsenSys Security Best Practices](https://consensys.github.io/smart-contract-best-practices/)
- [OpenZeppelin Security Blog](https://blog.openzeppelin.com/security-audits/) 