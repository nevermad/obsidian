## Короткий ответ

Beacon - это специальный контракт в proxy паттерне, который хранит адрес имплементации для множества прокси контрактов. Это позволяет обновлять имплементацию сразу для всех прокси через один Beacon контракт, что экономит газ и упрощает управление большим количеством прокси. В отличие от обычного слота implementation, Beacon обеспечивает централизованное управление и атомарное обновление.

---

## Подробный разбор

### **1. Базовая структура**

```solidity
// Интерфейс Beacon
interface IBeacon {
    function implementation() external view returns (address);
}

// Beacon контракт
contract UpgradeableBeacon {
    // Адрес имплементации
    address private _implementation;
    
    // Админ
    address private _owner;
    
    // События
    event Upgraded(address indexed implementation);
    
    constructor(address implementation_) {
        _owner = msg.sender;
        _setImplementation(implementation_);
    }
    
    // Получение адреса имплементации
    function implementation() public view returns (address) {
        return _implementation;
    }
    
    // Обновление имплементации
    function upgradeTo(address newImplementation) public {
        require(msg.sender == _owner, "Not owner");
        _setImplementation(newImplementation);
    }
    
    function _setImplementation(address newImplementation) private {
        require(
            newImplementation.code.length > 0,
            "Not a contract"
        );
        _implementation = newImplementation;
        emit Upgraded(newImplementation);
    }
}
```

### **2. Beacon Proxy**

```solidity
contract BeaconProxy {
    // Слот для адреса Beacon
    bytes32 private constant BEACON_SLOT = 
        keccak256("eip1967.proxy.beacon");
    
    constructor(address beacon) {
        _setBeacon(beacon);
    }
    
    // Получение адреса имплементации через Beacon
    function _implementation() internal view returns (address) {
        return IBeacon(_getBeacon()).implementation();
    }
    
    // Получение адреса Beacon
    function _getBeacon() internal view returns (address) {
        bytes32 slot = BEACON_SLOT;
        address beacon;
        assembly {
            beacon := sload(slot)
        }
        return beacon;
    }
    
    // Установка адреса Beacon
    function _setBeacon(address beacon) internal {
        require(
            beacon.code.length > 0,
            "Not a contract"
        );
        bytes32 slot = BEACON_SLOT;
        assembly {
            sstore(slot, beacon)
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

### **3. Преимущества Beacon**

```solidity
contract BeaconAdvantages {
    /*
    1. Централизованное управление:
       - Один источник правды для имплементации
       - Атомарное обновление всех прокси
       - Упрощенное управление версиями
    
    2. Экономия газа:
       - Меньше storage операций при деплое
       - Общие затраты на обновление ниже
       - Оптимизация при массовом деплое
    
    3. Безопасность:
       - Единая точка контроля
       - Проще аудит
       - Меньше возможностей для ошибок
    */
}
```

### **4. Фабрика Beacon Proxy**

```solidity
contract BeaconProxyFactory {
    // Адрес Beacon
    address public immutable beacon;
    
    constructor(address _beacon) {
        beacon = _beacon;
    }
    
    // Создание нового прокси
    function createProxy(
        bytes memory initData
    ) external returns (address) {
        // Деплоим новый прокси
        BeaconProxy proxy = new BeaconProxy(beacon);
        
        // Инициализируем если нужно
        if (initData.length > 0) {
            (bool success,) = address(proxy).call(initData);
            require(success, "Initialization failed");
        }
        
        return address(proxy);
    }
    
    // Массовое создание прокси
    function createProxies(
        uint256 count,
        bytes memory initData
    ) external returns (address[] memory) {
        address[] memory proxies = new address[](count);
        
        for (uint256 i = 0; i < count; i++) {
            proxies[i] = address(new BeaconProxy(beacon));
            
            if (initData.length > 0) {
                (bool success,) = proxies[i].call(initData);
                require(success, "Initialization failed");
            }
        }
        
        return proxies;
    }
}
```

### **5. Безопасное обновление**

```solidity
contract SafeBeacon {
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
    ) external onlyOwner {
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
    function executeUpgrade() external onlyOwner {
        require(
            block.timestamp >= 
                currentProposal.timestamp + UPGRADE_DELAY,
            "Timelock active"
        );
        
        require(!currentProposal.executed, "Already executed");
        
        _setImplementation(currentProposal.implementation);
        currentProposal.executed = true;
    }
}
```

### **6. Мониторинг и управление**

```solidity
contract BeaconMonitor {
    // Отслеживание прокси
    mapping(address => bool) public isProxy;
    address[] public allProxies;
    
    // Регистрация прокси
    function registerProxy(address proxy) external {
        require(!isProxy[proxy], "Already registered");
        
        isProxy[proxy] = true;
        allProxies.push(proxy);
    }
    
    // Проверка версий
    function checkVersions() external view returns (bool) {
        address implementation = 
            IBeacon(beacon).implementation();
            
        for (uint i = 0; i < allProxies.length; i++) {
            address proxyImpl = 
                IBeaconProxy(allProxies[i])
                    .implementation();
                    
            if (proxyImpl != implementation) {
                return false;
            }
        }
        
        return true;
    }
}
```

### **7. Примеры использования**

```solidity
// Пример NFT с Beacon Proxy
contract NFTBeacon {
    // Beacon для коллекций
    address public immutable collectionBeacon;
    
    // Фабрика коллекций
    function createCollection(
        string memory name,
        string memory symbol
    ) external returns (address) {
        // Создаем прокси через Beacon
        BeaconProxy proxy = new BeaconProxy(
            collectionBeacon
        );
        
        // Инициализируем коллекцию
        IERC721(address(proxy)).initialize(
            name,
            symbol,
            msg.sender
        );
        
        return address(proxy);
    }
    
    // Обновление всех коллекций
    function upgradeCollections(
        address newImplementation
    ) external onlyOwner {
        IBeacon(collectionBeacon).upgradeTo(
            newImplementation
        );
    }
}
```

### **8. Сравнение с обычным прокси**

```solidity
contract ProxyComparison {
    /*
    Обычный Proxy:
    + Простота реализации
    + Независимость обновлений
    + Меньше газа на вызовы
    - Сложное управление множеством прокси
    - Больше газа на массовые обновления
    
    Beacon Proxy:
    + Централизованное управление
    + Атомарные обновления
    + Экономия на массовых операциях
    - Дополнительный вызов для implementation
    - Единая точка отказа
    */
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
- [OpenZeppelin: Beacon Proxies](https://docs.openzeppelin.com/contracts/4.x/api/proxy#beacon)
- [OpenZeppelin: Writing Upgradeable Contracts](https://docs.openzeppelin.com/upgrades-plugins/1.x/writing-upgradeable) 