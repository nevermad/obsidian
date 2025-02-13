## Короткий ответ

TWAP (Time-Weighted Average Price) оракул - это механизм расчета средневзвешенной по времени цены актива. Он накапливает исторические цены и использует их для вычисления среднего значения за определенный период. Наиболее известная реализация - Uniswap V3 TWAP, которая использует накопление тиков для точного расчета средней цены.

---

## Подробный разбор

### **1. Принцип работы**

```solidity
contract TWAPOracle {
    struct Observation {
        uint32 timestamp;
        uint256 price;
        uint256 liquidityWeight;
    }
    
    // Хранение наблюдений
    Observation[] public observations;
    uint256 public constant MAX_OBSERVATIONS = 5760; // ~24 часа при 15с блоках
    
    // Добавление наблюдения
    function recordObservation(
        uint256 price,
        uint256 liquidity
    ) external {
        if (observations.length == MAX_OBSERVATIONS) {
            // Сдвигаем массив
            for (uint256 i = 0; i < observations.length - 1;) {
                observations[i] = observations[i + 1];
                unchecked { i++; }
            }
            observations[observations.length - 1] = Observation({
                timestamp: uint32(block.timestamp),
                price: price,
                liquidityWeight: liquidity
            });
        } else {
            observations.push(Observation({
                timestamp: uint32(block.timestamp),
                price: price,
                liquidityWeight: liquidity
            }));
        }
    }
}
```

### **2. Расчет TWAP**

```solidity
contract TWAPCalculator {
    using SafeMath for uint256;
    
    // Расчет TWAP за период
    function calculateTWAP(
        uint256 period
    ) external view returns (uint256) {
        require(period > 0, "Invalid period");
        uint256 startTime = block.timestamp - period;
        
        uint256 weightedSum = 0;
        uint256 totalWeight = 0;
        
        for (uint256 i = 0; i < observations.length;) {
            Observation memory current = observations[i];
            
            if (current.timestamp >= startTime) {
                uint256 duration;
                
                if (i == observations.length - 1) {
                    duration = block.timestamp - current.timestamp;
                } else {
                    duration = observations[i + 1].timestamp - current.timestamp;
                }
                
                weightedSum = weightedSum.add(
                    current.price.mul(duration).mul(current.liquidityWeight)
                );
                totalWeight = totalWeight.add(
                    duration.mul(current.liquidityWeight)
                );
            }
            
            unchecked { i++; }
        }
        
        require(totalWeight > 0, "No observations in period");
        return weightedSum.div(totalWeight);
    }
}
```

### **3. Uniswap V3 реализация**

```solidity
interface IUniswapV3Pool {
    function slot0() external view returns (
        uint160 sqrtPriceX96,
        int24 tick,
        uint16 observationIndex,
        uint16 observationCardinality,
        uint16 observationCardinalityNext,
        uint8 feeProtocol,
        bool unlocked
    );
    
    function observations(uint256 index) external view returns (
        uint32 blockTimestamp,
        int56 tickCumulative,
        uint160 secondsPerLiquidityCumulativeX128,
        bool initialized
    );
}

contract UniswapV3TWAPOracle {
    IUniswapV3Pool public immutable pool;
    
    constructor(address _pool) {
        pool = IUniswapV3Pool(_pool);
    }
    
    // Получение текущего тика
    function getCurrentTick() public view returns (int24) {
        (
            ,
            int24 tick,
            ,
            ,
            ,
            ,
            
        ) = pool.slot0();
        return tick;
    }
    
    // Расчет TWAP по тикам
    function calculateTWAPFromTicks(
        int56 startTickCumulative,
        int56 endTickCumulative,
        uint32 timeElapsed
    ) public pure returns (uint256) {
        require(timeElapsed > 0, "Time elapsed must be > 0");
        
        int56 tickCumulativeDelta = endTickCumulative - startTickCumulative;
        int24 timeWeightedAverageTick = int24(
            tickCumulativeDelta / int56(uint56(timeElapsed))
        );
        
        return _tickToPrice(timeWeightedAverageTick);
    }
}
```

### **4. Защита от манипуляций**

