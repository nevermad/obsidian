[[6. Список вопросов]]

## Короткий ответ

Multisig (мультиподпись) - это смарт-контракт, требующий подтверждения операции несколькими участниками перед её выполнением. Quorum - это минимальное количество подписей, необходимое для выполнения операции, а threshold - это процент или количество подписей от общего числа участников. Транзакции из Multisig отправляются после сбора необходимого количества подписей от авторизованных участников.

---

## Подробный разбор

### **1. Базовая реализация**

```solidity
contract MultiSigWallet {
    event Deposit(address indexed sender, uint256 amount);
    event SubmitTransaction(
        address indexed owner,
        uint256 indexed txIndex,
        address indexed to,
        uint256 value,
        bytes data
    );
    event ConfirmTransaction(address indexed owner, uint256 indexed txIndex);
    event RevokeConfirmation(address indexed owner, uint256 indexed txIndex);
    event ExecuteTransaction(address indexed owner, uint256 indexed txIndex);
    
    struct Transaction {
        address to;
        uint256 value;
        bytes data;
        bool executed;
        uint256 numConfirmations;
    }
    
    address[] public owners;
    mapping(address => bool) public isOwner;
    uint256 public numConfirmationsRequired;
    Transaction[] public transactions;
    mapping(uint256 => mapping(address => bool)) public isConfirmed;
    
    modifier onlyOwner() {
        require(isOwner[msg.sender], "Not owner");
        _;
    }
    
    modifier txExists(uint256 _txIndex) {
        require(_txIndex < transactions.length, "Tx does not exist");
        _;
    }
    
    modifier notExecuted(uint256 _txIndex) {
        require(!transactions[_txIndex].executed, "Tx already executed");
        _;
    }
    
    modifier notConfirmed(uint256 _txIndex) {
        require(!isConfirmed[_txIndex][msg.sender], "Tx already confirmed");
        _;
    }
    
    constructor(address[] memory _owners, uint256 _numConfirmationsRequired) {
        require(_owners.length > 0, "Owners required");
        require(
            _numConfirmationsRequired > 0 &&
            _numConfirmationsRequired <= _owners.length,
            "Invalid number of confirmations"
        );
        
        for (uint256 i = 0; i < _owners.length;) {
            address owner = _owners[i];
            require(owner != address(0), "Invalid owner");
            require(!isOwner[owner], "Owner not unique");
            
            isOwner[owner] = true;
            owners.push(owner);
            
            unchecked { i++; }
        }
        
        numConfirmationsRequired = _numConfirmationsRequired;
    }
    
    receive() external payable {
        emit Deposit(msg.sender, msg.value);
    }
    
    function submitTransaction(
        address _to,
        uint256 _value,
        bytes memory _data
    ) public onlyOwner {
        uint256 txIndex = transactions.length;
        
        transactions.push(
            Transaction({
                to: _to,
                value: _value,
                data: _data,
                executed: false,
                numConfirmations: 0
            })
        );
        
        emit SubmitTransaction(msg.sender, txIndex, _to, _value, _data);
    }
    
    function confirmTransaction(
        uint256 _txIndex
    ) public onlyOwner txExists(_txIndex) notExecuted(_txIndex) notConfirmed(_txIndex) {
        Transaction storage transaction = transactions[_txIndex];
        transaction.numConfirmations += 1;
        isConfirmed[_txIndex][msg.sender] = true;
        
        emit ConfirmTransaction(msg.sender, _txIndex);
    }
    
    function executeTransaction(
        uint256 _txIndex
    ) public onlyOwner txExists(_txIndex) notExecuted(_txIndex) {
        Transaction storage transaction = transactions[_txIndex];
        
        require(
            transaction.numConfirmations >= numConfirmationsRequired,
            "Cannot execute tx"
        );
        
        transaction.executed = true;
        
        (bool success, ) = transaction.to.call{value: transaction.value}(
            transaction.data
        );
        require(success, "Tx failed");
        
        emit ExecuteTransaction(msg.sender, _txIndex);
    }
    
    function revokeConfirmation(
        uint256 _txIndex
    ) public onlyOwner txExists(_txIndex) notExecuted(_txIndex) {
        Transaction storage transaction = transactions[_txIndex];
        
        require(isConfirmed[_txIndex][msg.sender], "Tx not confirmed");
        
        transaction.numConfirmations -= 1;
        isConfirmed[_txIndex][msg.sender] = false;
        
        emit RevokeConfirmation(msg.sender, _txIndex);
    }
}
```

