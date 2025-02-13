## Короткий ответ

UUPS (Universal Upgradeable Proxy Standard) - это паттерн прокси, где логика обновления находится в имплементации, а не в прокси. Прокси контракт максимально простой и только делегирует вызовы, а вся логика управления обновлениями реализована в имплементации. Это экономит газ при вызовах, но требует особой осторожности, так как ошибка в логике обновления может сделать контракт необновляемым.

---

## Подробный разбор

### **1. Базовая структура**

```solidity
// Минимальный прокси
contract UUPSProxy {
    // Слот для имплементации (EIP-1967)
    bytes32 private constant IMPLEMENTATION_SLOT = 
        0x360894a13ba1a3210667c828492db98dca3e2076cc3735a920a3ca505d382bbc;
    
    constructor(
        address _implementation,
        bytes memory _data
    ) {
        _setImplementation(_implementation);
        if (_data.length > 0) {
            (bool success,) = _implementation.delegatecall(_data);
            require(success, "Initialization failed");
        }
    }
    
    // Делегирование всех вызовов
    fallback() external payable {
        _delegate(_getImplementation());
    }
    
    receive() external payable {
        _delegate(_getImplementation());
    }
}
```

### **2. Логика обновления в имплементации**

```solidity
// Базовая имплементация
contract UUPSUpgradeable {
    // Слот для имплементации
    bytes32 private constant IMPLEMENTATION_SLOT = 
        0x360894a13ba1a3210667c828492db98dca3e2076cc3735a920a3ca505d382bbc;
    
    // Модификатор для проверки прав
    modifier onlyProxy() {
        require(
            address(this) != _getImplementation(),
            "Function must be called through proxy"
        );
        _;
    }
    
    // Функция обновления
    function upgradeTo(
        address newImplementation
    ) external onlyProxy {
        _authorizeUpgrade(newImplementation);
        _upgradeToAndCall(
            newImplementation,
            new bytes(0),
            false
        );
    }
    
    // Функция для авторизации обновления
    function _authorizeUpgrade(
        address newImplementation
    ) internal virtual {
        // Должна быть переопределена
        revert("Upgrade not authorized");
    }
}
```

### **3. Механизм делегирования**

```solidity
contract UUPSDelegation {
    // Делегирование вызова
    function _delegate(address implementation) internal {
        assembly {
            // Копируем calldata
            calldatacopy(0, 0, calldatasize())
            
            // Выполняем delegatecall
            let result := delegatecall(
                gas(),
                implementation,
                0,
                calldatasize(),
                0,
                0
            )
            
            // Копируем результат
            returndatacopy(0, 0, returndatasize())
            
            switch result
            case 0 { revert(0, returndatasize()) }
            default { return(0, returndatasize()) }
        }
    }
    
    // Получение адреса имплементации
    function _getImplementation() internal view returns (address) {
        bytes32 slot = IMPLEMENTATION_SLOT;
        address impl;
        assembly {
            impl := sload(slot)
        }
        return impl;
    }
}
```

### **4. Безопасное обновление**

```solidity
contract SafeUUPS is UUPSUpgradeable {
    // Роли доступа
    bytes32 public constant UPGRADER_ROLE = 
        keccak256("UPGRADER_ROLE");
    
    // Timelock для обновлений
    uint256 public constant UPGRADE_DELAY = 2 days;
    
    struct UpgradeProposal {
        address implementation;
        uint256 timestamp;
        bool executed;
    }
    
    UpgradeProposal public currentProposal;
    
    // Предложение обновления
    function proposeUpgrade(
        address newImplementation
    ) external onlyRole(UPGRADER_ROLE) {
        require(
            newImplementation.code.length > 0,
            "Not a contract"
        );
        
        currentProposal = UpgradeProposal({
            implementation: newImplementation,
            timestamp: block.timestamp,
            executed: false
        });
    }
    
    // Выполнение обновления
    function executeUpgrade() external onlyRole(UPGRADER_ROLE) {
        require(
            block.timestamp >= 
                currentProposal.timestamp + UPGRADE_DELAY,
            "Timelock active"
        );
        
        require(!currentProposal.executed, "Already executed");
        
        _upgradeToAndCall(
            currentProposal.implementation,
            new bytes(0),
            false
        );
        
        currentProposal.executed = true;
    }
    
    // Авторизация обновления
    function _authorizeUpgrade(
        address newImplementation
    ) internal override onlyRole(UPGRADER_ROLE) {
        // Дополнительные проверки
        _validateUpgrade(newImplementation);
    }
}
```

