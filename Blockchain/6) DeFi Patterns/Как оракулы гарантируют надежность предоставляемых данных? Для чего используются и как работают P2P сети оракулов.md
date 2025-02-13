## Короткий ответ

Оракулы гарантируют надежность данных через комбинацию механизмов: децентрализацию источников данных, экономические стимулы (стейкинг), криптографическую верификацию, агрегацию данных с отбрасыванием выбросов, и систему репутации узлов. Это создает устойчивую к манипуляциям систему доставки внешних данных в блокчейн.

---

## Подробный разбор

### **1. Децентрализация источников**

```solidity
contract DecentralizedOracle {
    struct DataSource {
        address provider;
        uint256 stake;
        bool isActive;
        uint256 reputation;
    }
    
    mapping(address => DataSource) public dataSources;
    uint256 public minRequiredSources = 3;
    
    function aggregateData(
        uint256[] calldata values,
        address[] calldata sources
    ) external view returns (uint256) {
        require(
            sources.length >= minRequiredSources,
            "Not enough sources"
        );
        
        // Проверка источников
        for (uint256 i = 0; i < sources.length;) {
            require(
                dataSources[sources[i]].isActive,
                "Invalid source"
            );
            unchecked { i++; }
        }
        
        return _calculateMedian(values);
    }
}
```

### **2. Экономические стимулы**

```solidity
contract StakedOracle {
    struct Stake {
        uint256 amount;
        uint256 lockedUntil;
    }
    
    mapping(address => Stake) public stakes;
    uint256 public constant MIN_STAKE = 1000 ether;
    uint256 public constant LOCK_PERIOD = 7 days;
    
    // Стейкинг токенов
    function stake() external payable {
        require(msg.value >= MIN_STAKE, "Insufficient stake");
        stakes[msg.sender] = Stake({
            amount: msg.value,
            lockedUntil: block.timestamp + LOCK_PERIOD
        });
    }
    
    // Слашинг при некорректных данных
    function slash(address provider) external {
        require(msg.sender == owner, "Only owner");
        Stake memory providerStake = stakes[provider];
        require(providerStake.amount > 0, "No stake");
        
        // Штраф 50% стейка
        uint256 penalty = providerStake.amount / 2;
        stakes[provider].amount -= penalty;
        
        // Распределение штрафа
        _distributeSlashedTokens(penalty);
    }
}
```

### **3. Криптографическая верификация**

```solidity
contract VerifiedOracle {
    // Подпись данных
    function verifyData(
        uint256 value,
        uint256 timestamp,
        bytes memory signature
    ) internal view returns (bool) {
        bytes32 message = keccak256(
            abi.encodePacked(value, timestamp)
        );
        
        // Восстановление подписавшего
        address signer = recoverSigner(message, signature);
        return isAuthorizedProvider(signer);
    }
    
    // Множественная верификация
    function verifyMultipleSignatures(
        uint256 value,
        uint256 timestamp,
        bytes[] memory signatures
    ) external view returns (bool) {
        bytes32 message = keccak256(
            abi.encodePacked(value, timestamp)
        );
        
        uint256 validSignatures = 0;
        for (uint256 i = 0; i < signatures.length;) {
            address signer = recoverSigner(message, signatures[i]);
            if (isAuthorizedProvider(signer)) {
                validSignatures++;
            }
            unchecked { i++; }
        }
        
        return validSignatures >= requiredSignatures;
    }
}
```

### **4. Агрегация данных**

