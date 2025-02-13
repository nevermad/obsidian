## Короткий ответ

В OpenZeppelin Proxy контракте есть следующие основные функции: `fallback()`, `receive()`, `_delegate(address)`, `_implementation()`, `_fallback()`, `_beforeFallback()`. Из них только `fallback()` и `receive()` имеют селекторы, остальные - internal функции. Вызовы перенаправляются в имплементацию через `delegatecall` в `fallback()` функции, которая копирует calldata, выполняет делегирование и возвращает результат.

---

## Подробный разбор

### **1. Основные функции**

```solidity
contract Proxy {
    // Функции с селекторами
    
    // 1. fallback - основная функция делегирования
    fallback() external payable virtual {
        _fallback();
    }
    
    // 2. receive - для получения ETH
    receive() external payable virtual {
        _fallback();
    }
    
    // Internal функции
    
    // 3. Получение адреса имплементации
    function _implementation() internal view virtual returns (address);
    
    // 4. Основная логика делегирования
    function _delegate(address implementation) internal virtual {
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
            
            // Копируем возвращаемые данные
            returndatacopy(0, 0, returndatasize())
            
            switch result
            case 0 {
                revert(0, returndatasize())
            }
            default {
                return(0, returndatasize())
            }
        }
    }
    
    // 5. Логика перед делегированием
    function _fallback() internal virtual {
        _beforeFallback();
        _delegate(_implementation());
    }
    
    // 6. Хук перед делегированием
    function _beforeFallback() internal virtual {}
}
```

### **2. Механизм делегирования**

```solidity
contract ProxyDelegation {
    // Пример полного процесса делегирования
    fallback() external payable {
        // 1. Получаем адрес имплементации
        address implementation = _implementation();
        
        // 2. Проверяем адрес
        require(implementation != address(0), "No implementation");
        
        // 3. Копируем calldata и делегируем
        assembly {
            // Сохраняем указатель на свободную память
            let ptr := mload(0x40)
            
            // Копируем calldata
            calldatacopy(ptr, 0, calldatasize())
            
            // Выполняем delegatecall
            let result := delegatecall(
                gas(),
                implementation,
                ptr,
                calldatasize(),
                0,
                0
            )
            
            // Сохраняем размер возвращаемых данных
            let size := returndatasize()
            
            // Копируем возвращаемые данные
            returndatacopy(ptr, 0, size)
            
            // Обрабатываем результат
            switch result
            case 0 {
                revert(ptr, size)
            }
            default {
                return(ptr, size)
            }
        }
    }
}
```

### **3. Хранение адреса имплементации**

```solidity
contract ProxyStorage {
    // EIP-1967 слот для implementation
    bytes32 private constant IMPLEMENTATION_SLOT = 
        bytes32(uint256(keccak256("eip1967.proxy.implementation")) - 1);
    
    // Получение адреса имплементации
    function _implementation() internal view returns (address impl) {
        assembly {
            impl := sload(IMPLEMENTATION_SLOT)
        }
    }
    
    // Установка адреса имплементации
    function _setImplementation(address newImplementation) internal {
        require(
            Address.isContract(newImplementation),
            "Not a contract"
        );
        
        assembly {
            sstore(IMPLEMENTATION_SLOT, newImplementation)
        }
    }
}
```

### **4. Обработка различных типов вызовов**

```solidity
contract ProxyCallHandling {
    // 1. Обычный вызов функции
    fallback() external payable {
        _fallback();
    }
    
    // 2. Отправка ETH
    receive() external payable {
        _fallback();
    }
    
    // 3. Обработка revert
    function _delegate(address implementation) internal {
        assembly {
            // ... delegatecall ...
            
            // Если вызов завершился с ошибкой
            if iszero(result) {
                // Копируем сообщение об ошибке
                returndatacopy(0, 0, returndatasize())
                // Возвращаем ошибку с тем же сообщением
                revert(0, returndatasize())
            }
        }
    }
    
    // 4. Обработка возвращаемых данных
    function _delegateAndReturn(
        address implementation
    ) internal returns (bytes memory) {
        (bool success, bytes memory returndata) = implementation.delegatecall(
            msg.data
        );
        
        if (!success) {
            assembly {
                returndatacopy(0, 0, returndatasize())
                revert(0, returndatasize())
            }
        }
        
        return returndata;
    }
}
```

### **5. Безопасность делегирования**

```solidity
contract ProxySecurity {
    // 1. Проверка адреса имплементации
    modifier validImplementation(address implementation) {
        require(
            Address.isContract(implementation),
            "Not a contract"
        );
        require(
            implementation != address(this),
            "Cannot delegate to self"
        );
        _;
    }
    
    // 2. Защита от рекурсивных вызовов
    bool private _delegating;
    
    modifier nonReentrant() {
        require(!_delegating, "Reentrant call");
        _delegating = true;
        _;
        _delegating = false;
    }
    
    // 3. Проверка размера calldata
    function _fallback() internal virtual {
        require(
            msg.data.length > 0 || msg.value > 0,
            "Empty call"
        );
        _delegate(_implementation());
    }
    
    // 4. Защита admin функций
    function _beforeFallback() internal virtual {
        // Проверяем, не является ли вызов admin функцией
        if (msg.sig == UPGRADE_SELECTOR) {
            require(msg.sender == _admin(), "Not admin");
        }
    }
}
```

### **6. Оптимизации**

```solidity
contract ProxyOptimizations {
    // 1. Оптимизация gas при копировании calldata
    function _delegate(address implementation) internal {
        assembly {
            // Копируем только используемую часть calldata
            let ptr := mload(0x40)
            calldatacopy(
                ptr,
                0,
                calldatasize()
            )
            
            // Выполняем delegatecall
            let result := delegatecall(
                gas(),
                implementation,
                ptr,
                calldatasize(),
                0,
                0
            )
            
            // Освобождаем память
            mstore(0x40, add(ptr, calldatasize()))
        }
    }
    
    // 2. Кэширование адреса имплементации
    address private _cachedImplementation;
    uint256 private _cacheTimestamp;
    
    function _implementation() internal view returns (address) {
        if (block.timestamp - _cacheTimestamp < 1 hours) {
            return _cachedImplementation;
        }
        
        address impl = _loadImplementation();
        _cachedImplementation = impl;
        _cacheTimestamp = block.timestamp;
        return impl;
    }
}
```

---

## Связанные темы
- [[6. Список вопросов]]
- [[Как работает delegatecall?]]
- [[Какие значения msg.value, msg.sender при call, staticcall, delegatecall?]]
- [[Расскажите подробно как работает паттерн proxy?]]

---

## Источники
- [OpenZeppelin: Proxy Contract](https://github.com/OpenZeppelin/openzeppelin-contracts/blob/master/contracts/proxy/Proxy.sol)
- [EIP-1967: Standard Proxy Storage Slots](https://eips.ethereum.org/EIPS/eip-1967)
- [OpenZeppelin: Understanding Proxies](https://docs.openzeppelin.com/upgrades-plugins/1.x/proxies) 