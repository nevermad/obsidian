## Короткий ответ

Основные типы proxy контрактов:
1. **Transparent Proxy** - разделяет логику для админа и пользователей
2. **UUPS (Universal Upgradeable Proxy Standard)** - логика обновления находится в имплементации
3. **Beacon Proxy** - множество прокси используют одну имплементацию через Beacon контракт
4. **Minimal Proxy (EIP-1167)** - легковесный клон контракта без возможности обновления

---

## Подробный разбор

### **1. Transparent Proxy**

```solidity
contract TransparentProxy {
    address private _admin;
    address private _implementation;
    
    modifier ifAdmin() {
        if (msg.sender == _admin) {
            _;
        } else {
            _fallback();
        }
    }
    
    function upgradeTo(address newImplementation) external ifAdmin {
        _implementation = newImplementation;
    }
    
    function _fallback() internal {
        // Если вызывающий - админ, запрещаем вызов функций имплементации
        require(
            msg.sender != _admin,
            "Admin cannot call implementation"
        );
        
        // Делегируем вызов имплементации
        _delegate(_implementation);
    }
}
```

**Преимущества:**
- Четкое разделение админских и пользовательских функций
- Предотвращает function clashing

**Недостатки:**
- Дополнительные газовые затраты на проверку админа
- Сложная логика разделения доступа

### **2. UUPS Proxy**

```solidity
contract UUPSProxy {
    address private _implementation;
    
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
    
    fallback() external payable {
        _delegate(_implementation);
    }
}

contract UUPSImplementation {
    // Логика обновления в имплементации
    function upgradeTo(address newImplementation) external {
        require(msg.sender == _getAdmin(), "Not authorized");
        _authorizeUpgrade(newImplementation);
        _setImplementation(newImplementation);
    }
    
    function _authorizeUpgrade(address) internal virtual {
        // Проверки перед обновлением
    }
}
```

**Преимущества:**
- Меньше газовых затрат
- Более гибкая логика обновления
- Совместим с EIP-1822

**Недостатки:**
- Риск потери возможности обновления при ошибке в имплементации
- Необходимость дублировать логику обновления в каждой имплементации

### **3. Beacon Proxy**

```solidity
contract BeaconProxy {
    // Адрес Beacon контракта
    address private immutable _beacon;
    
    constructor(address beacon) {
        _beacon = beacon;
    }
    
    function _implementation() internal view returns (address) {
        return IBeacon(_beacon).implementation();
    }
    
    fallback() external payable {
        _delegate(_implementation());
    }
}

contract UpgradeableBeacon {
    address private _implementation;
    address private _owner;
    
    function implementation() external view returns (address) {
        return _implementation;
    }
    
    function upgradeTo(address newImplementation) external {
        require(msg.sender == _owner, "Not authorized");
        _implementation = newImplementation;
    }
}
```

**Преимущества:**
- Централизованное обновление множества прокси
- Экономия газа при массовом развертывании
- Упрощенное управление версиями

**Недостатки:**
- Дополнительный вызов для получения адреса имплементации
- Единая точка отказа в Beacon контракте

### **4. Minimal Proxy (EIP-1167)**

```solidity
contract MinimalProxy {
    constructor(address implementation) {
        // Создаем байткод для клона
        assembly {
            mstore(0x0, 0x3d602d80600a3d3981f3363d3d373d3d3d363d73)
            mstore(0x14, implementation)
            mstore(0x28, 0x5af43d82803e903d91602b57fd5bf3)
            
            // Создаем контракт
            let clone := create(
                0,
                0x0,
                0x37
            )
        }
    }
}
```

**Преимущества:**
- Минимальные затраты газа на развертывание
- Простота и надежность
- Идеален для фабрик контрактов

**Недостатки:**
- Нет возможности обновления
- Полная зависимость от оригинального контракта

### **5. Сравнение типов**

```solidity
contract ProxyComparison {
    // Газовые затраты (приблизительно)
    struct GasCosts {
        uint256 deployment;
        uint256 calls;
        uint256 upgrade;
    }
    
    function getGasCosts() pure returns (
        mapping(string => GasCosts) memory
    ) {
        return {
            "Transparent": GasCosts(
                500000,  // deployment
                3000,    // calls overhead
                100000   // upgrade
            ),
            "UUPS": GasCosts(
                400000,  // deployment
                2000,    // calls overhead
                80000    // upgrade
            ),
            "Beacon": GasCosts(
                450000,  // deployment
                3500,    // calls overhead
                50000    // upgrade
            ),
            "Minimal": GasCosts(
                100000,  // deployment
                2000,    // calls overhead
                0        // no upgrade
            )
        };
    }
}
```

### **6. Выбор типа прокси**

1. **Используйте Transparent Proxy если:**
   - Безопасность важнее газовых затрат
   - Нужно четкое разделение админских и пользовательских функций

2. **Используйте UUPS если:**
   - Важна оптимизация газа
   - Нужна гибкая логика обновления
   - Готовы тщательно тестировать имплементацию

3. **Используйте Beacon Proxy если:**
   - Нужно много одинаковых прокси
   - Требуется централизованное обновление
   - Важна экономия при массовом развертывании

4. **Используйте Minimal Proxy если:**
   - Не требуется обновление
   - Критична экономия газа
   - Нужны простые клоны контрактов

---

## Связанные темы
- [[Расскажите подробно как работает паттерн proxy?]]
- [[Что такое storage collision?]]
- [[Как правильно обновлять proxy контракты?]]

---

## Источники
- [EIP-1967: Standard Proxy Storage Slots](https://eips.ethereum.org/EIPS/eip-1967)
- [EIP-1822: Universal Upgradeable Proxy Standard (UUPS)](https://eips.ethereum.org/EIPS/eip-1822)
- [EIP-1167: Minimal Proxy Contract](https://eips.ethereum.org/EIPS/eip-1167)
- [OpenZeppelin: Proxy Patterns](https://docs.openzeppelin.com/upgrades-plugins/1.x/proxies) 