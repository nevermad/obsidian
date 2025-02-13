## Короткий ответ

Storage collision (коллизия хранилища) - это проблема в смарт-контрактах, когда переменные в разных контрактах занимают одни и те же слоты хранилища. Особенно опасно в proxy паттернах, где при использовании delegatecall переменные прокси и имплементации могут конфликтовать, что приводит к повреждению данных.

---

## Подробный разбор

### **1. Механизм возникновения**

```solidity
// Прокси контракт
contract Proxy {
    // slot 0
    address public implementation;
    // slot 1
    address public admin;
}

// Контракт имплементации
contract Implementation {
    // slot 0 - конфликт с implementation!
    uint256 public value;
    // slot 1 - конфликт с admin!
    mapping(address => uint256) public balances;
}
```

### **2. Последствия коллизий**

```solidity
contract StorageCollisionExample {
    // В прокси
    address public implementation; // slot 0: 0x123...
    
    // В имплементации
    uint256 public value; // slot 0: перезапишет implementation!
    
    function setValue(uint256 _value) external {
        // При вызове через delegatecall
        value = _value; // Перезапишет адрес implementation!
        // Теперь прокси указывает на неверный адрес
    }
}
```

### **3. Решения**

1. **Unstructured Storage:**
```solidity
contract UnstructuredStorageProxy {
    // Используем случайные слоты через хеширование
    bytes32 private constant IMPLEMENTATION_SLOT = 
        keccak256("eip1967.proxy.implementation");
    
    function _setImplementation(address _impl) internal {
        assembly {
            sstore(IMPLEMENTATION_SLOT, _impl)
        }
    }
}
```

2. **Стандартизированные слоты (EIP-1967):**
```solidity
contract EIP1967Proxy {
    // Предопределенные слоты
    bytes32 private constant IMPLEMENTATION_SLOT = 
        0x360894a13ba1a3210667c828492db98dca3e2076cc3735a920a3ca505d382bbc;
    bytes32 private constant ADMIN_SLOT = 
        0xb53127684a568b3173ae13b9f8a6016e243e63b6e8ee1178d6a717850b5d6103;
    
    function _getImplementation() internal view returns (address impl) {
        assembly {
            impl := sload(IMPLEMENTATION_SLOT)
        }
    }
}
```

3. **Наследование с правильным порядком:**
```solidity
// Базовый контракт с переменными прокси
contract ProxyStorage {
    address private _implementation;
    address private _admin;
}

// Имплементация наследует storage layout
contract Implementation is ProxyStorage {
    // Новые переменные добавляются после
    uint256 public value;
    mapping(address => uint256) public balances;
}
```

### **4. Предотвращение коллизий**

1. **Проверка storage layout:**
```solidity
contract StorageChecker {
    function getStorageLayout() external pure returns (bytes32[] memory slots) {
        // Инструмент для анализа layout
        // Например, hardhat-storage-layout
    }
    
    function validateUpgrade(
        address newImplementation
    ) external view {
        // Проверка совместимости storage
        require(
            _isStorageLayoutCompatible(newImplementation),
            "Incompatible storage layout"
        );
    }
}
```

2. **Изолированное хранилище:**
```solidity
contract IsolatedStorage {
    // Отдельное пространство для каждого модуля
    mapping(bytes32 => mapping(bytes32 => uint256)) private _storage;
    
    function _setValue(
        bytes32 namespace,
        bytes32 key,
        uint256 value
    ) internal {
        _storage[namespace][key] = value;
    }
    
    function _getValue(
        bytes32 namespace,
        bytes32 key
    ) internal view returns (uint256) {
        return _storage[namespace][key];
    }
}
```

### **5. Лучшие практики**

```solidity
contract BestPractices {
    // 1. Использование констант для слотов
    bytes32 private constant NAMESPACE = 
        keccak256("com.example.contract");
    
    // 2. Документирование storage layout
    /// @custom:storage-location eip1967
    address public implementation;
    
    // 3. Проверки при обновлении
    function _authorizeUpgrade(
        address newImplementation
    ) internal {
        // Валидация storage layout
        // Проверка версий
        // Аудит безопасности
    }
}
```

---

## Связанные темы
- [[6. Список вопросов]]
- [[Расскажите подробно как работает паттерн proxy?]]
- [[Как работает delegatecall?]]
- [[Как правильно обновлять proxy контракты?]]

---

## Источники
- [EIP-1967: Standard Proxy Storage Slots](https://eips.ethereum.org/EIPS/eip-1967)
- [OpenZeppelin: Proxy Storage Slots](https://docs.openzeppelin.com/upgrades-plugins/1.x/proxies#storage-collisions)
- [Solidity Storage Layout Documentation](https://docs.soliditylang.org/en/latest/internals/layout_in_storage.html) 