## Короткий ответ

Rug pull - это тип мошенничества в DeFi, когда разработчики проекта внезапно выводят всю ликвидность из пула или продают большое количество токенов, оставляя инвесторов с обесцененными активами. Известные примеры: AnubisDAO ($60M), Luna Yield ($6.7M), TurtleDex ($2.4M).

---

## Подробный разбор

### **1. Типы rug pull**

```solidity
// 1. Liquidity Removal
contract LiquidityPool {
    // Уязвимый код без таймлока
    function removeLiquidity() external onlyOwner {
        // Владелец может вывести всю ликвидность
        token.transfer(owner, token.balanceOf(address(this)));
    }
}

// 2. Sell Pressure
contract Token {
    // Скрытые привилегии минтинга
    function mint(address to, uint256 amount) external {
        require(msg.sender == owner, "Not owner");
        _mint(to, amount);
    }
}

// 3. Backdoor
contract BackdoorExample {
    // Скрытая функция для кражи средств
    function _callback(bytes memory data) internal {
        if (data.length > 0 && owner == msg.sender) {
            address target = abi.decode(data, (address));
            IERC20(target).transfer(
                owner,
                IERC20(target).balanceOf(address(this))
            );
        }
    }
}
```

### **2. Механизмы реализации**

```solidity
contract RugPullMechanisms {
    // 1. Неограниченный минтинг
    function hiddenMint() external {
        require(msg.sender == owner);
        _mint(owner, 1000000 * 10**18);
    }
    
    // 2. Скрытые комиссии
    function transfer(
        address to,
        uint256 amount
    ) external returns (bool) {
        // Скрытая комиссия 99%
        uint256 fee = amount * 99 / 100;
        amount = amount - fee;
        _transfer(msg.sender, owner, fee);
        _transfer(msg.sender, to, amount);
        return true;
    }
    
    // 3. Блокировка продаж
    mapping(address => bool) public blacklisted;
    
    function sell(uint256 amount) external {
        require(!blacklisted[msg.sender], "Blacklisted");
        // Владелец может добавить в черный список
        // когда захочет продать свои токены
    }
}
```

### **3. Реальные примеры**

```solidity
// AnubisDAO (Октябрь 2021)
contract AnubisDAOExample {
    // Уязвимый код с неограниченными правами
    function initialize() external {
        require(!initialized, "Already initialized");
        initialized = true;
        
        // Владелец получает полный контроль
        _setupRole(DEFAULT_ADMIN_ROLE, msg.sender);
        _setupRole(MINTER_ROLE, msg.sender);
        _setupRole(BURNER_ROLE, msg.sender);
    }
    
    // Функция для вывода средств
    function withdrawAll() external {
        require(hasRole(DEFAULT_ADMIN_ROLE, msg.sender));
        uint256 balance = address(this).balance;
        payable(msg.sender).transfer(balance);
    }
}

// Luna Yield (Август 2021)
contract LunaYieldExample {
    // Код с скрытой возможностью вывода
    function migrate() external onlyOwner {
        // Функция "миграции" использовалась
        // для вывода всех средств
        token.transfer(
            owner,
            token.balanceOf(address(this))
        );
    }
}
```

### **4. Защитные механизмы**

```solidity
contract RugPullProtection {
    // 1. Timelock для критических операций
    uint256 public constant TIMELOCK = 2 days;
    mapping(bytes32 => uint256) public pendingOperations;
    
    function proposeLiquidityRemoval() external onlyOwner {
        bytes32 opId = keccak256("removeLiquidity");
        pendingOperations[opId] = block.timestamp + TIMELOCK;
    }
    
    function executeLiquidityRemoval() external onlyOwner {
        bytes32 opId = keccak256("removeLiquidity");
        require(
            block.timestamp >= pendingOperations[opId],
            "Timelock active"
        );
        // Выполнение операции
    }
    
    // 2. Ограничения на минтинг
    uint256 public constant MAX_SUPPLY = 1000000 * 10**18;
    
    function mint(address to, uint256 amount) external {
        require(
            totalSupply + amount <= MAX_SUPPLY,
            "Exceeds max supply"
        );
        _mint(to, amount);
    }
    
    // 3. Постепенная разблокировка токенов
    struct VestingSchedule {
        uint256 total;
        uint256 released;
        uint256 start;
        uint256 duration;
    }
    
    mapping(address => VestingSchedule) public vesting;
    
    function release() external {
        VestingSchedule storage schedule = vesting[msg.sender];
        uint256 releasable = _calculateReleasable(schedule);
        schedule.released += releasable;
        _transfer(address(this), msg.sender, releasable);
    }
}
```

### **5. Признаки потенциального rug pull**

```solidity
contract RedFlags {
    // 1. Отсутствие ограничений на минтинг
    function mint(uint256 amount) external onlyOwner {
        _mint(msg.sender, amount);
    }
    
    // 2. Возможность изменения критических параметров
    function setFee(uint256 newFee) external onlyOwner {
        // Владелец может установить комиссию 100%
        transferFee = newFee;
    }
    
    // 3. Отсутствие таймлока
    function emergencyWithdraw() external onlyOwner {
        // Мгновенный вывод всех средств
        token.transfer(owner, token.balanceOf(address(this)));
    }
    
    // 4. Скрытые привилегированные функции
    function _beforeTokenTransfer(
        address from,
        address to,
        uint256 amount
    ) internal override {
        // Скрытая возможность блокировки транзакций
        if (blacklisted[from] || blacklisted[to]) {
            revert("Blocked");
        }
    }
}
```

### **6. Лучшие практики безопасности**

```solidity
contract SecurityBestPractices {
    // 1. Многоподписный контроль
    address[] public signers;
    uint256 public constant MIN_SIGNATURES = 3;
    
    mapping(bytes32 => uint256) public signatures;
    
    function proposeOperation(
        bytes32 operation
    ) external {
        require(isSigner[msg.sender], "Not signer");
        signatures[operation]++;
        
        if (signatures[operation] >= MIN_SIGNATURES) {
            _executeOperation(operation);
        }
    }
    
    // 2. Постепенный вывод ликвидности
    uint256 public constant MAX_WITHDRAWAL_PERCENT = 10;
    uint256 public lastWithdrawalTime;
    uint256 public constant WITHDRAWAL_DELAY = 7 days;
    
    function withdrawLiquidity(
        uint256 amount
    ) external onlyOwner {
        require(
            block.timestamp >= lastWithdrawalTime + WITHDRAWAL_DELAY,
            "Too soon"
        );
        
        uint256 maxAmount = totalLiquidity() * MAX_WITHDRAWAL_PERCENT / 100;
        require(amount <= maxAmount, "Amount too high");
        
        lastWithdrawalTime = block.timestamp;
        _withdraw(amount);
    }
}
```

---

## Связанные темы
- [[6. Список вопросов]]
- [[Что такое и для чего необходим Governance Token?]]
- [[Что такое и как работает Multisig?]]
- [[Расскажите о работе role-based AccessControl OpenZeppelin]]

---

## Источники
- [DeFi Rug Pulls: What They Are and How to Avoid Them](https://academy.binance.com/en/articles/what-is-a-rug-pull-in-crypto-and-how-to-identify-it)
- [CertiK's Analysis of Major Rug Pulls](https://www.certik.com/resources/blog/FnfYrOJ1WB-top-10-defi-rug-pulls-2021)
- [Rekt.news Database of DeFi Hacks](https://rekt.news/) 