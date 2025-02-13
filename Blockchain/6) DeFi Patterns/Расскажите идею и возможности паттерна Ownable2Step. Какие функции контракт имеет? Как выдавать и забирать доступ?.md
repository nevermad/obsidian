[[6. Список вопросов]]

## Короткий ответ

Ownable2Step - это улучшенная версия паттерна Ownable, которая добавляет двухэтапную передачу прав владения для повышения безопасности. Новый владелец должен явно принять права через вызов `acceptOwnership()`, что защищает от случайной передачи прав неверному адресу. Контракт предоставляет функции для управления процессом передачи владения и отслеживания состояния передачи.

---

## Подробный разбор

### **1. Базовая реализация OpenZeppelin**

```solidity
abstract contract Ownable2Step is Ownable {
    address private _pendingOwner;
    
    event OwnershipTransferStarted(
        address indexed previousOwner,
        address indexed newOwner
    );
    
    function pendingOwner() public view virtual returns (address) {
        return _pendingOwner;
    }
    
    function transferOwnership(
        address newOwner
    ) public virtual override onlyOwner {
        require(newOwner != address(0), "Ownable2Step: new owner is the zero address");
        _pendingOwner = newOwner;
        emit OwnershipTransferStarted(owner(), newOwner);
    }
    
    function acceptOwnership() public virtual {
        address sender = msg.sender;
        require(pendingOwner() == sender, "Ownable2Step: caller is not the new owner");
        
        _transferOwnership(sender);
        _pendingOwner = address(0);
    }
    
    function _transferOwnership(
        address newOwner
    ) internal virtual override {
        delete _pendingOwner;
        super._transferOwnership(newOwner);
    }
}
```

### **2. Примеры использования**

1. **Безопасный токен:**
   ```solidity
   contract SecureToken is ERC20, Ownable2Step {
       mapping(address => bool) public blacklist;
       
       constructor() ERC20("Secure", "SEC") {}
       
       function blacklistAddress(address account) external onlyOwner {
           blacklist[account] = true;
       }
       
       function unblacklistAddress(address account) external onlyOwner {
           blacklist[account] = false;
       }
       
       function _beforeTokenTransfer(
           address from,
           address to,
           uint256 amount
       ) internal virtual override {
           require(!blacklist[from] && !blacklist[to], "Blacklisted");
           super._beforeTokenTransfer(from, to, amount);
       }
   }
   ```

2. **Управляемый протокол:**
   ```solidity
   contract ManagedProtocol is Ownable2Step {
       uint256 public fee;
       address public treasury;
       bool public paused;
       
       event FeeUpdated(uint256 oldFee, uint256 newFee);
       event TreasuryUpdated(address oldTreasury, address newTreasury);
       
       function setFee(uint256 newFee) external onlyOwner {
           require(newFee <= 1000, "Fee too high"); // max 10%
           emit FeeUpdated(fee, newFee);
           fee = newFee;
       }
       
       function setTreasury(address newTreasury) external onlyOwner {
           require(newTreasury != address(0), "Zero address");
           emit TreasuryUpdated(treasury, newTreasury);
           treasury = newTreasury;
       }
       
       function togglePause() external onlyOwner {
           paused = !paused;
       }
   }
   ```

### **3. Расширенные возможности**

1. **Тайм-лок для принятия владения:**
   ```solidity
   contract TimedOwnable2Step is Ownable2Step {
       uint256 private constant ACCEPTANCE_PERIOD = 2 days;
       uint256 private _transferInitiatedAt;
       
       function transferOwnership(
           address newOwner
       ) public virtual override onlyOwner {
           super.transferOwnership(newOwner);
           _transferInitiatedAt = block.timestamp;
       }
       
       function acceptOwnership() public virtual override {
           require(
               block.timestamp <= _transferInitiatedAt + ACCEPTANCE_PERIOD,
               "Acceptance period expired"
           );
           super.acceptOwnership();
       }
       
       function cancelOwnershipTransfer() external onlyOwner {
           require(pendingOwner() != address(0), "No pending transfer");
           _transferInitiatedAt = 0;
           delete _pendingOwner;
       }
   }
   ```

