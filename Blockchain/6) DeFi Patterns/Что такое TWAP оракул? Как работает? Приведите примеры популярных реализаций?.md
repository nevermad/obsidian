---
title: TWAP Oracle
tags:
  - oracle
  - twap
  - defi
  - price
aliases:
  - time weighted average price
  - временное взвешивание цены
---

## Краткий ответ

TWAP (Time-Weighted Average Price) оракул - это механизм определения цены актива на основе среднего значения, взвешенного по времени. Он работает путем накопления цен в течение определенного периода и вычисления среднего значения с учетом длительности каждого ценового интервала. Популярные реализации включают Uniswap V2/V3 TWAP, SushiSwap и dYdX.

## Подробное объяснение

### Принцип работы

1. Накопление цен
   ```solidity
   // Пример реализации накопления цен
   contract TWAPAccumulator {
       struct Observation {
           uint32 timestamp;
           uint256 priceCumulative;
       }
       
       Observation[] public observations;
       
       function update() external {
           uint32 blockTimestamp = uint32(block.timestamp);
           uint256 currentPrice = getCurrentPrice();
           
           if (observations.length > 0) {
               Observation storage last = observations[observations.length - 1];
               uint32 timeElapsed = blockTimestamp - last.timestamp;
               uint256 priceCumulative = last.priceCumulative + (currentPrice * timeElapsed);
               observations.push(Observation(blockTimestamp, priceCumulative));
           } else {
               observations.push(Observation(blockTimestamp, 0));
           }
       }
   }
   ```

2. Вычисление TWAP
   ```solidity
   // Пример вычисления TWAP
   contract TWAPCalculator {
       function computeTWAP(
           uint256[] memory prices,
           uint256[] memory timestamps,
           uint256 period
       ) public pure returns (uint256) {
           require(prices.length >= 2, "Need at least 2 observations");
           
           uint256 weightedSum = 0;
           uint256 firstTimestamp = timestamps[0];
           
           for (uint i = 1; i < prices.length; i++) {
               uint256 timeElapsed = timestamps[i] - timestamps[i-1];
               weightedSum += prices[i-1] * timeElapsed;
           }
           
           return weightedSum / period;
       }
   }
   ```

### Популярные реализации

1. Uniswap V2
   ```solidity
   // Интерфейс Uniswap V2 TWAP
   interface IUniswapV2Pair {
       function price0CumulativeLast() external view returns (uint);
       function price1CumulativeLast() external view returns (uint);
       function getReserves() external view returns (
           uint112 reserve0,
           uint112 reserve1,
           uint32 blockTimestampLast
       );
   }
   
   contract UniswapV2TWAP {
       using FixedPoint for *;
       IUniswapV2Pair public pair;
       
       function consult(address token, uint amountIn) external view returns (uint amountOut) {
           (uint price0Cumulative, uint price1Cumulative,) = currentCumulativePrices(pair);
           // Логика вычисления TWAP
       }
   }
   ```

2. Uniswap V3
   - Улучшенная точность
   - Оптимизированное хранение
   - Конфигурируемые периоды

3. SushiSwap
   - Форк Uniswap V2
   - Дополнительные проверки
   - Интеграция с другими протоколами

4. dYdX
   - Специализированный оракул
   - Высокая частота обновлений
   - Защита от манипуляций

### Преимущества и недостатки

1. Преимущества
   - Устойчивость к манипуляциям
   - Отсутствие внешних зависимостей
   - Прозрачность расчетов
   - Низкая стоимость использования

2. Недостатки
   - Задержка актуальных данных
   - Зависимость от ликвидности
   - Потребление газа при обновлении
   - Сложность реализации

### Примеры использования

1. Lending Protocols
   ```solidity
   // Пример использования TWAP в lending протоколе
   contract LendingProtocol {
       ITWAPOracle public oracle;
       uint256 public constant MIN_PERIOD = 30 minutes;
       
       function calculateCollateralValue(
           address token,
           uint256 amount
       ) public view returns (uint256) {
           uint256 twapPrice = oracle.getTWAP(token, MIN_PERIOD);
           return amount * twapPrice;
       }
   }
   ```

2. DEX Aggregators
   - Определение оптимальных маршрутов
   - Проверка проскальзывания
   - Арбитраж

3. Options Protocols
   - Определение цен исполнения
   - Расчет премий
   - Ликвидации

## Связанные темы

- [[6. Список вопросов]]
- [[Расскажите как работают on-chain оракулы цены]]
- [[Расскажите об атаке манипуляции ценой оракула]]
- [[Как оракулы гарантируют надежность предоставляемых данных?]]
- [[Расскажите о Chainlink Price Feed]]

## Источники
- [Uniswap V2 TWAP Documentation](https://docs.uniswap.org/contracts/v2/concepts/core-concepts/oracles)
- [Uniswap V3 TWAP Documentation](https://docs.uniswap.org/contracts/v3/concepts/oracle)
- [SushiSwap Documentation](https://dev.sushi.com/docs/Products/Oracle)
- [dYdX Documentation](https://docs.dydx.exchange/)
