## Короткий ответ

Proxy паттерн - это механизм обновляемых смарт-контрактов, где логика (implementation) и состояние (storage) разделены. Прокси-контракт хранит состояние и делегирует выполнение кода имплементации через delegatecall. Это позволяет обновлять логику контракта, сохраняя его состояние и адрес.

---

## Подробный разбор

### **1. Базовая структура**

```solidity
contract Proxy {
    // Слот для адреса имплементации (EIP-1967)
    bytes32 private constant IMPLEMENTATION_SLOT = 
        0x360894a13ba1a3210667c828492db98dca3e2076cc3735a920a3ca505d382bbc;
    
    // Хранение состояния
    uint256 public value;
    
    // Получение адреса имплементации
    function _implementation() internal view returns (address impl) {
        assembly {
            impl := sload(IMPLEMENTATION_SLOT)
        }
    }
    
    // Делегирование вызовов
    fallback() external payable {
        _delegate(_implementation());
    }
    
    receive() external payable {
        _delegate(_implementation());
    }
    
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

### **2. Хранение данных**

1. **Storage layout:**
   ```solidity
   contract ProxyStorage {
       // Прокси хранит состояние
       uint256 public value;          // slot 0
       address public owner;          // slot 1
       mapping(address => uint256) public balances; // slot 2
       
       // Имплементация должна иметь такой же layout
       contract Implementation {
           uint256 public value;      // slot 0
           address public owner;      // slot 1
           mapping(address => uint256) public balances; // slot 2
           
           // Новые переменные можно добавлять только в конец
           uint256 public newVariable; // slot 3
       }
   }
   ```

2. **Unstructured Storage:**
   ```solidity
   contract UnstructuredStorage {
       // Хранение критических переменных в случайных слотах
       bytes32 private constant ADMIN_SLOT = keccak256("admin.slot");
       
       function _setAdmin(address admin) internal {
           assembly {
               sstore(ADMIN_SLOT, admin)
           }
       }
       
       function _getAdmin() internal view returns (address admin) {
           assembly {
               admin := sload(ADMIN_SLOT)
           }
       }
   }
   ```

### **3. Обновление имплементации**

```solidity
contract UpgradeableProxy is Proxy {
    bytes32 private constant ADMIN_SLOT = 
        0xb53127684a568b3173ae13b9f8a6016e243e63b6e8ee1178d6a717850b5d6103;
    
    modifier onlyAdmin() {
        require(msg.sender == _getAdmin(), "Not admin");
        _;
    }
    
    function upgradeTo(address newImplementation) external onlyAdmin {
        _setImplementation(newImplementation);
    }
    
    function _setImplementation(address newImplementation) internal {
        require(
            newImplementation.code.length > 0,
            "Not a contract"
        );
        assembly {
            sstore(IMPLEMENTATION_SLOT, newImplementation)
        }
    }
}
```

### **4. Преимущества и недостатки**

1. **Преимущества:**
   ```solidity
   contract ProxyAdvantages {
       // 1. Обновляемость логики
       function upgrade(address newLogic) external {
           // Можно исправлять баги
           // Добавлять новую функциональность
           // Оптимизировать код
       }
       
       // 2. Сохранение состояния
       mapping(address => uint256) public balances;
       // Все данные сохраняются при обновлении
       
       // 3. Постоянный адрес
       address public constant PROXY_ADDRESS = 
           0x1234...;
       // Пользователи всегда взаимодействуют с одним адресом
   }
   ```

2. **Недостатки:**
   ```solidity
   contract ProxyDisadvantages {
       // 1. Сложность разработки
       uint256 public value; // Должен быть в том же слоте во всех версиях
       
       // 2. Риск коллизий storage
       address public owner; // Может конфликтовать с переменными имплементации
       
       // 3. Дополнительные газовые затраты
       function someFunction() external {
           // Каждый вызов требует delegatecall
       }
   }
   ```

### **5. Безопасность**

```solidity
contract SecureProxy {
    // 1. Инициализация
    bool private _initialized;
    
    function initialize() external {
        require(!_initialized, "Already initialized");
        _initialized = true;
        // Инициализация состояния
    }
    
    // 2. Защита от коллизий
    bytes32 private constant COLLISION_HASH = 
        keccak256("proxy.specific.storage");
    
    mapping(bytes32 => uint256) private _proxyStorage;
    
    function _setProxyValue(uint256 value) internal {
        _proxyStorage[COLLISION_HASH] = value;
    }
    
    // 3. Проверки обновлений
    function _authorizeUpgrade(
        address newImplementation
    ) internal view {
        // Проверка совместимости storage
        // Проверка безопасности кода
        // Проверка прав доступа
    }
}
```

### **6. Типы прокси**

1. **Transparent Proxy:**
   ```solidity
   contract TransparentProxy {
       function _delegate(address implementation) internal {
           // Проверяем, не является ли вызывающий админом
           if (msg.sender == _getAdmin()) {
               // Админ может вызывать только админские функции
               require(
                   !_isProxyFunction(msg.sig),
                   "Admin cannot call proxy functions"
               );
           }
           // Делегируем вызов
           _delegateCall(implementation);
       }
   }
   ```

2. **UUPS Proxy:**
   ```solidity
   contract UUPSProxy {
       // Логика обновления находится в имплементации
       function upgradeTo(
           address newImplementation
       ) external {
           // Только имплементация может обновить себя
           require(
               msg.sender == address(this),
               "Only proxy can upgrade"
           );
           _setImplementation(newImplementation);
       }
   }
   ```

---

## Связанные темы
- [[6. Список вопросов]]
- [[Как работает delegatecall?]]
- [[Что такое storage collision?]]
- [[Какие типы proxy вы знаете?]]

---

## Источники
- [EIP-1967: Standard Proxy Storage Slots](https://eips.ethereum.org/EIPS/eip-1967)
- [OpenZeppelin Proxy Documentation](https://docs.openzeppelin.com/upgrades-plugins/1.x/proxies)
- [UUPS vs Transparent Proxy Pattern](https://docs.openzeppelin.com/upgrades-plugins/1.x/proxies#transparent-proxies-and-function-clashes) 