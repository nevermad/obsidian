---
title: On-chain оракулы цены
tags:
  - oracle
  - price
  - defi
  - amm
aliases:
  - ценовые оракулы
  - on-chain oracle
---

## Краткий ответ

On-chain оракулы цены - это смарт-контракты, которые определяют цены активов на основе данных, доступных непосредственно в блокчейне (например, состояние пулов ликвидности DEX). Надежность данных обеспечивается через механизмы временного взвешивания (TWAP), множественные источники данных, проверку ликвидности и математические модели определения манипуляций.

## Подробное объяснение

### Механизмы работы

1. Uniswap V2 TWAP Oracle
   ```solidity
   // Пример реализации TWAP оракула
   contract UniswapV2TWAPOracle {
       using FixedPoint for *;
       
       struct Observation {
           uint timestamp;
           uint price0Cumulative;
           uint price1Cumulative;
       }
       
       function currentCumulativePrices(
           address pair
       ) public view returns (
           uint price0Cumulative,
           uint price1Cumulative,
           uint32 blockTimestamp
       ) {
           blockTimestamp = uint32(block.timestamp % 2**32);
           price0Cumulative = IUniswapV2Pair(pair).price0CumulativeLast();
           price1Cumulative = IUniswapV2Pair(pair).price1CumulativeLast();
       }
       
       function computeTWAP(
           uint[] memory prices,
           uint[] memory timestamps
       ) public pure returns (uint) {
           require(prices.length > 1 && timestamps.length == prices.length);
           uint timeWeightedPrice;
           for (uint i = 1; i < prices.length; i++) {
               uint timeDelta = timestamps[i] - timestamps[i-1];
               timeWeightedPrice += prices[i-1] * timeDelta;
           }
           return timeWeightedPrice / (timestamps[timestamps.length-1] - timestamps[0]);
       }
   }
   ```

2. Curve Finance
   - Использование виртуального баланса
   - Moving average для цен
   - Проверка глубины ликвидности

3. Balancer V2
   - Weighted average pricing
   - Множественные пулы
   - Динамические веса

### Гарантии надежности

1. Временное взвешивание
   ```solidity
   // Пример реализации взвешивания по времени
   contract TimeWeightedPrice {
       struct PricePoint {
           uint256 price;
           uint256 timestamp;
           uint256 weight;
       }
       
       function calculateWeightedPrice(
           PricePoint[] memory points
       ) public pure returns (uint256) {
           uint256 totalWeight;
           uint256 weightedSum;
           
           for (uint i = 0; i < points.length; i++) {
               totalWeight += points[i].weight;
               weightedSum += points[i].price * points[i].weight;
           }
           
           return weightedSum / totalWeight;
       }
   }
   ```

2. Проверка ликвидности
   - Минимальный объем пула
   - Соотношение активов
   - История торгов

3. Защита от манипуляций
   ```solidity
   // Пример проверки на манипуляции
   contract ManipulationResistant {
       uint256 constant MAX_PRICE_CHANGE = 10; // 10%
       uint256 constant MIN_LIQUIDITY = 1000 ether;
       
       function validatePrice(
           uint256 oldPrice,
           uint256 newPrice,
           uint256 liquidity
       ) public pure returns (bool) {
           require(liquidity >= MIN_LIQUIDITY, "Insufficient liquidity");
           
           uint256 priceChange = calculatePercentChange(oldPrice, newPrice);
           return priceChange <= MAX_PRICE_CHANGE;
       }
   }
   ```

### Примеры использования

1. DEX Агрегация
   ```solidity
   // Пример агрегации цен с DEX
   contract DEXAggregator {
       struct DEXPrice {
           address dex;
           uint256 price;
           uint256 liquidity;
       }
       
       function getAggregatedPrice(
           DEXPrice[] memory prices
       ) public pure returns (uint256) {
           uint256 totalLiquidity;
           uint256 weightedPrice;
           
           for (uint i = 0; i < prices.length; i++) {
               totalLiquidity += prices[i].liquidity;
               weightedPrice += prices[i].price * prices[i].liquidity;
           }
           
           return weightedPrice / totalLiquidity;
       }
   }
   ```

2. Lending Protocols
   - Обеспечение займов
   - Ликвидации
   - Процентные ставки

3. Derivatives
   - Синтетические активы
   - Опционы
   - Фьючерсы

### Ограничения и риски

1. Зависимость от ликвидности
   - Необходимость глубоких пулов
   - Риск манипуляций при низкой ликвидности
   - Влияние крупных сделок

2. Flash loan атаки
   - Временная манипуляция ценами
   - Арбитраж между пулами
   - Необходимость TWAP

3. Задержка данных
   - Период усреднения
   - Компромисс между точностью и безопасностью
   - Устаревание данных

## Связанные темы

- [[Что такое TWAP оракул?]]
- [[Расскажите об атаке манипуляции ценой оракула]]
- [[Расскажите о Chainlink Price Feed]]
- [[Как оракулы гарантируют надежность предоставляемых данных?]]

## Источники
- [Uniswap V2 Oracles](https://docs.uniswap.org/contracts/v2/concepts/core-concepts/oracles)
- [Curve Finance Documentation](https://curve.readthedocs.io/)
- [Balancer V2 Price Oracle](https://docs.balancer.fi/concepts/oracles)
- [DeFi Security Best Practices](https://consensys.github.io/smart-contract-best-practices/development-recommendations/defi-integration/price-oracles/)
