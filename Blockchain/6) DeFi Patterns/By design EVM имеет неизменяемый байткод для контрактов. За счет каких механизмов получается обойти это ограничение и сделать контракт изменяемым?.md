## Короткий ответ

Несмотря на неизменяемость байткода в EVM, существует несколько паттернов для создания обновляемых контрактов: proxy паттерн (delegatecall), beacon прокси, diamond паттерн (EIP-2535), и eternal storage. Основной механизм - разделение логики и данных между разными контрактами, где прокси контракт хранит состояние и делегирует выполнение логики в изменяемую имплементацию.

---

## Подробный разбор

### **1. Proxy паттерн**

```solidity
contract Proxy {
    // Слот для адреса имплементации
    bytes32 private constant IMPLEMENTATION_SLOT = 
        bytes32(uint256(keccak256("eip1967.proxy.implementation")) - 1);
    
    // Делегирование всех вызовов
    fallback() external payable {
        address implementation = _getImplementation();
        
        assembly {
            // Копируем calldata
            calldatacopy(0, 0, calldatasize())
            
            // Делегируем выполнение
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
    
    // Обновление имплементации
    function upgradeTo(address newImplementation) external {
        _setImplementation(newImplementation);
    }
}
```

### **2. Beacon прокси**

```solidity
contract UpgradeableBeacon {
    address private _implementation;
    address private _owner;
    
    event Upgraded(address indexed implementation);
    
    constructor(address implementation_) {
        _owner = msg.sender;
        _setImplementation(implementation_);
    }
    
    function implementation() public view returns (address) {
        return _implementation;
    }
    
    function upgradeTo(address newImplementation) external {
        require(msg.sender == _owner, "Not owner");
        _setImplementation(newImplementation);
    }
}

contract BeaconProxy {
    // Слот для адреса beacon
    bytes32 private constant BEACON_SLOT =
        bytes32(uint256(keccak256("eip1967.proxy.beacon")) - 1);
    
    constructor(address beacon) {
        _setBeacon(beacon);
    }
    
    fallback() external payable {
        _fallback();
    }
    
    function _fallback() internal {
        address beacon = _getBeacon();
        address implementation = IBeacon(beacon).implementation();
        
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

### **3. Diamond паттерн**

```solidity
contract Diamond {
    // Маппинг функций к имплементациям
    mapping(bytes4 => address) private _selectorToFacet;
    
    // Добавление новой фасетки
    function addFacet(
        address facet,
        bytes4[] memory selectors
    ) external {
        for (uint256 i = 0; i < selectors.length;) {
            _selectorToFacet[selectors[i]] = facet;
            unchecked { i++; }
        }
    }
    
    // Удаление фасетки
    function removeFacet(bytes4[] memory selectors) external {
        for (uint256 i = 0; i < selectors.length;) {
            delete _selectorToFacet[selectors[i]];
            unchecked { i++; }
        }
    }
    
    fallback() external payable {
        address facet = _selectorToFacet[msg.sig];
        require(facet != address(0), "Function not found");
        
        assembly {
            calldatacopy(0, 0, calldatasize())
            let result := delegatecall(
                gas(),
                facet,
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

### **4. Eternal Storage**

```solidity
contract EternalStorage {
    mapping(bytes32 => uint256) private _uintStorage;
    mapping(bytes32 => string) private _stringStorage;
    mapping(bytes32 => address) private _addressStorage;
    mapping(bytes32 => bytes) private _bytesStorage;
    mapping(bytes32 => bool) private _boolStorage;
    mapping(bytes32 => int256) private _intStorage;
    
    // Логика хранится в отдельном контракте
    address public logic;
    
    function setLogic(address _logic) external {
        logic = _logic;
    }
    
    fallback() external payable {
        address _logic = logic;
        require(_logic != address(0));
        
        assembly {
            calldatacopy(0, 0, calldatasize())
            let result := delegatecall(
                gas(),
                _logic,
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
contract SafeUpgrade {
    // Таймлок для обновлений
    uint256 public constant UPGRADE_TIMELOCK = 2 days;
    mapping(address => uint256) public upgradeProposals;
    
    // Предложение обновления
    function proposeUpgrade(
        address newImplementation
    ) external {
        upgradeProposals[newImplementation] = block.timestamp + UPGRADE_TIMELOCK;
        emit UpgradeProposed(newImplementation);
    }
    
    // Выполнение обновления
    function executeUpgrade(
        address newImplementation
    ) external {
        require(
            block.timestamp >= upgradeProposals[newImplementation],
            "Timelock active"
        );
        require(
            _validateImplementation(newImplementation),
            "Invalid implementation"
        );
        
        _setImplementation(newImplementation);
    }
    
    // Проверка совместимости storage
    function _validateImplementation(
        address newImplementation
    ) internal view returns (bool) {
        // Проверка интерфейса
        try IUpgradeable(newImplementation).supportsInterface(
            type(IUpgradeable).interfaceId
        ) returns (bool support) {
            if (!support) return false;
        } catch {
            return false;
        }
        
        // Проверка storage layout
        bytes32 oldHash = _getStorageHash(_getImplementation());
        bytes32 newHash = _getStorageHash(newImplementation);
        
        return oldHash == newHash;
    }
}
```

### **6. Примеры использования**

```solidity
// 1. Обновляемый токен
contract UpgradeableToken {
    // Прокси делегирует вызовы в имплементацию
    function transfer(
        address to,
        uint256 amount
    ) external returns (bool) {
        address impl = _getImplementation();
        
        (bool success, bytes memory result) = impl.delegatecall(
            abi.encodeWithSelector(
                IERC20.transfer.selector,
                to,
                amount
            )
        );
        
        require(success, "Transfer failed");
        return abi.decode(result, (bool));
    }
}

// 2. Обновляемый DEX
contract UpgradeableDEX {
    // Beacon прокси для всех пар
    address public immutable beacon;
    mapping(address => mapping(address => address)) public pairs;
    
    function createPair(
        address tokenA,
        address tokenB
    ) external returns (address pair) {
        pair = address(new BeaconProxy(beacon));
        pairs[tokenA][tokenB] = pair;
        pairs[tokenB][tokenA] = pair;
    }
}
```

---

## Связанные темы
- [[6. Список вопросов]]
- [[Расскажите подробно как работает паттерн proxy?]]
- [[Что такое Beacon?]]
- [[Что такое и как работает Eternal storage?]]

---

## Источники
- [EIP-1967: Standard Proxy Storage Slots](https://eips.ethereum.org/EIPS/eip-1967)
- [EIP-2535: Diamond Standard](https://eips.ethereum.org/EIPS/eip-2535)
- [OpenZeppelin: Proxy Upgrade Pattern](https://docs.openzeppelin.com/upgrades-plugins/1.x/proxies) 