### **2. Quorum & Threshold**

1. **Выбор параметров:**
   ```solidity
   contract QuorumExample {
       uint256 public constant MIN_QUORUM_PERCENT = 50; // Минимум 50%
       uint256 public constant MAX_QUORUM_PERCENT = 75; // Максимум 75%
       
       function calculateQuorum(
           uint256 totalOwners
       ) public pure returns (uint256) {
           // Для 3 владельцев: 2 подписи (66%)
           // Для 5 владельцев: 3 подписи (60%)
           // Для 7 владельцев: 4 подписи (57%)
           return (totalOwners * MIN_QUORUM_PERCENT + 99) / 100;
       }
       
       function validateQuorum(
           uint256 quorum,
           uint256 totalOwners
       ) public pure returns (bool) {
           uint256 quorumPercent = (quorum * 100) / totalOwners;
           return quorumPercent >= MIN_QUORUM_PERCENT &&
                  quorumPercent <= MAX_QUORUM_PERCENT;
       }
   }
   ```

2. **Динамический кворум:**
   ```solidity
   contract DynamicQuorum {
       struct QuorumLevel {
           uint256 threshold;
           uint256 delay;
       }
       
       mapping(uint256 => QuorumLevel) public quorumLevels;
       
       constructor() {
           // Малые транзакции: 50% подписей, без задержки
           quorumLevels[0] = QuorumLevel(50, 0);
           
           // Средние транзакции: 66% подписей, 1 день задержки
           quorumLevels[1] = QuorumLevel(66, 1 days);
           
           // Крупные транзакции: 75% подписей, 3 дня задержки
           quorumLevels[2] = QuorumLevel(75, 3 days);
       }
       
       function getRequiredQuorum(
           uint256 amount
       ) public view returns (QuorumLevel memory) {
           if (amount < 100 ether) {
               return quorumLevels[0];
           } else if (amount < 1000 ether) {
               return quorumLevels[1];
           } else {
               return quorumLevels[2];
           }
       }
   }
   ```

### **3. Процесс отправки транзакций**

1. **Базовый процесс:**
   ```solidity
   // 1. Создание транзакции
   multisig.submitTransaction(
       recipient,
       amount,
       data
   );
   
   // 2. Подтверждение транзакции владельцами
   multisig.confirmTransaction(txIndex);
   
   // 3. Выполнение транзакции после достижения кворума
   multisig.executeTransaction(txIndex);
   ```

2. **Расширенный процесс:**
   ```solidity
   contract EnhancedMultiSig {
       struct TransactionData {
           address to;
           uint256 value;
           bytes data;
           bool executed;
           uint256 numConfirmations;
           uint256 submittedTime;
           uint256 executionTime;
           address[] confirmations;
       }
       
       function submitTransaction(
           address _to,
           uint256 _value,
           bytes memory _data,
           uint256 _delay
       ) public onlyOwner {
           uint256 txIndex = transactions.length;
           
           transactions.push(
               TransactionData({
                   to: _to,
                   value: _value,
                   data: _data,
                   executed: false,
                   numConfirmations: 0,
                   submittedTime: block.timestamp,
                   executionTime: block.timestamp + _delay,
                   confirmations: new address[](0)
               })
           );
           
           emit TransactionSubmitted(msg.sender, txIndex, _to, _value);
       }
       
       function executeTransaction(
           uint256 _txIndex
       ) public onlyOwner txExists(_txIndex) notExecuted(_txIndex) {
           TransactionData storage transaction = transactions[_txIndex];
           
           require(
               transaction.numConfirmations >= numConfirmationsRequired,
               "Not enough confirmations"
           );
           
           require(
               block.timestamp >= transaction.executionTime,
               "Execution delay not passed"
           );
           
           transaction.executed = true;
           
           (bool success, ) = transaction.to.call{value: transaction.value}(
               transaction.data
           );
           require(success, "Transaction failed");
           
           emit TransactionExecuted(msg.sender, _txIndex);
       }
   }
   ```

