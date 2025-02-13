## Короткий ответ

Chainlink Price Feed - это децентрализованный оракул цен, который предоставляет надежные данные о ценах криптовалют, фиатных валют, commodities и других активов. Он использует сеть независимых нод-валидаторов, которые агрегируют данные из множества источников и обеспечивают их достоверность через систему стейкинга и репутации.

---

## Подробный разбор

### **1. Архитектура**

```solidity
interface AggregatorV3Interface {
    function decimals() external view returns (uint8);
    function description() external view returns (string memory);
    function version() external view returns (uint256);
    
    function getRoundData(uint80 _roundId) external view returns (
        uint80 roundId,
        int256 answer,
        uint256 startedAt,
        uint256 updatedAt,
        uint80 answeredInRound
    );
    
    function latestRoundData() external view returns (
        uint80 roundId,
        int256 answer,
        uint256 startedAt,
        uint256 updatedAt,
        uint80 answeredInRound
    );
}
```

### **2. Использование в смарт-контрактах**

```solidity
contract PriceFeedConsumer {
    AggregatorV3Interface internal priceFeed;
    
    constructor() {
        // ETH/USD Price Feed на Mainnet
        priceFeed = AggregatorV3Interface(
            0x5f4eC3Df9cbd43714FE2740f5E3616155c5b8419
        );
    }
    
    // Получение последней цены
    function getLatestPrice() public view returns (int) {
        (
            uint80 roundID,
            int price,
            uint startedAt,
            uint timeStamp,
            uint80 answeredInRound
        ) = priceFeed.latestRoundData();
        return price;
    }
    
    // Получение цены с проверками
    function getVerifiedPrice() public view returns (
        int256 price,
        uint256 timestamp
    ) {
        (
            uint80 roundID,
            int256 answer,
            uint256 startedAt,
            uint256 updatedAt,
            uint80 answeredInRound
        ) = priceFeed.latestRoundData();
        
        require(answer > 0, "Negative price");
        require(
            updatedAt >= block.timestamp - 1 hours,
            "Stale price"
        );
        require(
            answeredInRound >= roundID,
            "Stale round"
        );
        
        return (answer, updatedAt);
    }
}
```

### **3. Безопасное использование**

```solidity
contract SafePriceFeedConsumer {
    AggregatorV3Interface public immutable priceFeed;
    uint256 public constant GRACE_PERIOD = 1 hours;
    int256 public constant MIN_PRICE = 0;
    int256 public constant MAX_PRICE_CHANGE = 50; // 50%
    
    int256 private lastPrice;
    
    constructor(address _priceFeed) {
        priceFeed = AggregatorV3Interface(_priceFeed);
    }
    
    function getSafePrice() external returns (int256) {
        (
            uint80 roundId,
            int256 price,
            uint256 startedAt,
            uint256 updatedAt,
            uint80 answeredInRound
        ) = priceFeed.latestRoundData();
        
        // Базовые проверки
        require(price >= MIN_PRICE, "Invalid price");
        require(updatedAt > 0, "Round not complete");
        require(
            answeredInRound >= roundId,
            "Stale round"
        );
        
        // Проверка свежести данных
        require(
            block.timestamp - updatedAt <= GRACE_PERIOD,
            "Data too old"
        );
        
        // Проверка резких изменений
        if (lastPrice > 0) {
            int256 priceChange = abs(
                ((price - lastPrice) * 100) / lastPrice
            );
            require(
                priceChange <= MAX_PRICE_CHANGE,
                "Price change too high"
            );
        }
        
        lastPrice = price;
        return price;
    }
}
```

### **4. Расширенные возможности**

```solidity
contract AdvancedPriceFeedConsumer {
    struct PriceData {
        int256 price;
        uint256 timestamp;
        uint256 heartbeat;
        uint8 decimals;
    }
    
    mapping(address => PriceData) public priceFeeds;
    
    // Добавление нового фида
    function addPriceFeed(
        address token,
        address feedAddress
    ) external {
        AggregatorV3Interface feed = AggregatorV3Interface(
            feedAddress
        );
        
        (
            ,
            int256 price,
            ,
            uint256 updatedAt,
            
        ) = feed.latestRoundData();
        
        priceFeeds[token] = PriceData({
            price: price,
            timestamp: updatedAt,
            heartbeat: 1 hours,
            decimals: feed.decimals()
        });
    }
    
    // Получение цены в USD с нормализацией decimals
    function getNormalizedPrice(
        address token
    ) external view returns (uint256) {
        PriceData memory data = priceFeeds[token];
        require(data.price > 0, "Price feed not found");
        
        // Нормализация к 18 decimals
        uint8 feedDecimals = data.decimals;
        if (feedDecimals < 18) {
            return uint256(data.price) * 10**(18 - feedDecimals);
        } else if (feedDecimals > 18) {
            return uint256(data.price) / 10**(feedDecimals - 18);
        }
        return uint256(data.price);
    }
    
    // Получение исторических данных
    function getHistoricalPrice(
        address token,
        uint80 roundId
    ) external view returns (PriceData memory) {
        AggregatorV3Interface feed = AggregatorV3Interface(
            address(priceFeeds[token])
        );
        
        (
            ,
            int256 price,
            ,
            uint256 updatedAt,
            
        ) = feed.getRoundData(roundId);
        
        return PriceData({
            price: price,
            timestamp: updatedAt,
            heartbeat: 1 hours,
            decimals: feed.decimals()
        });
    }
}
```

### **5. Мониторинг и обработка ошибок**

```solidity
contract PriceFeedMonitor {
    event PriceUpdated(
        address indexed feed,
        int256 price,
        uint256 timestamp
    );
    
    event PriceAnomaly(
        address indexed feed,
        int256 oldPrice,
        int256 newPrice,
        string reason
    );
    
    mapping(address => int256) public lastPrices;
    
    function monitorPrice(
        address feedAddress
    ) external returns (bool) {
        try AggregatorV3Interface(feedAddress).latestRoundData() returns (
            uint80 roundId,
            int256 price,
            uint256 startedAt,
            uint256 updatedAt,
            uint80 answeredInRound
        ) {
            // Проверка аномалий
            int256 oldPrice = lastPrices[feedAddress];
            if (oldPrice > 0) {
                int256 change = ((price - oldPrice) * 100) / oldPrice;
                
                if (abs(change) > 30) {
                    emit PriceAnomaly(
                        feedAddress,
                        oldPrice,
                        price,
                        "Large price change"
                    );
                    return false;
                }
            }
            
            lastPrices[feedAddress] = price;
            emit PriceUpdated(feedAddress, price, updatedAt);
            return true;
            
        } catch Error(string memory reason) {
            emit PriceAnomaly(
                feedAddress,
                lastPrices[feedAddress],
                0,
                reason
            );
            return false;
        } catch {
            emit PriceAnomaly(
                feedAddress,
                lastPrices[feedAddress],
                0,
                "Unknown error"
            );
            return false;
        }
    }
}
```

---

## Связанные темы
- [[6. Список вопросов]]
- [[Что такое Oracle?]]
- [[Как оракулы гарантируют надежность предоставляемых данных?]]
- [[Расскажите об атаке манипуляции ценой оракула]]

---

## Источники
- [Chainlink Price Feeds Documentation](https://docs.chain.link/data-feeds)
- [Price Feed Contract Addresses](https://docs.chain.link/data-feeds/price-feeds/addresses)
- [Using Price Feeds in Smart Contracts](https://docs.chain.link/getting-started/consuming-data-feeds) 