```solidity
contract DataAggregator {
    struct Report {
        uint256 value;
        uint256 timestamp;
        address reporter;
    }
    
    Report[] private reports;
    uint256 public constant MAX_DEVIATION = 10; // 10%
    
    function submitReport(uint256 value) external {
        require(isAuthorizedReporter(msg.sender), "Not authorized");
        
        // Проверка на выбросы
        if (reports.length > 0) {
            uint256 median = _calculateMedian(
                _getLastReportValues(10)
            );
            uint256 deviation = abs(value, median) * 100 / median;
            require(deviation <= MAX_DEVIATION, "High deviation");
        }
        
        reports.push(Report({
            value: value,
            timestamp: block.timestamp,
            reporter: msg.sender
        }));
    }
    
    function getAggregatedValue() external view returns (uint256) {
        require(reports.length > 0, "No data");
        
        // Отбрасываем старые отчеты
        uint256[] memory validValues = _getRecentValues(1 hours);
        require(validValues.length > 0, "No recent data");
        
        // Сортировка и отбрасывание крайних значений
        uint256[] memory sortedValues = _sort(validValues);
        uint256 trimCount = sortedValues.length / 4;
        
        // Вычисление среднего без крайних значений
        uint256 sum = 0;
        for (uint256 i = trimCount; i < sortedValues.length - trimCount;) {
            sum += sortedValues[i];
            unchecked { i++; }
        }
        
        return sum / (sortedValues.length - 2 * trimCount);
    }
}
```

### **5. Система репутации**

```solidity
contract ReputationSystem {
    struct Provider {
        uint256 reputation;
        uint256 totalReports;
        uint256 accurateReports;
        uint256 lastUpdateBlock;
    }
    
    mapping(address => Provider) public providers;
    
    // Обновление репутации
    function updateReputation(
        address provider,
        bool wasAccurate
    ) external {
        require(msg.sender == owner, "Only owner");
        
        Provider storage p = providers[provider];
        p.totalReports++;
        
        if (wasAccurate) {
            p.accurateReports++;
            p.reputation = min(p.reputation + 1, 100);
        } else {
            p.reputation = p.reputation > 5 ? p.reputation - 5 : 0;
        }
        
        p.lastUpdateBlock = block.number;
    }
    
    // Проверка надежности провайдера
    function isReliableProvider(
        address provider
    ) external view returns (bool) {
        Provider memory p = providers[provider];
        
        // Минимум 100 отчетов
        if (p.totalReports < 100) return false;
        
        // Точность не менее 95%
        uint256 accuracy = p.accurateReports * 100 / p.totalReports;
        if (accuracy < 95) return false;
        
        // Активность в последних 1000 блоках
        if (block.number - p.lastUpdateBlock > 1000) return false;
        
        return true;
    }
}
```

### **6. Мониторинг и аудит**

```solidity
contract OracleAudit {
    event DataSubmitted(
        address indexed provider,
        uint256 value,
        uint256 timestamp
    );
    
    event AnomalyDetected(
        address indexed provider,
        uint256 value,
        string reason
    );
    
    // Аудит-лог всех обновлений
    function logDataSubmission(
        address provider,
        uint256 value
    ) external {
        emit DataSubmitted(provider, value, block.timestamp);
    }
    
    // Детекция аномалий
    function detectAnomalies(
        uint256[] memory values,
        address[] memory providers
    ) external {
        uint256 median = _calculateMedian(values);
        
        for (uint256 i = 0; i < values.length;) {
            uint256 deviation = abs(values[i], median) * 100 / median;
            
            if (deviation > 20) {
                emit AnomalyDetected(
                    providers[i],
                    values[i],
                    "High deviation from median"
                );
            }
            
            unchecked { i++; }
        }
    }
}
```

---

## Связанные темы
- [[6. Список вопросов]]
- [[Что такое Oracle?]]
- [[Расскажите о Chainlink Price Feed]]
- [[Расскажите об атаке манипуляции ценой оракула]]

---

## Источники
- [Chainlink Data Quality](https://chain.link/education/blockchain-oracles/data-quality)
- [Oracle Security Best Practices](https://blog.chain.link/defi-oracle-security-best-practices/)
- [Secure Data Delivery](https://docs.chain.link/architecture-overview/architecture-decentralized-model) 