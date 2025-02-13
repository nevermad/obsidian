## Короткий ответ

Inherited storage - это паттерн организации хранилища в Solidity, где переменные состояния наследуются и располагаются в слотах хранилища в порядке линеаризации C3. При множественном наследовании порядок определяется от наиболее базового к наиболее производному контракту, с учетом правил разрешения конфликтов C3 линеаризации.

---

## Подробный разбор

### **1. Базовая структура storage**

```solidity
// Базовый контракт
contract Base {
    // slot 0
    uint256 public baseVar;
    
    // slot 1
    address public baseAddress;
}

// Наследник
contract Derived is Base {
    // slot 2 (после baseVar и baseAddress)
    uint256 public derivedVar;
    
    // slot 3
    mapping(address => uint256) public balances;
}
```

### **2. Порядок наследования A: B and C**

```solidity
// B контракт
contract B {
    // slot 0
    uint256 public b1;
    // slot 1
    uint256 public b2;
}

// C контракт
contract C {
    // slot 0
    uint256 public c1;
    // slot 1
    uint256 public c2;
}

// A наследует B и C
contract A is B, C {
    // Порядок слотов:
    // 0: B.b1
    // 1: B.b2
    // 2: C.c1
    // 3: C.c2
    // 4: A.a1
    uint256 public a1;
}
```

### **3. Множественное наследование**

```solidity
// C - базовый контракт
contract C {
    // slot 0
    uint256 public c1;
}

// B наследует C
contract B is C {
    // slot 1 (после C.c1)
    uint256 public b1;
}

// D наследует C
contract D is C {
    // slot 1 (после C.c1)
    uint256 public d1;
}

// A наследует B и D
contract A is B, D {
    // Порядок линеаризации: A -> B -> D -> C
    // Порядок слотов:
    // 0: C.c1 (из C)
    // 1: B.b1 (из B)
    // 2: D.d1 (из D)
    // 3: A.a1 (из A)
    uint256 public a1;
}
```

### **4. C3 Линеаризация**

```solidity
contract LinearizationExample {
    // Пример линеаризации для:
    //     X
    //    / \
    //   Y   A
    //  / \ /
    // B   C
    //  \ /
    //   D

    // Порядок линеаризации: X + merge(
    //     (Y + merge(
    //         (B + merge((D), ())),
    //         (C + merge((D), ()))
    //     )),
    //     (A + merge(
    //         (C + merge((D), ()))
    //     )),
    //     ()
    // )
    
    // Результат: X -> Y -> A -> B -> C -> D
}
```

### **5. Правила размещения переменных**

```solidity
contract StorageRules {
    // 1. Фиксированный размер
    uint256 public fixed1; // 32 bytes, 1 slot
    address public addr;   // 20 bytes, 1 slot
    
    // 2. Упаковка переменных
    uint128 public small1; // 16 bytes
    uint128 public small2; // 16 bytes
    // small1 и small2 упакованы в 1 слот
    
    // 3. Динамический размер
    mapping(address => uint256) public map1; // 1 slot (указатель)
    uint256[] public array1;                 // 1 slot (длина)
    
    // 4. Порядок определяет упаковку
    uint8 public tiny1;   // 1 byte
    uint256 public big1;  // 32 bytes (новый слот)
    uint8 public tiny2;   // 1 byte (новый слот)
}
```

### **6. Особенности и проблемы**

```solidity
contract StorageIssues {
    // 1. Коллизии имен
    uint256 public value;
    
    function setValue(uint256 newValue) public {
        // Какой value обновляется?
        value = newValue;
    }
    
    // 2. Теневое наследование
    function getValue() public view returns (uint256) {
        // Какой value читается?
        return value;
    }
    
    // 3. Порядок инициализации
    constructor() {
        // Важен порядок инициализации
        _initializeBase();
        _initializeDerived();
    }
}
```

### **7. Лучшие практики**

```solidity
// 1. Использование абстрактных контрактов
abstract contract StorageLayout {
    // Определяем базовый layout
    uint256 internal _value;
    mapping(address => uint256) internal _balances;
}

// 2. Документирование layout
contract DocumentedStorage is StorageLayout {
    /// @custom:storage-location eip1967
    uint256 public override value;
}

// 3. Использование gaps
contract UpgradeableStorage {
    uint256[50] private __gap;
    
    // Новые переменные можно добавлять
    // после gap
}

// 4. Изоляция storage
contract IsolatedStorage {
    // Отдельное пространство для каждого модуля
    mapping(bytes32 => mapping(bytes32 => bytes32))
        private _storage;
}
```

### **8. Пример полного контракта**

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract StorageExample {
    // Базовый storage layout
    struct StorageLayout {
        uint256 value;
        address owner;
        mapping(address => uint256) balances;
        uint256[] data;
    }
    
    // Слот для хранения структуры
    bytes32 private constant STORAGE_SLOT = 
        keccak256("example.storage");
        
    function _getStorage() 
        private 
        pure 
        returns (StorageLayout storage s) 
    {
        bytes32 slot = STORAGE_SLOT;
        assembly {
            s.slot := slot
        }
    }
    
    // Безопасное обновление
    function _setValue(uint256 newValue) internal {
        StorageLayout storage s = _getStorage();
        s.value = newValue;
    }
    
    // Безопасное чтение
    function getValue() 
        public 
        view 
        returns (uint256) 
    {
        return _getStorage().value;
    }
}
```

---

## Связанные темы
- [[6. Список вопросов]]
- [[Расскажите подробно как работает паттерн proxy?]]
- [[Что такое storage collision?]]
- [[Для чего используются gap переменные?]]

---

## Источники
- [Solidity Storage Layout](https://docs.soliditylang.org/en/latest/internals/layout_in_storage.html)
- [OpenZeppelin: Writing Upgradeable Contracts](https://docs.openzeppelin.com/upgrades-plugins/1.x/writing-upgradeable)
- [C3 Linearization Algorithm](https://en.wikipedia.org/wiki/C3_linearization) 