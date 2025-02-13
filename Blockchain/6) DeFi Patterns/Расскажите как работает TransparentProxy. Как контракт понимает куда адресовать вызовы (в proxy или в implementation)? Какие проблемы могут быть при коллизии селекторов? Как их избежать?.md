## Короткий ответ

TransparentProxy - это тип proxy контракта, который разделяет вызовы на основе адреса отправителя: если вызов идет от админа, он обрабатывается прокси контрактом, если от обычного пользователя - делегируется в имплементацию. Это решает проблему коллизии селекторов между прокси и имплементацией, но добавляет дополнительные газовые затраты на проверку отправителя.

---

## Подробный разбор

### **1. Базовая структура**

```solidity
contract TransparentProxy {
    // Слоты для хранения (EIP-1967)
    bytes32 private constant IMPLEMENTATION_SLOT = 
        0x360894a13ba1a3210667c828492db98dca3e2076cc3735a920a3ca505d382bbc;
    bytes32 private constant ADMIN_SLOT = 
        0xb53127684a568b3173ae13b9f8a6016e243e63b6e8ee1178d6a717850b5d6103;
    
    // Модификатор для админских функций
    modifier ifAdmin() {
        if (msg.sender == _admin()) {
            _;
        } else {
            _fallback();
        }
    }
    
    // Получение админа
    function _admin() internal view returns (address) {
        return StorageSlot.getAddressSlot(ADMIN_SLOT).value;
    }
    
    // Получение имплементации
    function _implementation() internal view returns (address) {
        return StorageSlot.getAddressSlot(
            IMPLEMENTATION_SLOT
        ).value;
    }
}
```

### **2. Механизм маршрутизации**

```solidity
contract ProxyDispatch {
    // Основная логика маршрутизации
    fallback() external payable {
        address _admin = _getAdmin();
        
        if (msg.sender == _admin) {
            // Админ может вызывать только админские функции
            require(
                !_isProxyFunction(msg.sig),
                "Admin cannot call implementation"
            );
            _fallback();
        } else {
            // Пользователи могут вызывать только
            // функции имплементации
            _delegate(_implementation());
        }
    }
    
    // Проверка селектора прокси
    function _isProxyFunction(
        bytes4 selector
    ) internal pure returns (bool) {
        // Список селекторов прокси
        bytes4[] memory selectors = new bytes4[](3);
        selectors[0] = this.upgradeTo.selector;
        selectors[1] = this.changeAdmin.selector;
        selectors[2] = this.implementation.selector;
        
        for (uint i = 0; i < selectors.length; i++) {
            if (selector == selectors[i]) {
                return true;
            }
        }
        
        return false;
    }
}
```

### **3. Проблема коллизии селекторов**

```solidity
contract SelectorCollision {
    // Пример коллизии
    contract Proxy {
        // upgradeTo(address)
        // селектор: 0x3659cfe6
        function upgradeTo(address newImpl) public {}
    }
    
    contract Implementation {
        // случайная функция с тем же селектором
        // calculateValue(uint256)
        // селектор: 0x3659cfe6
        function calculateValue(uint256 x) public {}
    }
    
    /*
    Проблемы:
    1. Одинаковые селекторы функций
    2. Неясно какую функцию вызывать
    3. Возможна потеря доступа к админским функциям
    */
}
```

### **4. Решение через TransparentProxy**

```solidity
contract TransparentSolution {
    // Админские функции
    function upgradeTo(
        address newImplementation
    ) external ifAdmin {
        _setImplementation(newImplementation);
    }
    
    function changeAdmin(address newAdmin) external ifAdmin {
        _setAdmin(newAdmin);
    }
    
    // Пользовательские вызовы
    fallback() external payable {
        if (msg.sender == _admin()) {
            revert("Admin cannot call fallback");
        }
        _delegate(_implementation());
    }
    
    // Делегирование
    function _delegate(address implementation) internal {
        assembly {
            calldatacopy(0, 0, calldatasize())
            
            let result := delegatecall(
                gas(),
                implementation,
                0,
                calldatasize(),
                0,
                0
            )
            
            returndatacopy(0, 0, returndatasize())
            
            switch result
            case 0 { revert(0, returndatasize()) }
            default { return(0, returndatasize()) }
        }
    }
}
```

### **5. Безопасное обновление**

