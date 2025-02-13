## Короткий ответ

On-chain оракулы цены - это смарт-контракты, которые предоставляют информацию о ценах активов, используя данные непосредственно из блокчейна. Основные типы: AMM-based (например, Uniswap TWAP), агрегаторы DEX цен, и бандлеры ликвидности. Они не требуют внешних данных, но могут быть подвержены манипуляциям через флэш-кредиты.

---

## Подробный разбор

### **1. TWAP оракул Uniswap**

```solidity
interface IUniswapV3Pool {
    function observe(
        uint32[] calldata secondsAgos
    ) external view returns (
        int56[] memory tickCumulatives,
        uint160[] memory secondsPerLiquidityCumulativeX128s
    );
}

contract UniswapV3TWAPOracle {
    IUniswapV3Pool public immutable pool;
    
    constructor(address _pool) {
        pool = IUniswapV3Pool(_pool);
    }
    
    // Получение TWAP цены
    function getTWAP(
        uint32 period
    ) external view returns (uint256 price) {
        require(period > 0, "Invalid period");
        
        uint32[] memory secondsAgos = new uint32[](2);
        secondsAgos[0] = period;
        secondsAgos[1] = 0;
        
        (
            int56[] memory tickCumulatives,
            
        ) = pool.observe(secondsAgos);
        
        int56 tickCumulativesDelta = tickCumulatives[1] - tickCumulatives[0];
        int24 timeWeightedAverageTick = int24(
            tickCumulativesDelta / period
        );
        
        // Конвертация тика в цену
        price = _tickToPrice(timeWeightedAverageTick);
    }
}
```

### **2. Агрегатор DEX цен**

```solidity
contract DEXPriceAggregator {
    struct DEXPrice {
        address dex;
        uint256 price;
        uint256 liquidity;
    }
    
    // Список поддерживаемых DEX
    mapping(address => bool) public supportedDEXes;
    uint256 public constant MIN_LIQUIDITY = 1000 ether;
    
    // Получение агрегированной цены
    function getAggregatedPrice(
        address token
    ) external view returns (uint256) {
        DEXPrice[] memory prices = new DEXPrice[](
            supportedDEXes.length
        );
        uint256 totalLiquidity = 0;
        
        // Сбор цен со всех DEX
        for (uint256 i = 0; i < supportedDEXes.length;) {
            address dex = supportedDEXes[i];
            (uint256 price, uint256 liquidity) = _getDEXPrice(
                dex,
                token
            );
            
            if (liquidity >= MIN_LIQUIDITY) {
                prices[i] = DEXPrice({
                    dex: dex,
                    price: price,
                    liquidity: liquidity
                });
                totalLiquidity += liquidity;
            }
            
            unchecked { i++; }
        }
        
        // Вычисление средневзвешенной цены
        return _calculateWeightedPrice(prices, totalLiquidity);
    }
}
```

### **3. Бандлер ликвидности**

```solidity
contract LiquidityBundler {
    struct LiquidityPool {
        address token0;
        address token1;
        uint256 reserve0;
        uint256 reserve1;
        uint256 weight;
    }
    
    mapping(bytes32 => LiquidityPool[]) public pools;
    
    // Добавление пула ликвидности
    function addPool(
        address token0,
        address token1,
        uint256 weight
    ) external {
        bytes32 pairHash = _getPairHash(token0, token1);
        
        pools[pairHash].push(LiquidityPool({
            token0: token0,
            token1: token1,
            reserve0: 0,
            reserve1: 0,
            weight: weight
        }));
    }
    
    // Обновление резервов
    function updateReserves(
        address token0,
        address token1,
        uint256 reserve0,
        uint256 reserve1
    ) external {
        bytes32 pairHash = _getPairHash(token0, token1);
        LiquidityPool[] storage poolList = pools[pairHash];
        
        for (uint256 i = 0; i < poolList.length;) {
            if (
                poolList[i].token0 == token0 &&
                poolList[i].token1 == token1
            ) {
                poolList[i].reserve0 = reserve0;
                poolList[i].reserve1 = reserve1;
                break;
            }
            unchecked { i++; }
        }
    }
    
    // Получение цены с учетом всех пулов
    function getBundledPrice(
        address tokenIn,
        address tokenOut
    ) external view returns (uint256) {
        bytes32 pairHash = _getPairHash(tokenIn, tokenOut);
        LiquidityPool[] memory poolList = pools[pairHash];
        
        uint256 totalWeight = 0;
        uint256 weightedPrice = 0;
        
        for (uint256 i = 0; i < poolList.length;) {
            if (poolList[i].reserve0 > 0 && poolList[i].reserve1 > 0) {
                uint256 price = _calculatePrice(
                    poolList[i].reserve0,
                    poolList[i].reserve1
                );
                
                weightedPrice += price * poolList[i].weight;
                totalWeight += poolList[i].weight;
            }
            unchecked { i++; }
        }
        
        require(totalWeight > 0, "No valid pools");
        return weightedPrice / totalWeight;
    }
}
```

