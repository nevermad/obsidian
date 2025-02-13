## Короткий ответ

Unstructured storage - это паттерн хранения данных в смарт-контрактах, где переменные хранятся в псевдослучайных слотах, вычисляемых через keccak256 хеширование. Это позволяет избежать коллизий storage при наследовании и обновлении контрактов. Вероятность коллизии при 1000 слотов крайне мала (около 10^-37) из-за большого пространства хеширования (2^256).

---

## Подробный разбор

### **1. Базовый механизм**

```solidity
contract UnstructuredStorage {
    // Вычисление слота через keccak256
    bytes32 private constant OWNER_SLOT = 
        keccak256("com.example.owner");
    
    // Чтение из слота
    function owner() public view returns (address) {
        bytes32 slot = OWNER_SLOT;
        address value;
        assembly {
            value := sload(slot)
        }
        return value;
    }
    
    // Запись в слот
    function setOwner(address newOwner) public {
        bytes32 slot = OWNER_SLOT;
        assembly {
            sstore(slot, newOwner)
        }
    }
}
```

### **2. Расчет вероятности коллизий**

```solidity
contract CollisionProbability {
    /*
    Вероятность коллизии для n слотов:
    P(collision) = 1 - e^(-n^2 / (2 * 2^256))
    
    Для 1000 слотов:
    n = 1000
    2^256 ≈ 1.1579209e+77
    
    P = 1 - e^(-1000^2 / (2 * 1.1579209e+77))
    P = 1 - e^(-1e6 / 2.3158418e+77)
    P ≈ 4.3168e-37
    
    Это означает, что вероятность коллизии
    практически равна нулю
    */
    
    function calculateCollisionProbability(
        uint256 n
    ) public pure returns (uint256) {
        // n - количество слотов
        // Возвращает вероятность * 1e18
        
        uint256 slots = 2**256;
        uint256 collisions = (n * (n - 1)) / 2;
        
        return (collisions * 1e18) / slots;
    }
}
```

### **3. Организация хранилища**

```solidity
contract StorageOrganization {
    // 1. Префиксы для доменов
    bytes32 private constant PREFIX_ACCESS = 
        keccak256("access");
    bytes32 private constant PREFIX_TOKEN = 
        keccak256("token");
    bytes32 private constant PREFIX_CONFIG = 
        keccak256("config");
    
    // 2. Генерация слотов
    function getSlot(
        bytes32 prefix,
        string memory name
    ) internal pure returns (bytes32) {
        return keccak256(
            abi.encodePacked(prefix, ".", name)
        );
    }
    
    // 3. Организация переменных по доменам
    bytes32 private constant OWNER_SLOT = 
        keccak256(
            abi.encodePacked(PREFIX_ACCESS, ".owner")
        );
    
    bytes32 private constant TOTAL_SUPPLY_SLOT = 
        keccak256(
            abi.encodePacked(PREFIX_TOKEN, ".totalSupply")
        );
}
```

### **4. Работа с разными типами данных**

```solidity
contract UnstructuredTypes {
    // Простые типы
    function setUint(bytes32 slot, uint256 value) internal {
        assembly {
            sstore(slot, value)
        }
    }
    
    // Строки и массивы
    function setString(
        bytes32 slot,
        string memory value
    ) internal {
        bytes32 hashedSlot = keccak256(
            abi.encodePacked(slot)
        );
        
        assembly {
            // Сохраняем длину
            sstore(slot, mload(value))
            
            // Сохраняем данные
            let length := mload(value)
            let data := add(value, 0x20)
            
            for { let i := 0 } 
                lt(i, length) 
                { i := add(i, 32) } 
            {
                sstore(
                    add(hashedSlot, i),
                    mload(add(data, i))
                )
            }
        }
    }
    
    // Маппинги
    function mappingSlot(
        bytes32 slot,
        address key
    ) internal pure returns (bytes32) {
        return keccak256(
            abi.encodePacked(key, slot)
        );
    }
}
```