```solidity
contract SafeTransparentProxy {
    // Структура для обновления
    struct PendingUpgrade {
        address implementation;
        uint256 timestamp;
    }
    
    // Timelock для обновлений
    uint256 public constant UPGRADE_DELAY = 2 days;
    PendingUpgrade public pendingUpgrade;
    
    // Предложение обновления
    function proposeUpgrade(
        address newImplementation
    ) external ifAdmin {
        require(
            newImplementation.code.length > 0,
            "Not a contract"
        );
        
        pendingUpgrade = PendingUpgrade({
            implementation: newImplementation,
            timestamp: block.timestamp
        });
    }
    
    // Выполнение обновления
    function executeUpgrade() external ifAdmin {
        require(
            block.timestamp >= 
                pendingUpgrade.timestamp + UPGRADE_DELAY,
            "Timelock active"
        );
        
        _setImplementation(pendingUpgrade.implementation);
        delete pendingUpgrade;
    }
}
```

### **6. Оптимизация газа**

```solidity
contract GasOptimizedProxy {
    // Кеширование админа
    address private immutable _ADMIN;
    
    constructor() {
        _ADMIN = msg.sender;
    }
    
    // Быстрая проверка админа
    modifier ifAdmin() {
        if (msg.sender == _ADMIN) {
            _;
        } else {
            _delegate(_implementation());
        }
    }
    
    // Оптимизированная проверка селектора
    function _isProxyFunction(
        bytes4 selector
    ) internal pure returns (bool) {
        // Используем битовую маску
        uint256 selector_mask = 
            0x3659cfe6 | // upgradeTo
            0x8f283970 | // changeAdmin
            0x5c60da1b;  // implementation
            
        return (uint32(selector) & selector_mask) == 
               uint32(selector);
    }
}
```

### **7. Безопасные паттерны**

```solidity
contract ProxyPatterns {
    // 1. Проверка совместимости
    function _validateImplementation(
        address implementation
    ) internal view {
        // Проверяем интерфейс
        require(
            implementation.code.length > 0,
            "Not a contract"
        );
        
        // Проверяем селекторы
        bytes4[] memory required = _requiredSelectors();
        for (uint i = 0; i < required.length; i++) {
            require(
                _implementsFunction(
                    implementation,
                    required[i]
                ),
                "Missing function"
            );
        }
    }
    
    // 2. Защита от случайных вызовов
    function _validateCall(
        address target,
        bytes memory data
    ) internal view {
        if (msg.sender == _admin()) {
            require(
                !_isProxyFunction(bytes4(data)),
                "Admin cannot call implementation"
            );
        }
    }
    
    // 3. Логирование изменений
    event AdminChanged(
        address previousAdmin,
        address newAdmin
    );
    
    event Upgraded(
        address indexed implementation
    );
}
```

### **8. Примеры использования**

```solidity
// Пример безопасного прокси
contract SafeTransparentProxy {
    // Админские функции
    function upgradeTo(
        address newImplementation
    ) external ifAdmin {
        _validateImplementation(newImplementation);
        _setImplementation(newImplementation);
        emit Upgraded(newImplementation);
    }
    
    function changeAdmin(address newAdmin) external ifAdmin {
        require(newAdmin != address(0), "Zero address");
        address oldAdmin = _admin();
        _setAdmin(newAdmin);
        emit AdminChanged(oldAdmin, newAdmin);
    }
    
    // Пользовательские вызовы
    fallback() external payable {
        require(
            msg.sender != _admin(),
            "Admin cannot call implementation"
        );
        _delegate(_implementation());
    }
    
    receive() external payable {
        require(
            msg.sender != _admin(),
            "Admin cannot call implementation"
        );
        _delegate(_implementation());
    }
}
```

---

## Связанные темы
- [[6. Список вопросов]]
- [[Расскажите подробно как работает паттерн proxy?]]
- [[Какие типы proxy вы знаете?]]
- [[Как правильно обновлять proxy контракты?]]

---

## Источники
- [EIP-1967: Standard Proxy Storage Slots](https://eips.ethereum.org/EIPS/eip-1967)
- [OpenZeppelin: TransparentUpgradeableProxy](https://docs.openzeppelin.com/contracts/4.x/api/proxy#TransparentUpgradeableProxy)
- [OpenZeppelin: Writing Upgradeable Contracts](https://docs.openzeppelin.com/upgrades-plugins/1.x/writing-upgradeable) 