### **4. Защита от манипуляций**

```solidity
contract ManipulationResistantOracle {
    struct PriceObservation {
        uint256 price;
        uint256 timestamp;
        uint256 confidence;
    }
    
    uint256 public constant OBSERVATION_PERIOD = 1 hours;
    uint256 public constant MAX_PRICE_DEVIATION = 10; // 10%
    
    mapping(address => PriceObservation[]) public priceHistory;
    
    // Добавление наблюдения
    function addObservation(
        address token,
        uint256 price
    ) external {
        PriceObservation[] storage history = priceHistory[token];
        
        // Проверка отклонения от исторических данных
        if (history.length > 0) {
            uint256 avgPrice = _calculateHistoricalAverage(
                token,
                OBSERVATION_PERIOD
            );
            
            uint256 deviation = _calculateDeviation(price, avgPrice);
            require(
                deviation <= MAX_PRICE_DEVIATION,
                "Price deviation too high"
            );
        }
        
        // Добавление наблюдения
        history.push(PriceObservation({
            price: price,
            timestamp: block.timestamp,
            confidence: _calculateConfidence(price, token)
        }));
    }
    
    // Получение надежной цены
    function getReliablePrice(
        address token
    ) external view returns (uint256) {
        PriceObservation[] memory history = priceHistory[token];
        require(history.length > 0, "No price data");
        
        // Фильтрация старых наблюдений
        uint256 validObservations = 0;
        uint256 weightedSum = 0;
        uint256 totalConfidence = 0;
        
        for (uint256 i = 0; i < history.length;) {
            if (
                block.timestamp - history[i].timestamp <=
                OBSERVATION_PERIOD
            ) {
                weightedSum += history[i].price * history[i].confidence;
                totalConfidence += history[i].confidence;
                validObservations++;
            }
            unchecked { i++; }
        }
        
        require(validObservations > 0, "No valid observations");
        return weightedSum / totalConfidence;
    }
}
```

### **5. Интеграция с DeFi протоколами**

```solidity
contract DeFiProtocolIntegration {
    IUniswapV3TWAPOracle public twapOracle;
    DEXPriceAggregator public dexAggregator;
    LiquidityBundler public liquidityBundler;
    
    uint256 public constant CONFIDENCE_THRESHOLD = 95; // 95%
    
    // Получение наиболее надежной цены
    function getMostReliablePrice(
        address token
    ) external view returns (uint256) {
        // Получение цен из разных источников
        uint256 twapPrice = twapOracle.getTWAP(1 hours);
        uint256 aggregatedPrice = dexAggregator.getAggregatedPrice(token);
        uint256 bundledPrice = liquidityBundler.getBundledPrice(
            token,
            address(0) // ETH
        );
        
        // Проверка консенсуса
        if (
            _pricesInRange(twapPrice, aggregatedPrice) &&
            _pricesInRange(aggregatedPrice, bundledPrice)
        ) {
            // Все цены согласованы
            return (twapPrice + aggregatedPrice + bundledPrice) / 3;
        }
        
        // Возвращаем TWAP как наиболее надежный
        return twapPrice;
    }
    
    // Проверка диапазона цен
    function _pricesInRange(
        uint256 price1,
        uint256 price2
    ) internal pure returns (bool) {
        uint256 deviation = _calculateDeviation(price1, price2);
        return deviation <= 5; // 5% максимальное отклонение
    }
}
```

---

## Связанные темы
- [[Что такое TWAP оракул?]]
- [[Расскажите об атаке манипуляции ценой оракула]]
- [[Что такое Oracle?]]

---

## Источники
- [Uniswap V3 TWAP Documentation](https://docs.uniswap.org/protocol/concepts/V3-overview/oracle)
- [DeFi Oracle Security](https://blog.chain.link/defi-oracle-security/)
- [Price Oracle Design Patterns](https://ethereum.org/en/developers/docs/oracles/) 