2. **Подтверждение через подпись:**
   ```solidity
   contract SignedOwnable2Step is Ownable2Step {
       mapping(address => bytes32) private _pendingTransfers;
       
       function transferOwnershipWithSignature(
           address newOwner,
           bytes memory signature
       ) external onlyOwner {
           bytes32 hash = keccak256(
               abi.encodePacked(address(this), newOwner)
           );
           require(
               recoverSigner(hash, signature) == newOwner,
               "Invalid signature"
           );
           super.transferOwnership(newOwner);
       }
       
       function recoverSigner(
           bytes32 hash,
           bytes memory signature
       ) internal pure returns (address) {
           bytes32 messageHash = keccak256(
               abi.encodePacked("\x19Ethereum Signed Message:\n32", hash)
           );
           (uint8 v, bytes32 r, bytes32 s) = splitSignature(signature);
           return ecrecover(messageHash, v, r, s);
       }
   }
   ```

### **4. Безопасность и лучшие практики**

1. **Проверки безопасности:**
   ```solidity
   contract SecureOwnable2Step is Ownable2Step {
       // Защита от фронтраннинга
       mapping(address => uint256) private _nonces;
       
       function transferOwnershipWithNonce(
           address newOwner,
           uint256 nonce
       ) external onlyOwner {
           require(nonce == _nonces[msg.sender] + 1, "Invalid nonce");
           _nonces[msg.sender] = nonce;
           super.transferOwnership(newOwner);
       }
       
       // Защита от случайного принятия
       function acceptOwnershipWithConfirmation(
           bytes32 confirmationHash
       ) external {
           require(
               keccak256(abi.encodePacked(msg.sender)) == confirmationHash,
               "Invalid confirmation"
           );
           super.acceptOwnership();
       }
   }
   ```

2. **Логирование и мониторинг:**
   ```solidity
   contract AuditedOwnable2Step is Ownable2Step {
       event OwnershipTransferCanceled(
           address indexed previousOwner,
           address indexed pendingOwner
       );
       
       event OwnershipTransferExpired(
           address indexed previousOwner,
           address indexed pendingOwner
       );
       
       function cancelOwnershipTransfer() external onlyOwner {
           address pending = pendingOwner();
           require(pending != address(0), "No pending transfer");
           delete _pendingOwner;
           emit OwnershipTransferCanceled(owner(), pending);
       }
   }
   ```

### **5. Как выдавать и забирать доступ**

1. **Процесс передачи владения:**
   ```solidity
   // 1. Текущий владелец инициирует передачу
   contract.transferOwnership(newOwner);
   
   // 2. Проверяем pending owner
   require(contract.pendingOwner() == newOwner);
   
   // 3. Новый владелец принимает права
   contract.acceptOwnership();
   
   // 4. Проверяем успешную передачу
   require(contract.owner() == newOwner);
   require(contract.pendingOwner() == address(0));
   ```

2. **Отмена передачи:**
   ```solidity
   // 1. Проверяем наличие pending transfer
   address pending = contract.pendingOwner();
   require(pending != address(0));
   
   // 2. Отменяем передачу
   contract.cancelOwnershipTransfer();
   
   // 3. Проверяем отмену
   require(contract.pendingOwner() == address(0));
   ```

3. **Безопасная передача с таймаутом:**
   ```solidity
   // 1. Инициируем передачу с временным окном
   contract.transferOwnershipWithTimeout(newOwner, 2 days);
   
   // 2. Новый владелец должен принять в течение окна
   contract.acceptOwnership();
   
   // 3. После окна передача автоматически отменяется
   require(
       block.timestamp <= transferInitiatedAt + ACCEPTANCE_PERIOD,
       "Expired"
   );
   ```

---

## Связанные темы
- [[Расскажите идею и возможности паттерна Ownable]]
- [[Расскажите о работе role-based AccessControl OpenZeppelin]]
- [[Что представляет из себя access control паттерн?]]

---

## Источники
- [OpenZeppelin Ownable2Step](https://docs.openzeppelin.com/contracts/4.x/api/access#Ownable2Step)
- [Solidity Security Considerations](https://docs.soliditylang.org/en/v0.8.17/security-considerations.html)
- [Smart Contract Best Practices](https://consensys.github.io/smart-contract-best-practices/) 