## Короткий ответ

При замене implementation в proxy контракте необходимо учитывать следующие ограничения: совместимость storage layout, сохранение интерфейса функций, обратную совместимость событий, инициализацию новой имплементации. Замена ERC721 на ERC20 implementation невозможна из-за несовместимости storage layout и различий в интерфейсах.

---

## Подробный разбор

### **1. Storage Layout совместимость**

```solidity
// Оригинальная ERC721 имплементация
contract ERC721Implementation {
    // Storage layout
    mapping(uint256 => address) private _owners;
    mapping(address => uint256) private _balances;
    mapping(uint256 => address) private _tokenApprovals;
    mapping(address => mapping(address => bool)) private _operatorApprovals;
    
    // Gap для будущих обновлений
    uint256[50] private __gap;
}

// ❌ Несовместимая ERC20 имплементация
contract ERC20Implementation {
    // Другой storage layout
    mapping(address => uint256) private _balances;
    mapping(address => mapping(address => uint256)) private _allowances;
    uint256 private _totalSupply;
    
    // Конфликт storage
    string private _name;
    string private _symbol;
}

// ✅ Совместимая обновленная ERC721 имплементация
contract ERC721V2Implementation is ERC721Implementation {
    // Новые переменные добавляются после gap
    mapping(uint256 => string) private _tokenURIs;
    bool public isPaused;
}
```

### **2. Интерфейс функций**

```solidity
// Оригинальный интерфейс
interface IERC721 {
    function balanceOf(address owner) external view returns (uint256);
    function ownerOf(uint256 tokenId) external view returns (address);
    function transferFrom(address from, address to, uint256 tokenId) external;
    function safeTransferFrom(address from, address to, uint256 tokenId) external;
    function approve(address to, uint256 tokenId) external;
}

// ❌ Несовместимый интерфейс
interface IERC20 {
    function balanceOf(address account) external view returns (uint256);
    function transfer(address to, uint256 amount) external returns (bool);
    function approve(address spender, uint256 amount) external returns (bool);
    function transferFrom(
        address from,
        address to,
        uint256 amount
    ) external returns (bool);
}

// ✅ Совместимое обновление
interface IERC721V2 is IERC721 {
    // Добавление новых функций
    function pause() external;
    function unpause() external;
    // Сохранение старых функций
}
```

### **3. События и их совместимость**

```solidity
contract EventCompatibility {
    // Оригинальные события
    event Transfer(
        address indexed from,
        address indexed to,
        uint256 indexed tokenId
    );
    
    event Approval(
        address indexed owner,
        address indexed approved,
        uint256 indexed tokenId
    );
    
    // ❌ Несовместимые события
    event Transfer(
        address indexed from,
        address indexed to,
        uint256 value
    );
    
    event Approval(
        address indexed owner,
        address indexed spender,
        uint256 value
    );
    
    // ✅ Совместимое обновление
    event Transfer(
        address indexed from,
        address indexed to,
        uint256 indexed tokenId
    );
    
    event Approval(
        address indexed owner,
        address indexed approved,
        uint256 indexed tokenId
    );
    
    // Новые события
    event Paused(address account);
    event Unpaused(address account);
}
```

### **4. Инициализация**

```solidity
contract InitializableImplementation {
    bool private _initialized;
    bool private _initializing;
    
    modifier initializer() {
        require(
            !_initialized && !_initializing,
            "Already initialized"
        );
        
        _initializing = true;
        _;
        _initializing = false;
        _initialized = true;
    }
    
    // Инициализация V1
    function initialize() public initializer {
        _initialized = true;
    }
    
    // ✅ Правильное обновление
    function initializeV2() public {
        require(_initialized, "Not initialized");
        require(!_initializing, "Initializing");
        _initializing = true;
        
        // Дополнительная инициализация
        
        _initializing = false;
    }
}
```

### **5. Проверки совместимости**

```solidity
contract UpgradeValidator {
    // Проверка storage layout
    function validateStorage(
        address oldImpl,
        address newImpl
    ) external view returns (bool) {
        // Получаем слоты storage
        bytes32[] memory oldSlots = _getStorageSlots(oldImpl);
        bytes32[] memory newSlots = _getStorageSlots(newImpl);
        
        // Проверяем совместимость
        for (uint256 i = 0; i < oldSlots.length;) {
            if (oldSlots[i] != newSlots[i]) {
                return false;
            }
            unchecked { i++; }
        }
        
        return true;
    }
    
    // Проверка интерфейса
    function validateInterface(
        address oldImpl,
        address newImpl
    ) external view returns (bool) {
        // Получаем селекторы функций
        bytes4[] memory oldSelectors = _getSelectors(oldImpl);
        bytes4[] memory newSelectors = _getSelectors(newImpl);
        
        // Проверяем наличие всех старых функций
        for (uint256 i = 0; i < oldSelectors.length;) {
            bool found = false;
            for (uint256 j = 0; j < newSelectors.length;) {
                if (oldSelectors[i] == newSelectors[j]) {
                    found = true;
                    break;
                }
                unchecked { j++; }
            }
            if (!found) return false;
            unchecked { i++; }
        }
        
        return true;
    }
}
```

### **6. Безопасное обновление**

```solidity
contract SafeUpgrade {
    // Проверка перед обновлением
    function _validateUpgrade(
        address newImplementation
    ) internal view {
        // 1. Проверка storage
        require(
            _validateStorage(newImplementation),
            "Storage layout mismatch"
        );
        
        // 2. Проверка интерфейса
        require(
            _validateInterface(newImplementation),
            "Interface mismatch"
        );
        
        // 3. Проверка инициализации
        require(
            IInitializable(newImplementation).initialized(),
            "Not initialized"
        );
        
        // 4. Проверка версии
        require(
            _validateVersion(newImplementation),
            "Invalid version"
        );
    }
    
    // Процесс обновления
    function upgradeTo(
        address newImplementation
    ) external {
        // Проверки
        _validateUpgrade(newImplementation);
        
        // Подготовка к обновлению
        _prepareUpgrade(newImplementation);
        
        // Обновление
        _setImplementation(newImplementation);
        
        // Пост-обновление
        _afterUpgrade(newImplementation);
    }
}
```

---

## Связанные темы
- [[Какие ограничения и особенности накладываются на storage proxy контракта?]]
- [[Что такое storage collision?]]
- [[Расскажите о паттерне инициализации смарт-контрактов]]

---

## Источники
- [OpenZeppelin: Writing Upgradeable Contracts](https://docs.openzeppelin.com/upgrades-plugins/1.x/writing-upgradeable)
- [OpenZeppelin: Proxy Upgrade Pattern](https://docs.openzeppelin.com/upgrades-plugins/1.x/proxies)
- [EIP-1967: Standard Proxy Storage Slots](https://eips.ethereum.org/EIPS/eip-1967) 