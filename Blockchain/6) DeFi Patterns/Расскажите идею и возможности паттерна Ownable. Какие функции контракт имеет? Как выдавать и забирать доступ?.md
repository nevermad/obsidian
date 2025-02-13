[[6. Список вопросов]]

## Короткий ответ

Ownable - это базовый паттерн контроля доступа, где есть единственный владелец контракта, который имеет эксклюзивные права на выполнение определенных функций. Контракт предоставляет базовые функции для управления владением: проверку владельца, передачу и отказ от владения. Это самый простой способ ограничить доступ к функциям контракта.

---

## Подробный разбор

### **1. Базовая реализация OpenZeppelin**

```solidity
abstract contract Ownable {
    address private _owner;
    
    event OwnershipTransferred(
        address indexed previousOwner,
        address indexed newOwner
    );
    
    constructor() {
        _transferOwnership(msg.sender);
    }
    
    modifier onlyOwner() {
        require(owner() == msg.sender, "Ownable: caller is not the owner");
        _;
    }
    
    function owner() public view virtual returns (address) {
        return _owner;
    }
    
    function renounceOwnership() public virtual onlyOwner {
        _transferOwnership(address(0));
    }
    
    function transferOwnership(address newOwner) public virtual onlyOwner {
        require(newOwner != address(0), "Ownable: new owner is the zero address");
        _transferOwnership(newOwner);
    }
    
    function _transferOwnership(address newOwner) internal virtual {
        address oldOwner = _owner;
        _owner = newOwner;
        emit OwnershipTransferred(oldOwner, newOwner);
    }
}
```

### **2. Примеры использования**

1. **Управляемый токен:**
   ```solidity
   contract ManagedToken is ERC20, Ownable {
       uint256 public maxSupply;
       bool public transfersEnabled;
       
       constructor() ERC20("Managed", "MGD") {
           maxSupply = 1000000 * 10**decimals();
       }
       
       function mint(address to, uint256 amount) external onlyOwner {
           require(totalSupply() + amount <= maxSupply, "Max supply exceeded");
           _mint(to, amount);
       }
       
       function setTransfersEnabled(bool enabled) external onlyOwner {
           transfersEnabled = enabled;
       }
       
       function _beforeTokenTransfer(
           address from,
           address to,
           uint256 amount
       ) internal virtual override {
           require(transfersEnabled, "Transfers are disabled");
           super._beforeTokenTransfer(from, to, amount);
       }
   }
   ```

2. **Управляемый маркетплейс:**
   ```solidity
   contract ManagedMarketplace is Ownable {
       uint256 public fee;
       address public feeRecipient;
       
       function setFee(uint256 newFee) external onlyOwner {
           require(newFee <= 1000, "Fee too high"); // max 10%
           fee = newFee;
       }
       
       function setFeeRecipient(address newRecipient) external onlyOwner {
           require(newRecipient != address(0), "Zero address");
           feeRecipient = newRecipient;
       }
       
       function withdrawFees() external onlyOwner {
           uint256 balance = address(this).balance;
           payable(feeRecipient).transfer(balance);
       }
   }
   ```

### **3. Расширенные возможности**

1. **Временная передача прав:**
   ```solidity
   contract TemporaryOwnable is Ownable {
       address private _temporaryOwner;
       uint256 private _temporaryOwnerExpiry;
       
       event TemporaryOwnershipGranted(
           address indexed temporaryOwner,
           uint256 expiresAt
       );
       
       modifier onlyEffectiveOwner() {
           require(
               msg.sender == owner() ||
               (msg.sender == _temporaryOwner &&
               block.timestamp < _temporaryOwnerExpiry),
               "Not authorized"
           );
           _;
       }
       
       function grantTemporaryOwnership(
           address temporary,
           uint256 duration
       ) external onlyOwner {
           require(temporary != address(0), "Zero address");
           _temporaryOwner = temporary;
           _temporaryOwnerExpiry = block.timestamp + duration;
           emit TemporaryOwnershipGranted(temporary, _temporaryOwnerExpiry);
       }
   }
   ```

2. **Множественные владельцы:**
   ```solidity
   contract MultiOwnable is Ownable {
       mapping(address => bool) private _owners;
       uint256 private _ownerCount;
       
       event OwnerAdded(address indexed owner);
       event OwnerRemoved(address indexed owner);
       
       modifier onlyOwners() {
           require(_owners[msg.sender], "Not an owner");
           _;
       }
       
       function addOwner(address newOwner) external onlyOwner {
           require(!_owners[newOwner], "Already owner");
           _owners[newOwner] = true;
           _ownerCount++;
           emit OwnerAdded(newOwner);
       }
       
       function removeOwner(address owner) external onlyOwner {
           require(_owners[owner], "Not owner");
           require(_ownerCount > 1, "Cannot remove last owner");
           _owners[owner] = false;
           _ownerCount--;
           emit OwnerRemoved(owner);
       }
   }
   ```

### **4. Безопасность и лучшие практики**

1. **Проверки безопасности:**
   ```solidity
   contract SecureOwnable is Ownable {
       // Защита от случайной передачи владения
       mapping(address => bool) private _pendingOwners;
       uint256 private constant OWNERSHIP_DELAY = 2 days;
       
       function transferOwnership(
           address newOwner
       ) public virtual override onlyOwner {
           require(newOwner != address(0), "Zero address");
           _pendingOwners[newOwner] = true;
       }
       
       function acceptOwnership() external {
           require(_pendingOwners[msg.sender], "Not pending owner");
           delete _pendingOwners[msg.sender];
           _transferOwnership(msg.sender);
       }
   }
   ```

2. **Логирование действий:**
   ```solidity
   contract AuditedOwnable is Ownable {
       event OwnerAction(
           address indexed owner,
           string indexed action,
           bytes data
       );
       
       function executeAction(
           string calldata action,
           bytes calldata data
       ) external onlyOwner {
           emit OwnerAction(msg.sender, action, data);
           // Выполнение действия
       }
   }
   ```

### **5. Как выдавать и забирать доступ**

1. **Передача владения:**
   ```solidity
   // 1. Текущий владелец вызывает
   contract.transferOwnership(newOwner);
   
   // 2. Проверка нового владельца
   require(contract.owner() == newOwner);
   ```

2. **Отказ от владения:**
   ```solidity
   // Владелец отказывается от прав
   contract.renounceOwnership();
   
   // После этого owner() вернет address(0)
   ```

3. **Безопасная передача:**
   ```solidity
   // 1. Предложение нового владельца
   contract.proposeOwner(newOwner);
   
   // 2. Новый владелец принимает права
   contract.acceptOwnership();
   
   // 3. Проверка успешной передачи
   require(contract.owner() == newOwner);
   ```

---

## Связанные темы
- [[Расскажите идею и возможности паттерна Ownable2Step]]
- [[Расскажите о работе role-based AccessControl OpenZeppelin]]
- [[Что представляет из себя access control паттерн?]]

---

## Источники
- [OpenZeppelin Ownable](https://docs.openzeppelin.com/contracts/4.x/api/access#Ownable)
- [Solidity Patterns: Access Restriction](https://fravoll.github.io/solidity-patterns/access_restriction.html)
- [Smart Contract Best Practices](https://consensys.github.io/smart-contract-best-practices/) 