### **5. Проверки безопасности**

```solidity
contract UUPSChecks {
    // 1. Проверка совместимости
    function _validateUpgrade(
        address newImplementation
    ) internal view {
        // Проверяем что это UUPS
        require(
            _isUUPSContract(newImplementation),
            "Not UUPS"
        );
        
        // Проверяем интерфейс
        require(
            _implementsRequired(newImplementation),
            "Missing interface"
        );
        
        // Проверяем storage layout
        require(
            _isStorageCompatible(newImplementation),
            "Incompatible storage"
        );
    }
    
    // 2. Проверка UUPS
    function _isUUPSContract(
        address implementation
    ) internal view returns (bool) {
        try IUUPS(implementation).proxiableUUID() returns (
            bytes32 uuid
        ) {
            return uuid == IMPLEMENTATION_SLOT;
        } catch {
            return false;
        }
    }
    
    // 3. Защита от ошибок
    modifier safeDelegateCall() {
        require(
            address(this) != _getImplementation(),
            "Cannot call on implementation"
        );
        _;
    }
}
```

### **6. Оптимизация газа**

```solidity
contract GasOptimizedUUPS {
    // 1. Кеширование проверок
    bool private _initialized;
    bool private _upgrading;
    
    modifier initializer() {
        require(
            !_initialized || _upgrading,
            "Already initialized"
        );
        
        bool isTopLevelCall = !_upgrading;
        if (isTopLevelCall) {
            _upgrading = true;
            _initialized = true;
        }
        
        _;
        
        if (isTopLevelCall) {
            _upgrading = false;
        }
    }
    
    // 2. Оптимизированное делегирование
    function _delegate(
        address implementation
    ) internal virtual {
        assembly {
            // Загружаем указатель свободной памяти
            let ptr := mload(0x40)
            
            // Копируем calldata
            calldatacopy(ptr, 0, calldatasize())
            
            // Делегируем вызов
            let result := delegatecall(
                gas(),
                implementation,
                ptr,
                calldatasize(),
                0,
                0
            )
            
            // Копируем результат
            let size := returndatasize()
            returndatacopy(ptr, 0, size)
            
            switch result
            case 0 { revert(ptr, size) }
            default { return(ptr, size) }
        }
    }
}
```

### **7. Примеры использования**

```solidity
// Пример токена с UUPS
contract UUPSToken is UUPSUpgradeable, ERC20Upgradeable {
    // Инициализация
    function initialize(
        string memory name,
        string memory symbol
    ) public initializer {
        __ERC20_init(name, symbol);
        _mint(msg.sender, 1000000 * 10**decimals());
    }
    
    // Авторизация обновления
    function _authorizeUpgrade(
        address newImplementation
    ) internal override onlyOwner {
        // Проверки перед обновлением
        require(
            IERC20Upgradeable(newImplementation).decimals() == 
            decimals(),
            "Invalid decimals"
        );
    }
    
    // Новая функциональность в V2
    function mint(
        address to,
        uint256 amount
    ) public onlyOwner {
        _mint(to, amount);
    }
}
```

### **8. Сравнение с TransparentProxy**

```solidity
contract ProxyComparison {
    /*
    UUPS:
    + Меньше газа на вызовы
    + Более гибкая логика обновления
    + Проще прокси контракт
    - Риск потери возможности обновления
    - Сложнее имплементация
    
    TransparentProxy:
    + Более безопасный
    + Проще имплементация
    + Четкое разделение админ/пользователь
    - Больше газа на вызовы
    - Сложнее прокси контракт
    */
}
```

---

## Связанные темы
- [[6. Список вопросов]]
- [[Расскажите подробно как работает паттерн proxy?]]
- [[Какие типы proxy вы знаете?]]
- [[Расскажите как работает TransparentProxy]]

---

## Источники
- [EIP-1822: Universal Upgradeable Proxy Standard](https://eips.ethereum.org/EIPS/eip-1822)
- [OpenZeppelin: UUPS Proxies](https://docs.openzeppelin.com/contracts/4.x/api/proxy#UUPSUpgradeable)
- [OpenZeppelin: Writing Upgradeable Contracts](https://docs.openzeppelin.com/upgrades-plugins/1.x/writing-upgradeable) 