### **5. Преимущества и недостатки**

```solidity
contract StorageComparison {
    /*
    Преимущества:
    1. Нет коллизий при наследовании
    2. Гибкое добавление переменных
    3. Безопасное обновление контрактов
    4. Изоляция хранилища
    
    Недостатки:
    1. Больше газа на доступ
    2. Сложнее читать код
    3. Нужно управлять слотами
    4. Возможны ошибки при генерации ключей
    */
}
```

### **6. Безопасное использование**

```solidity
contract SafeUnstructuredStorage {
    // 1. Проверка существования слота
    function exists(bytes32 slot) internal view returns (bool) {
        uint256 value;
        assembly {
            value := sload(slot)
        }
        return value != 0;
    }
    
    // 2. Атомарные операции
    function incrementCounter(
        bytes32 slot
    ) internal returns (uint256) {
        uint256 value;
        assembly {
            value := add(sload(slot), 1)
            sstore(slot, value)
        }
        return value;
    }
    
    // 3. Защита от перезаписи
    modifier protectSlot(bytes32 slot) {
        require(!exists(slot), "Slot already used");
        _;
    }
}
```

### **7. Примеры использования**

```solidity
// Пример прокси контракта
contract UnstructuredProxy {
    // Слот для адреса имплементации
    bytes32 private constant IMPLEMENTATION_SLOT = 
        keccak256("proxy.implementation");
    
    // Слот для админа
    bytes32 private constant ADMIN_SLOT = 
        keccak256("proxy.admin");
    
    function _delegate(address implementation) internal {
        assembly {
            // Копируем calldata
            calldatacopy(0, 0, calldatasize())
            
            // Делегируем вызов
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
}

// Пример токена
contract UnstructuredToken {
    bytes32 private constant TOTAL_SUPPLY_SLOT = 
        keccak256("token.totalSupply");
    
    function balanceSlot(
        address account
    ) private pure returns (bytes32) {
        return keccak256(
            abi.encodePacked("token.balance", account)
        );
    }
    
    function transfer(
        address to,
        uint256 amount
    ) public returns (bool) {
        address from = msg.sender;
        bytes32 fromSlot = balanceSlot(from);
        bytes32 toSlot = balanceSlot(to);
        
        uint256 fromBalance;
        assembly {
            fromBalance := sload(fromSlot)
        }
        
        require(fromBalance >= amount, "Insufficient");
        
        assembly {
            sstore(fromSlot, sub(fromBalance, amount))
            sstore(toSlot, add(sload(toSlot), amount))
        }
        
        return true;
    }
}
```

### **8. Тестирование коллизий**

```solidity
contract CollisionTest {
    // Генерация тестовых слотов
    function generateTestSlots(
        uint256 count
    ) public pure returns (bytes32[] memory) {
        bytes32[] memory slots = new bytes32[](count);
        
        for (uint256 i = 0; i < count; i++) {
            slots[i] = keccak256(
                abi.encodePacked("test.slot.", i)
            );
        }
        
        return slots;
    }
    
    // Проверка коллизий
    function checkCollisions(
        bytes32[] memory slots
    ) public pure returns (bool) {
        for (uint256 i = 0; i < slots.length; i++) {
            for (uint256 j = i + 1; j < slots.length; j++) {
                if (slots[i] == slots[j]) {
                    return true;
                }
            }
        }
        return false;
    }
}
```

---

## Связанные темы
- [[6. Список вопросов]]
- [[Расскажите подробно как работает паттерн proxy?]]
- [[Что такое storage collision?]]
- [[Что такое и как работает Eternal storage?]]

---

## Источники
- [EIP-1967: Standard Proxy Storage Slots](https://eips.ethereum.org/EIPS/eip-1967)
- [OpenZeppelin: Writing Upgradeable Contracts](https://docs.openzeppelin.com/upgrades-plugins/1.x/writing-upgradeable)
- [Birthday Problem](https://en.wikipedia.org/wiki/Birthday_problem) 