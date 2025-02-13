## Короткий ответ

Storage proxy контракта должен быть согласован со storage implementation контракта, так как при delegatecall они используют одни и те же слоты. Основные ограничения: порядок переменных должен сохраняться при обновлениях, нельзя удалять существующие переменные, новые переменные можно добавлять только в конец, необходимо использовать gap slots для будущих обновлений. Для согласования используются паттерны inherited storage, unstructured storage и eternal storage.

---

## Подробный разбор

### **1. Структура storage**

```solidity
// Базовый контракт с storage
contract StorageLayout {
    // Слот 0
    uint256 public value1;
    // Слот 1
    address public value2;
    // Слот 2
    mapping(address => uint256) public value3;
    // Слот 3
    uint256[] public value4;
    
    // Gap для будущих обновлений
    uint256[50] private __gap;
}

// Правильное обновление
contract StorageV2 is StorageLayout {
    // Новые переменные после gap
    uint256 public newValue1;
    address public newValue2;
}

// Неправильное обновление - нарушает layout
contract StorageV2Wrong is StorageLayout {
    // ❌ Новая переменная между существующими
    uint256 public newValue;
    uint256 public value1; // Конфликт со слотом 0
}
```

### **2. Inherited Storage паттерн**

```solidity
// Базовый контракт с storage
contract Storage {
    bytes32 internal constant ADMIN_SLOT = 
        bytes32(uint256(keccak256("admin.slot")) - 1);
    bytes32 internal constant IMPLEMENTATION_SLOT = 
        bytes32(uint256(keccak256("implementation.slot")) - 1);
        
    function _setAdmin(address admin) internal {
        assembly {
            sstore(ADMIN_SLOT, admin)
        }
    }
    
    function _setImplementation(address implementation) internal {
        assembly {
            sstore(IMPLEMENTATION_SLOT, implementation)
        }
    }
}

// Прокси наследует storage
contract Proxy is Storage {
    constructor(address _logic) {
        _setImplementation(_logic);
        _setAdmin(msg.sender);
    }
    
    fallback() external payable {
        _delegate(_getImplementation());
    }
}

// Имплементация также наследует storage
contract Implementation is Storage {
    // Все переменные добавляются после storage
    uint256 public value;
    
    function setValue(uint256 _value) external {
        require(msg.sender == _getAdmin(), "Not admin");
        value = _value;
    }
}
```

### **3. Unstructured Storage**

```solidity
contract UnstructuredProxy {
    // Использование хешей для определения слотов
    function _implementation() internal view returns (address impl) {
        bytes32 slot = bytes32(uint256(keccak256("eip1967.proxy.implementation")) - 1);
        assembly {
            impl := sload(slot)
        }
    }
    
    function _setImplementation(address newImplementation) internal {
        bytes32 slot = bytes32(uint256(keccak256("eip1967.proxy.implementation")) - 1);
        assembly {
            sstore(slot, newImplementation)
        }
    }
}

contract UnstructuredImplementation {
    // Использование хешей для переменных
    function _setValue(uint256 value) internal {
        bytes32 slot = keccak256("my.contract.value");
        assembly {
            sstore(slot, value)
        }
    }
    
    function _getValue() internal view returns (uint256 value) {
        bytes32 slot = keccak256("my.contract.value");
        assembly {
            value := sload(slot)
        }
    }
}
```

### **4. Gap Slots**

```solidity
contract BaseWithGap {
    uint256 public value1;
    uint256 public value2;
    
    // Резервируем слоты для будущих версий
    uint256[50] private __gap;
}

contract UpgradedVersion is BaseWithGap {
    // Новые переменные используют gap слоты
    uint256 public value3;
    uint256 public value4;
    
    // Оставшиеся gap слоты
    uint256[48] private __gap;
}

// Пример расчета необходимого количества gap слотов
contract StorageCalculator {
    struct ComplexStruct {
        uint256 a;     // 1 слот
        address b;     // 1 слот
        uint256[] c;   // 1 слот (длина массива)
        mapping(address => uint256) d; // 1 слот
    }
    
    // Всего используется 4 слота
    ComplexStruct public data;
    
    // Резервируем слоты с запасом
    uint256[46] private __gap; // 50 - 4 = 46
}
```

### **5. Валидация storage**

```solidity
contract StorageValidator {
    // Проверка layout при обновлении
    function validateStorage(
        address oldImpl,
        address newImpl
    ) external view returns (bool) {
        // Получаем хеш storage layout
        bytes32 oldHash = _getStorageHash(oldImpl);
        bytes32 newHash = _getStorageHash(newImpl);
        
        // Проверяем совместимость
        if (oldHash != newHash) {
            // Детальная проверка
            return _validateStorageCompatibility(
                oldImpl,
                newImpl
            );
        }
        
        return true;
    }
    
    // Проверка совместимости переменных
    function _validateStorageCompatibility(
        address oldImpl,
        address newImpl
    ) internal view returns (bool) {
        assembly {
            // Проверяем первые 100 слотов
            for { let i := 0 } lt(i, 100) { i := add(i, 1) }
            {
                let oldValue := sload(i)
                let newValue := sload(i)
                
                // Значения должны совпадать
                if iszero(eq(oldValue, newValue)) {
                    revert(0, 0)
                }
            }
        }
        return true;
    }
}
```

### **6. Лучшие практики**

```solidity
// 1. Использование констант для слотов
contract StorageBestPractices {
    bytes32 private constant SLOT_1 = keccak256("slot.1");
    bytes32 private constant SLOT_2 = keccak256("slot.2");
    
    function _setValue(uint256 value) internal {
        assembly {
            sstore(SLOT_1, value)
        }
    }
}

// 2. Документирование storage layout
contract DocumentedStorage {
    /// @custom:storage-location eip1967.proxy.implementation
    address internal _implementation;
    
    /// @custom:storage-location eip1967.proxy.admin
    address internal _admin;
    
    /// @custom:storage-location eip1967.proxy.beacon
    address internal _beacon;
}

// 3. Проверки при обновлении
contract SafeUpgrade {
    function upgradeTo(address newImpl) external {
        // Проверка storage layout
        require(
            _validateStorage(newImpl),
            "Incompatible storage"
        );
        
        // Проверка интерфейса
        require(
            _validateInterface(newImpl),
            "Incompatible interface"
        );
        
        _setImplementation(newImpl);
    }
}
```

---

## Связанные темы
- [[6. Список вопросов]]
- [[Что такое storage collision?]]
- [[Расскажите о паттерне inherited storage]]
- [[Расскажите о Unstructured storage]]

---

## Источники
- [OpenZeppelin: Writing Upgradeable Contracts](https://docs.openzeppelin.com/upgrades-plugins/1.x/writing-upgradeable)
- [EIP-1967: Standard Proxy Storage Slots](https://eips.ethereum.org/EIPS/eip-1967)
- [Solidity Storage Layout](https://docs.soliditylang.org/en/latest/internals/layout_in_storage.html) 