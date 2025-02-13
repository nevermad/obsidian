## Короткий ответ

Oracle (оракул) - это сервис, который позволяет смарт-контрактам получать данные из внешнего мира (off-chain). Оракулы решают проблему изолированности блокчейна, предоставляя доступ к ценам активов, погодным данным, результатам событий и другой внешней информации через доверенные источники.

---

## Подробный разбор

### **1. Базовая архитектура**

```solidity
interface IOracle {
    // Получение данных
    function getData() external view returns (uint256);
    
    // Обновление данных
    function updateData(uint256 newData) external;
    
    // Проверка актуальности
    function lastUpdateTime() external view returns (uint256);
}

contract SimpleOracle is IOracle {
    uint256 private _data;
    uint256 private _lastUpdateTime;
    address private _trustedUpdater;
    
    event DataUpdated(uint256 newData, uint256 timestamp);
    
    modifier onlyTrustedUpdater() {
        require(msg.sender == _trustedUpdater, "Not authorized");
        _;
    }
    
    function getData() external view override returns (uint256) {
        require(block.timestamp - _lastUpdateTime <= 1 hours, "Data stale");
        return _data;
    }
    
    function updateData(uint256 newData) external override onlyTrustedUpdater {
        _data = newData;
        _lastUpdateTime = block.timestamp;
        emit DataUpdated(newData, block.timestamp);
    }
    
    function lastUpdateTime() external view override returns (uint256) {
        return _lastUpdateTime;
    }
}
```

### **2. Типы данных**

1. **Финансовые данные:**
   ```solidity
   interface IPriceOracle {
       // Цены активов
       function getPrice(address token) external view returns (uint256);
       
       // Курсы валют
       function getExchangeRate(
           string calldata fromCurrency,
           string calldata toCurrency
       ) external view returns (uint256);
       
       // Процентные ставки
       function getInterestRate(address market) external view returns (uint256);
   }
   ```

2. **Реальный мир:**
   ```solidity
   interface IRealWorldOracle {
       // Погодные данные
       function getTemperature(string calldata location) external view returns (int256);
       
       // Результаты событий
       function getEventResult(bytes32 eventId) external view returns (bytes memory);
       
       // Случайные числа
       function getRandomNumber(uint256 seed) external returns (uint256);
   }
   ```

### **3. Механизмы обновления**

```solidity
contract UpdateMechanisms {
    // Push: данные отправляются в контракт
    function pushUpdate(uint256 newData) external onlyOracle {
        _updateData(newData);
    }
    
    // Pull: контракт запрашивает данные
    function pullUpdate() external {
        uint256 newData = IExternalOracle(oracleAddress).getData();
        _updateData(newData);
    }
    
    // Гибридный: проверка + обновление
    function checkAndUpdate() external {
        uint256 lastUpdate = _lastUpdateTime;
        if (block.timestamp - lastUpdate > updateInterval) {
            uint256 newData = IExternalOracle(oracleAddress).getData();
            _updateData(newData);
        }
    }
}
```

### **4. Безопасность и валидация**

```solidity
contract SecureOracle {
    struct DataPoint {
        uint256 value;
        uint256 timestamp;
        address source;
    }
    
    DataPoint[] private _history;
    mapping(address => bool) private _trustedSources;
    uint256 private constant MAX_DEVIATION = 10; // 10%
    
    function updateData(uint256 newData) external {
        require(_trustedSources[msg.sender], "Not trusted source");
        
        // Проверка отклонения
        if (_history.length > 0) {
            uint256 lastValue = _history[_history.length - 1].value;
            uint256 deviation = abs(newData, lastValue) * 100 / lastValue;
            require(deviation <= MAX_DEVIATION, "Deviation too high");
        }
        
        // Сохранение истории
        _history.push(DataPoint({
            value: newData,
            timestamp: block.timestamp,
            source: msg.sender
        }));
    }
    
    function getMedianPrice() external view returns (uint256) {
        require(_history.length > 0, "No data");
        
        // Получение медианного значения
        uint256[] memory values = new uint256[](_history.length);
        for (uint256 i = 0; i < _history.length;) {
            values[i] = _history[i].value;
            unchecked { i++; }
        }
        
        return _calculateMedian(values);
    }
}
```

### **5. Примеры использования**

1. **DeFi протокол:**
   ```solidity
   contract LendingProtocol {
       IPriceOracle public oracle;
       
       function calculateCollateralValue(
           address token,
           uint256 amount
       ) public view returns (uint256) {
           uint256 price = oracle.getPrice(token);
           return price * amount / 1e18;
       }
       
       function liquidationCheck(
           address account,
           address debtToken,
           address collateralToken
       ) external view returns (bool) {
           uint256 debtValue = calculateDebtValue(account, debtToken);
           uint256 collateralValue = calculateCollateralValue(
               collateralToken,
               collateralAmount[account]
           );
           
           return collateralValue < debtValue * 150 / 100; // 150% collateral ratio
       }
   }
   ```

2. **Страховой протокол:**
   ```solidity
   contract InsuranceProtocol {
       IRealWorldOracle public oracle;
       
       function processWeatherInsurance(
           string calldata location,
           int256 triggerTemp
       ) external {
           int256 currentTemp = oracle.getTemperature(location);
           
           if (currentTemp > triggerTemp) {
               _processPayout();
           }
       }
   }
   ```

---

## Связанные темы
- [[Почему на блокчейне нельзя получить данные извне?]]
- [[Как оракулы гарантируют надежность предоставляемых данных?]]
- [[Расскажите о Chainlink Price Feed]]

---

## Источники
- [Chainlink Documentation](https://docs.chain.link/)
- [Oracle Security Best Practices](https://blog.chain.link/defi-oracle-security-best-practices/)
- [Understanding Blockchain Oracles](https://ethereum.org/en/developers/docs/oracles/) 