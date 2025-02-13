[[6. Список вопросов]]

## Короткий ответ

Access control паттерн - это механизм управления доступом к функциям смарт-контракта, который позволяет ограничить выполнение определенных операций только авторизованными адресами. Используется для защиты критических функций, таких как обновление параметров, вывод средств или изменение конфигурации контракта.

---

## Подробный разбор

### **1. Базовая реализация**

```solidity
contract AccessControl {
    mapping(address => bool) private _admins;
    
    event AdminAdded(address indexed account);
    event AdminRemoved(address indexed account);
    
    modifier onlyAdmin() {
        require(_admins[msg.sender], "Not an admin");
        _;
    }
    
    constructor() {
        _admins[msg.sender] = true;
        emit AdminAdded(msg.sender);
    }
    
    function addAdmin(address account) external onlyAdmin {
        require(account != address(0), "Zero address");
        require(!_admins[account], "Already admin");
        _admins[account] = true;
        emit AdminAdded(account);
    }
    
    function removeAdmin(address account) external onlyAdmin {
        require(_admins[account], "Not admin");
        require(account != msg.sender, "Cannot remove self");
        _admins[account] = false;
        emit AdminRemoved(account);
    }
    
    function isAdmin(address account) public view returns (bool) {
        return _admins[account];
    }
}
```

### **2. Примеры использования**

1. **Управление протоколом DeFi:**
   ```solidity
   contract DeFiProtocol is AccessControl {
       uint256 public fee;
       address public treasury;
       
       function setFee(uint256 newFee) external onlyAdmin {
           require(newFee <= 1000, "Fee too high"); // max 10%
           fee = newFee;
       }
       
       function setTreasury(address newTreasury) external onlyAdmin {
           require(newTreasury != address(0), "Zero address");
           treasury = newTreasury;
       }
       
       function emergencyWithdraw() external onlyAdmin {
           uint256 balance = address(this).balance;
           payable(treasury).transfer(balance);
       }
   }
   ```

2. **NFT Маркетплейс:**
   ```solidity
   contract NFTMarketplace is AccessControl {
       mapping(address => bool) private _verifiedCollections;
       uint256 public listingFee;
       
       function verifyCollection(
           address collection
       ) external onlyAdmin {
           _verifiedCollections[collection] = true;
       }
       
       function updateListingFee(
           uint256 newFee
       ) external onlyAdmin {
           require(newFee <= 0.1 ether, "Fee too high");
           listingFee = newFee;
       }
       
       function blacklistCollection(
           address collection
       ) external onlyAdmin {
           _verifiedCollections[collection] = false;
       }
   }
   ```

### **3. Расширенные возможности**

1. **Многоуровневый доступ:**
   ```solidity
   contract MultiLevelAccess {
       mapping(address => uint256) private _accessLevels;
       
       uint256 public constant ADMIN_LEVEL = 2;
       uint256 public constant OPERATOR_LEVEL = 1;
       
       modifier minLevel(uint256 level) {
           require(
               _accessLevels[msg.sender] >= level,
               "Insufficient access level"
           );
           _;
       }
       
       function setAccessLevel(
           address account,
           uint256 level
       ) external minLevel(ADMIN_LEVEL) {
           require(level < ADMIN_LEVEL, "Cannot grant admin");
           _accessLevels[account] = level;
       }
   }
   ```

2. **Временный доступ:**
   ```solidity
   contract TemporaryAccess {
       struct Access {
           bool hasAccess;
           uint256 expiresAt;
       }
       
       mapping(address => Access) private _temporaryAccess;
       
       modifier onlyWithAccess() {
           require(
               _temporaryAccess[msg.sender].hasAccess &&
               _temporaryAccess[msg.sender].expiresAt > block.timestamp,
               "No access"
           );
           _;
       }
       
       function grantTemporaryAccess(
           address account,
           uint256 duration
       ) external onlyAdmin {
           _temporaryAccess[account] = Access(
               true,
               block.timestamp + duration
           );
       }
   }
   ```

### **4. Примеры необходимости использования**

1. **Финансовые операции:**
   - Изменение комиссий протокола
   - Обновление адресов казначейства
   - Экстренный вывод средств
   - Обновление параметров протокола

2. **Управление списками:**
   - Добавление/удаление токенов из whitelist
   - Верификация NFT коллекций
   - Управление списком стейблкоинов
   - Блокировка подозрительных адресов

3. **Технические операции:**
   - Обновление смарт-контрактов (proxy)
   - Приостановка работы контракта
   - Обновление оракулов
   - Изменение параметров безопасности

4. **Управление ролями:**
   - Назначение операторов
   - Управление валидаторами
   - Добавление модераторов
   - Управление правами доступа

### **5. Лучшие практики**

1. **Безопасность:**
   ```solidity
   contract SecureAccess {
       // Защита от случайного удаления всех админов
       uint256 private _adminCount;
       
       function removeAdmin(address account) external onlyAdmin {
           require(_adminCount > 1, "Cannot remove last admin");
           require(account != msg.sender, "Cannot remove self");
           _adminCount--;
           _admins[account] = false;
       }
       
       // Двухэтапное изменение критических параметров
       mapping(bytes32 => uint256) private _pendingChanges;
       uint256 private constant DELAY = 2 days;
       
       function proposeChange(
           bytes32 paramHash,
           uint256 newValue
       ) external onlyAdmin {
           _pendingChanges[paramHash] = newValue;
       }
       
       function executeChange(
           bytes32 paramHash
       ) external onlyAdmin {
           require(
               block.timestamp >= _pendingChanges[paramHash] + DELAY,
               "Too early"
           );
           // Выполнение изменения
       }
   }
   ```

---

## Связанные темы
- [[Расскажите идею и возможности паттерна Ownable. Какие функции контракт имеет? Как выдавать и забирать доступ?]]
- [[Расскажите о работе role-based AccessControl OpenZeppelin]]
- [[Что такое и как работает Multisig?]]

---

## Источники
- [OpenZeppelin Access Control](https://docs.openzeppelin.com/contracts/4.x/access-control)
- [Solidity Security Considerations](https://docs.soliditylang.org/en/v0.8.17/security-considerations.html)
- [Smart Contract Best Practices](https://consensys.github.io/smart-contract-best-practices/) 