```solidity
contract TWAPSecurity {
    uint256 public constant MAX_PRICE_CHANGE = 10; // 10%
    uint256 public constant MIN_PERIOD = 30 minutes;
    uint256 public constant MAX_PERIOD = 24 hours;
    
    // Проверка валидности TWAP
    function validateTWAP(
        uint256 twapPrice,
        uint256 spotPrice,
        uint256 period
    ) external pure returns (bool) {
        require(
            period >= MIN_PERIOD && period <= MAX_PERIOD,
            "Invalid period"
        );
        
        // Проверка отклонения от спот цены
        uint256 deviation = _calculateDeviation(twapPrice, spotPrice);
        if (deviation > MAX_PRICE_CHANGE) {
            return false;
        }
        
        return true;
    }
    
    // Расчет безопасного TWAP
    function getSafeTWAP(
        uint256[] memory periods
    ) external view returns (uint256) {
        require(periods.length > 0, "No periods");
        
        uint256[] memory prices = new uint256[](periods.length);
        
        // Получение TWAP для разных периодов
        for (uint256 i = 0; i < periods.length;) {
            prices[i] = calculateTWAP(periods[i]);
            unchecked { i++; }
        }
        
        // Медианное значение как наиболее надежное
        return _calculateMedian(prices);
    }
}
```

### **5. Интеграция в DeFi протоколы**

```solidity
contract TWAPIntegration {
    ITWAPOracle public twapOracle;
    uint256 public constant TWAP_PERIOD = 1 hours;
    
    // Использование TWAP в lending протоколе
    function calculateCollateralValue(
        address token,
        uint256 amount
    ) external view returns (uint256) {
        // Получение TWAP цены
        uint256 twapPrice = twapOracle.calculateTWAP(TWAP_PERIOD);
        
        // Получение спот цены
        uint256 spotPrice = _getSpotPrice(token);
        
        // Использование минимальной цены для безопасности
        uint256 price = twapPrice < spotPrice ? twapPrice : spotPrice;
        
        return amount * price / 1e18;
    }
    
    // Использование TWAP для ликвидаций
    function checkLiquidation(
        address account
    ) external view returns (bool) {
        uint256 collateralValue = calculateCollateralValue(
            getCollateralToken(account),
            getCollateralAmount(account)
        );
        
        uint256 debtValue = calculateDebtValue(account);
        
        // Проверка здоровья позиции
        return collateralValue * 100 < debtValue * requiredCollateralRatio;
    }
}
```

### **6. Оптимизации и улучшения**

```solidity
contract OptimizedTWAP {
    using SafeMath for uint256;
    
    struct CompressedObservation {
        uint32 timestamp;
        uint224 price; // Сжатая цена
    }
    
    CompressedObservation[] public compressedObservations;
    
    // Оптимизированное хранение
    function addCompressedObservation(uint256 price) external {
        require(price < 2**224, "Price too high");
        
        compressedObservations.push(CompressedObservation({
            timestamp: uint32(block.timestamp),
            price: uint224(price)
        }));
    }
    
    // Кэширование результатов
    mapping(uint256 => uint256) public cachedTWAP;
    mapping(uint256 => uint256) public cacheTimestamp;
    uint256 public constant CACHE_DURATION = 5 minutes;
    
    // Получение TWAP с кэшированием
    function getCachedTWAP(
        uint256 period
    ) external view returns (uint256) {
        uint256 cached = cachedTWAP[period];
        uint256 lastUpdate = cacheTimestamp[period];
        
        if (
            cached > 0 &&
            block.timestamp - lastUpdate <= CACHE_DURATION
        ) {
            return cached;
        }
        
        uint256 newTWAP = calculateTWAP(period);
        cachedTWAP[period] = newTWAP;
        cacheTimestamp[period] = block.timestamp;
        
        return newTWAP;
    }
}
```

---

## Связанные темы
- [[6. Список вопросов]]
- [[Расскажите как работают on-chain оракулы цены]]
- [[Расскажите об атаке манипуляции ценой оракула]]
- [[Что такое Oracle?]]

---

## Источники
- [Uniswap V3 TWAP Documentation](https://docs.uniswap.org/protocol/concepts/V3-overview/oracle)
- [TWAP Oracle Design](https://blog.chain.link/twap-oracles-fair-prices/)
- [DeFi Security: Price Oracle Manipulation](https://consensys.github.io/smart-contract-best-practices/attacks/price-oracle-manipulation/) 