### **4. Популярные реализации**

1. **Gnosis Safe:**
   ```solidity
   interface IGnosisSafe {
       function execTransaction(
           address to,
           uint256 value,
           bytes calldata data,
           uint8 operation,
           uint256 safeTxGas,
           uint256 baseGas,
           uint256 gasPrice,
           address gasToken,
           address refundReceiver,
           bytes memory signatures
       ) external payable returns (bool);
       
       function getThreshold() external view returns (uint256);
       function getOwners() external view returns (address[] memory);
       function isOwner(address owner) external view returns (bool);
   }
   ```

2. **OpenZeppelin Governor:**
   ```solidity
   abstract contract Governor is IGovernor {
       struct ProposalCore {
           uint256 voteStart;
           uint256 voteEnd;
           bool executed;
           bool canceled;
       }
       
       mapping(uint256 => ProposalCore) private _proposals;
       
       function propose(
           address[] memory targets,
           uint256[] memory values,
           bytes[] memory calldatas,
           string memory description
       ) public virtual override returns (uint256) {
           // Создание предложения
       }
       
       function execute(
           address[] memory targets,
           uint256[] memory values,
           bytes[] memory calldatas,
           bytes32 descriptionHash
       ) public payable virtual override returns (uint256) {
           // Выполнение предложения
       }
   }
   ```

### **5. Безопасность и лучшие практики**

1. **Защита от атак:**
   ```solidity
   contract SecureMultiSig {
       // Защита от replay-атак
       mapping(bytes32 => bool) public executed;
       
       function executeTransaction(
           address to,
           uint256 value,
           bytes memory data,
           bytes[] memory signatures
       ) public {
           bytes32 txHash = keccak256(
               abi.encodePacked(
                   address(this),
                   block.chainid,
                   nonce++,
                   to,
                   value,
                   data
               )
           );
           
           require(!executed[txHash], "Already executed");
           require(
               verifySignatures(txHash, signatures),
               "Invalid signatures"
           );
           
           executed[txHash] = true;
           
           (bool success, ) = to.call{value: value}(data);
           require(success, "Transaction failed");
       }
   }
   ```

2. **Мониторинг и логирование:**
   ```solidity
   contract AuditedMultiSig {
       event QuorumChanged(uint256 oldQuorum, uint256 newQuorum);
       event OwnerAdded(address indexed owner);
       event OwnerRemoved(address indexed owner);
       event TransactionSubmitted(
           address indexed submitter,
           uint256 indexed txIndex,
           address indexed to,
           uint256 value
       );
       event TransactionConfirmed(
           address indexed owner,
           uint256 indexed txIndex
       );
       event TransactionExecuted(
           address indexed executor,
           uint256 indexed txIndex
       );
       event TransactionFailed(
           uint256 indexed txIndex,
           string reason
       );
   }
   ```

---

## Связанные темы
- [[Multisig 1:2 какие могут быть проблемы?]]
- [[Какие требования следует предъявить к аккаунтам участников Multisig?]]
- [[Что такое DAO?]]

---

## Источники
- [Gnosis Safe Contracts](https://github.com/safe-global/safe-contracts)
- [OpenZeppelin Governor](https://docs.openzeppelin.com/contracts/4.x/api/governance)
- [ConsenSys Best Practices](https://consensys.github.io/smart-contract-best-practices/) 