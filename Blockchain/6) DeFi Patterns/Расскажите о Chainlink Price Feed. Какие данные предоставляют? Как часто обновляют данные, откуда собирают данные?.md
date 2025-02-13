---
title: Chainlink Price Feed
tags:
  - oracle
  - chainlink
  - defi
  - price feed
aliases:
  - ценовые фиды
  - price oracle
---

## Краткий ответ

Chainlink Price Feed - это децентрализованный оракул цен, который предоставляет надежные данные о ценах криптовалют, фиатных валют, commodities и других активов. Данные обновляются каждый раз, когда цена отклоняется более чем на заданный порог (обычно 0.5-1%) или по истечении heartbeat интервала (от 1 минуты до 24 часов). Данные собираются из множества источников, включая централизованные и децентрализованные биржи, маркет-мейкеров и агрегаторов.

## Подробное объяснение

### Предоставляемые данные

1. Криптовалютные пары
   - BTC/USD, ETH/USD, LINK/USD
   - Кросс-курсы: BTC/ETH, LINK/ETH
   - Стейблкоины: USDC/USD, DAI/USD

2. Фиатные валюты
   - EUR/USD, GBP/USD, JPY/USD
   - Кросс-курсы основных валют
   - Emerging markets валюты

3. Commodities
   - Gold (XAU/USD)
   - Silver (XAG/USD)
   - Oil (BRENT/USD)

4. Индексы
   - S&P 500
   - NASDAQ
   - Криптовалютные индексы

### Частота обновлений

1. Триггеры обновлений
   ```solidity
   // Пример конфигурации Price Feed
   struct FeedConfig {
       uint256 deviation = 0.5%; // Порог отклонения цены
       uint256 heartbeat = 1 hours; // Максимальный интервал
       uint256 minAnswers = 3; // Минимум ответов оракулов
   }
   ```

2. Heartbeat интервалы
   - Криптовалюты: 1-2 минуты
   - Фиатные пары: 24 часа
   - Commodities: 24 часа
   - Индексы: зависит от рынка

3. Deviation thresholds
   - Волатильные активы: 0.5%
   - Стабильные активы: 1%
   - Стейблкоины: 0.25%

### Источники данных

1. Централизованные биржи
   - Binance
   - Coinbase
   - Kraken
   - FTX
   - Gemini

2. Децентрализованные биржи
   - Uniswap
   - SushiSwap
   - Curve
   - Balancer

3. Маркет-мейкеры
   - Jump Trading
   - Cumberland
   - GSR
   - Alameda Research

4. Агрегаторы
   - CoinGecko
   - CoinMarketCap
   - Kaiko
   - Nomics

### Пример использования

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@chainlink/contracts/src/v0.8/interfaces/AggregatorV3Interface.sol";

contract PriceConsumerV3 {
    AggregatorV3Interface internal priceFeed;

    constructor() {
        // ETH/USD price feed on Ethereum mainnet
        priceFeed = AggregatorV3Interface(0x5f4eC3Df9cbd43714FE2740f5E3616155c5b8419);
    }

    function getLatestPrice() public view returns (
        uint80 roundId,
        int256 price,
        uint256 startedAt,
        uint256 updatedAt,
        uint80 answeredInRound
    ) {
        return priceFeed.latestRoundData();
    }

    function getDecimals() public view returns (uint8) {
        return priceFeed.decimals();
    }
}
```

### Механизмы обеспечения надежности

1. Агрегация данных
   - Медианное значение
   - Отсечение выбросов
   - Взвешивание источников

2. Валидация
   - Проверка временных меток
   - Мониторинг отклонений
   - Верификация подписей

3. Экономическая безопасность
   - Стейкинг LINK токенов
   - Репутационная система
   - Штрафы за некорректные данные

## Связанные темы

- [[6. Список вопросов]]
- [[Что такое Oracle?]]
- [[Расскажите о базовой архитектуре оракулов]]
- [[Как оракулы гарантируют надежность предоставляемых данных?]]
- [[Расскажите об атаке манипуляции ценой оракула]]
- [[Что такое TWAP оракул?]]

## Источники
- [Chainlink Data Feeds](https://docs.chain.link/data-feeds)
- [Price Feed Contract Addresses](https://docs.chain.link/data-feeds/price-feeds/addresses)
- [Chainlink Architecture Overview](https://docs.chain.link/architecture-overview/architecture-overview)
- [Chainlink Data Quality](https://chain.link/data-quality)
