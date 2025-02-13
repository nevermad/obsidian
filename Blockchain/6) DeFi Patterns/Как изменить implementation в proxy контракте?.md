## Короткий ответ

Для изменения implementation в proxy контракте необходимо:
1. Развернуть новую имплементацию
2. Проверить совместимость storage layout
3. Инициализировать новую имплементацию (если требуется)
4. Вызвать функцию обновления в proxy (upgradeTo или аналогичную)
5. Проверить корректность обновления

---

## Подробный разбор

### **1. Базовый процесс обновления**

```solidity
contract ProxyAdmin {
    // Слот для хранения адреса имплементации (EIP-1967)
    bytes32 private constant IMPLEMENTATION_SLOT = 
        0x360894a13ba1a3210667c828492db98dca3e2076cc3735a920a3ca505d382bbc;
    
    // Функция обновления
    function upgradeTo(address newImplementation) external onlyAdmin {
        // Проверяем, что новый адрес - это контракт
        require(
            newImplementation.code.length > 0,
            "Not a contract"
        );
        
        // Сохраняем старый адрес для событий
        address oldImplementation = _getImplementation();
        
        // Обновляем адрес
        assembly {
            sstore(IMPLEMENTATION_SLOT, newImplementation)
        }
        
        // Событие об обновлении
        emit Upgraded(oldImplementation, newImplementation);
    }
    
    // Получение текущей имплементации
    function _getImplementation() internal view returns (address impl) {
        assembly {
            impl := sload(IMPLEMENTATION_SLOT)
        }
    }
}
```

### **2. Безопасное обновление**

```solidity
contract SafeUpgrade {
    // Структура для предложения обновления
    struct UpgradeProposal {
        address implementation;
        uint256 timestamp;
        bool initialized;
        mapping(address => bool) votes;
        uint256 voteCount;
    }
    
    UpgradeProposal public currentProposal;
    uint256 public constant TIMELOCK = 2 days;
    uint256 public constant MIN_VOTES = 3;
    
    // Шаг 1: Предложение обновления
    function proposeUpgrade(
        address newImplementation
    ) external onlyAdmin {
        // Проверки
        require(
            newImplementation.code.length > 0,
            "Not a contract"
        );
        require(
            !currentProposal.initialized,
            "Proposal exists"
        );
        
        // Создаем предложение
        currentProposal = UpgradeProposal({
            implementation: newImplementation,
            timestamp: block.timestamp,
            initialized: true,
            voteCount: 0
        });
    }
    
    // Шаг 2: Голосование за обновление
    function voteForUpgrade() external onlyAdmin {
        require(
            currentProposal.initialized,
            "No proposal"
        );
        require(
            !currentProposal.votes[msg.sender],
            "Already voted"
        );
        
        currentProposal.votes[msg.sender] = true;
        currentProposal.voteCount++;
    }
    
    // Шаг 3: Выполнение обновления
    function executeUpgrade() external onlyAdmin {
        require(
            currentProposal.initialized,
            "No proposal"
        );
        require(
            block.timestamp >= 
                currentProposal.timestamp + TIMELOCK,
            "Timelock active"
        );
        require(
            currentProposal.voteCount >= MIN_VOTES,
            "Not enough votes"
        );
        
        // Проверяем совместимость
        _validateUpgrade(currentProposal.implementation);
        
        // Выполняем обновление
        _upgrade(currentProposal.implementation);
        
        // Сбрасываем предложение
        delete currentProposal;
    }
}
```

### **3. Проверки перед обновлением**

```solidity
contract UpgradeChecks {
    // 1. Проверка storage layout
    function _validateStorage(
        address newImplementation
    ) internal view {
        // Получаем layout старой имплементации
        bytes32 oldLayout = _getStorageLayout(
            _getImplementation()
        );
        
        // Получаем layout новой имплементации
        bytes32 newLayout = _getStorageLayout(
            newImplementation
        );
        
        // Проверяем совместимость
        require(
            _isCompatible(oldLayout, newLayout),
            "Incompatible storage"
        );
    }
    
    // 2. Проверка интерфейса
    function _validateInterface(
        address implementation
    ) internal view {
        // Проверяем наличие необходимых функций
        bytes4[] memory selectors = _getRequiredSelectors();
        
        for (uint i = 0; i < selectors.length; i++) {
            require(
                _implementsFunction(
                    implementation,
                    selectors[i]
                ),
                "Missing required function"
            );
        }
    }
    
    // 3. Проверка инициализации
    function _checkInitialization(
        address implementation
    ) internal view {
        // Проверяем, требуется ли инициализация
        bool needsInit = IUpgradeable(implementation)
            .needsInitialization();
            
        if (needsInit) {
            require(
                _hasInitFunction(implementation),
                "Missing initialize function"
            );
        }
    }
}
```

### **4. Различные способы обновления**

1. **Прямое обновление (не рекомендуется):**
```solidity
function upgradeImplementation(address newImpl) external {
    require(msg.sender == admin, "Not admin");
    _setImplementation(newImpl);
}
```

2. **Через Timelock:**
```solidity
contract TimelockUpgrade {
    uint256 public constant DELAY = 2 days;
    mapping(address => uint256) public upgradeSchedule;
    
    function scheduleUpgrade(
        address newImpl
    ) external onlyAdmin {
        upgradeSchedule[newImpl] = block.timestamp + DELAY;
    }
    
    function executeUpgrade(
        address newImpl
    ) external onlyAdmin {
        require(
            block.timestamp >= upgradeSchedule[newImpl],
            "Timelock active"
        );
        _setImplementation(newImpl);
    }
}
```

3. **Через Multisig:**
```solidity
contract MultisigUpgrade {
    uint256 public constant REQUIRED = 3;
    mapping(address => mapping(address => bool)) public hasVoted;
    mapping(address => uint256) public voteCount;
    
    function voteForUpgrade(
        address newImpl
    ) external onlyAdmin {
        require(!hasVoted[newImpl][msg.sender], "Already voted");
        
        hasVoted[newImpl][msg.sender] = true;
        voteCount[newImpl]++;
        
        if (voteCount[newImpl] >= REQUIRED) {
            _setImplementation(newImpl);
        }
    }
}
```

### **5. После обновления**

```solidity
contract PostUpgrade {
    // 1. Проверка успешности обновления
    function verifyUpgrade(
        address expectedImpl
    ) external view returns (bool) {
        // Проверяем адрес
        require(
            _getImplementation() == expectedImpl,
            "Wrong implementation"
        );
        
        // Проверяем работоспособность
        try IImplementation(address(this)).version() returns (
            string memory version
        ) {
            return true;
        } catch {
            return false;
        }
    }
    
    // 2. Откат при проблемах
    function rollbackUpgrade(
        address previousImpl
    ) external onlyAdmin {
        require(
            previousImpl.code.length > 0,
            "Not a contract"
        );
        
        _setImplementation(previousImpl);
        emit UpgradeRolledBack(previousImpl);
    }
}
```

---

## Связанные темы
- [[Расскажите подробно как работает паттерн proxy?]]
- [[Что такое storage collision?]]
- [[Какие типы proxy вы знаете?]]
- [[Как правильно обновлять proxy контракты?]]

---

## Источники
- [OpenZeppelin: Upgrading Smart Contracts](https://docs.openzeppelin.com/upgrades-plugins/1.x/writing-upgradeable)
- [EIP-1967: Standard Proxy Storage Slots](https://eips.ethereum.org/EIPS/eip-1967)
- [UUPS vs Transparent Proxy Pattern](https://docs.openzeppelin.com/upgrades-plugins/1.x/proxies#transparent-proxies-and-function-clashes) 