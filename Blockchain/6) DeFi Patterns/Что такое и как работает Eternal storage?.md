## Короткий ответ

Eternal storage - это паттерн хранения данных в смарт-контрактах, где все переменные состояния хранятся в маппингах по типам данных, а не в обычных переменных. Это позволяет избежать проблем с layout storage при обновлении контрактов и делает хранилище более гибким и расширяемым.

---

## Подробный разбор

### **1. Базовая структура**

```solidity
contract EternalStorage {
    // Маппинги для каждого типа данных
    mapping(bytes32 => uint256) private uintStorage;
    mapping(bytes32 => string) private stringStorage;
    mapping(bytes32 => address) private addressStorage;
    mapping(bytes32 => bytes) private bytesStorage;
    mapping(bytes32 => bool) private boolStorage;
    mapping(bytes32 => int256) private intStorage;
    
    // Маппинги для массивов
    mapping(bytes32 => bytes32[]) private bytes32ArrayStorage;
    mapping(bytes32 => uint256[]) private uintArrayStorage;
    mapping(bytes32 => address[]) private addressArrayStorage;
}
```

### **2. Доступ к данным**

```solidity
contract EternalStorageAccess {
    // Геттеры
    function getUint(bytes32 key) public view returns (uint256) {
        return uintStorage[key];
    }
    
    function getString(bytes32 key) public view returns (string memory) {
        return stringStorage[key];
    }
    
    function getAddress(bytes32 key) public view returns (address) {
        return addressStorage[key];
    }
    
    // Сеттеры
    function setUint(bytes32 key, uint256 value) public {
        uintStorage[key] = value;
    }
    
    function setString(bytes32 key, string memory value) public {
        stringStorage[key] = value;
    }
    
    function setAddress(bytes32 key, address value) public {
        addressStorage[key] = value;
    }
}
```

### **3. Генерация ключей**

```solidity
contract StorageKeys {
    // Генерация ключей для переменных
    bytes32 private constant TOTAL_SUPPLY = 
        keccak256("token.totalSupply");
    bytes32 private constant OWNER = 
        keccak256("access.owner");
    bytes32 private constant PAUSED = 
        keccak256("state.paused");
        
    // Генерация ключей для маппингов
    function balanceKey(
        address account
    ) private pure returns (bytes32) {
        return keccak256(
            abi.encodePacked("token.balance", account)
        );
    }
    
    function allowanceKey(
        address owner,
        address spender
    ) private pure returns (bytes32) {
        return keccak256(
            abi.encodePacked(
                "token.allowance",
                owner,
                spender
            )
        );
    }
}
```

### **4. Использование в контрактах**

```solidity
// Базовый контракт с хранилищем
contract TokenStorage is EternalStorage {
    // Константы для ключей
    bytes32 private constant TOTAL_SUPPLY = 
        keccak256("token.totalSupply");
        
    function totalSupply() public view returns (uint256) {
        return getUint(TOTAL_SUPPLY);
    }
    
    function balanceOf(
        address account
    ) public view returns (uint256) {
        return getUint(balanceKey(account));
    }
    
    function transfer(
        address to,
        uint256 amount
    ) public returns (bool) {
        address from = msg.sender;
        
        // Уменьшаем баланс отправителя
        setUint(
            balanceKey(from),
            balanceOf(from) - amount
        );
        
        // Увеличиваем баланс получателя
        setUint(
            balanceKey(to),
            balanceOf(to) + amount
        );
        
        return true;
    }
}
```

### **5. Структуры данных**

```solidity
contract ComplexStorage {
    // Структуры через маппинги
    function setStruct(
        bytes32 key,
        uint256 value1,
        address value2,
        bool value3
    ) public {
        bytes32 baseKey = keccak256(
            abi.encodePacked("struct", key)
        );
        
        setUint(
            keccak256(
                abi.encodePacked(baseKey, "value1")
            ),
            value1
        );
        
        setAddress(
            keccak256(
                abi.encodePacked(baseKey, "value2")
            ),
            value2
        );
        
        setBool(
            keccak256(
                abi.encodePacked(baseKey, "value3")
            ),
            value3
        );
    }
    
    // Массивы через маппинги
    function pushToArray(
        bytes32 arrayKey,
        uint256 value
    ) public {
        uint256 length = getUint(
            keccak256(
                abi.encodePacked(arrayKey, "length")
            )
        );
        
        setUint(
            keccak256(
                abi.encodePacked(arrayKey, length)
            ),
            value
        );
        
        setUint(
            keccak256(
                abi.encodePacked(arrayKey, "length")
            ),
            length + 1
        );
    }
}
```

### **6. Преимущества и недостатки**

```solidity
contract StorageComparison {
    // Традиционный подход
    contract Traditional {
        uint256 public value;
        mapping(address => uint256) public balances;
        
        // Проблемы при обновлении:
        // - Фиксированный layout
        // - Сложно добавлять новые переменные
        // - Риск коллизий
    }
    
    // Eternal Storage
    contract Eternal {
        // Преимущества:
        // + Гибкое хранилище
        // + Легко добавлять новые переменные
        // + Нет проблем с layout
        
        // Недостатки:
        // - Больше газа на доступ
        // - Сложнее читать код
        // - Нужно управлять ключами
    }
}
```

### **7. Безопасность**

```solidity
contract SecureStorage {
    // Защита доступа
    mapping(bytes32 => address) private accessControl;
    
    modifier onlyAuthorized(bytes32 key) {
        require(
            accessControl[key] == msg.sender,
            "Not authorized"
        );
        _;
    }
    
    // Безопасные сеттеры
    function setUint(
        bytes32 key,
        uint256 value
    ) public onlyAuthorized(key) {
        uintStorage[key] = value;
    }
    
    // Проверка существования
    function hasKey(bytes32 key) public view returns (bool) {
        return uintStorage[key] != 0 ||
               addressStorage[key] != address(0) ||
               boolStorage[key];
    }
}
```

### **8. Примеры использования**

```solidity
// Пример токена с Eternal Storage
contract EternalToken is EternalStorage {
    // Константы
    bytes32 private constant TOTAL_SUPPLY = 
        keccak256("token.totalSupply");
    bytes32 private constant DECIMALS = 
        keccak256("token.decimals");
    bytes32 private constant SYMBOL = 
        keccak256("token.symbol");
        
    // Инициализация
    function initialize() public {
        require(!getBool(INITIALIZED), "Already initialized");
        
        setUint(DECIMALS, 18);
        setString(SYMBOL, "ETN");
        setAddress(OWNER, msg.sender);
        setBool(INITIALIZED, true);
    }
    
    // Логика токена
    function mint(address to, uint256 amount) public {
        require(
            getAddress(OWNER) == msg.sender,
            "Only owner"
        );
        
        setUint(
            balanceKey(to),
            getUint(balanceKey(to)) + amount
        );
        
        setUint(
            TOTAL_SUPPLY,
            getUint(TOTAL_SUPPLY) + amount
        );
    }
}
```

---

## Связанные темы
- [[6. Список вопросов]]
- [[Расскажите подробно как работает паттерн proxy?]]
- [[Что такое storage collision?]]
- [[Расскажите о Unstructured storage?]]

---

## Источники
- [EIP-1967: Standard Proxy Storage Slots](https://eips.ethereum.org/EIPS/eip-1967)
- [OpenZeppelin: Writing Upgradeable Contracts](https://docs.openzeppelin.com/upgrades-plugins/1.x/writing-upgradeable)
- [Solidity Storage Layout](https://docs.soliditylang.org/en/latest/internals/layout_in_storage.html)