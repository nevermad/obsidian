## Короткий ответ

Unchecked блоки в Solidity - это специальные блоки кода, в которых отключаются проверки переполнения и антипереполнения для арифметических операций. Они были введены в Solidity 0.8.0 для оптимизации газа в случаях, когда разработчик уверен, что переполнение невозможно или является частью желаемого поведения.

---

## Подробный разбор

### **1. Механизм работы**

1. **Стандартное поведение:**
   ```solidity
   contract CheckedMath {
       function add(uint256 a, uint256 b) external pure returns (uint256) {
           // Автоматическая проверка переполнения
           return a + b; // Выбросит revert при переполнении
       }
       
       function subtract(uint256 a, uint256 b) external pure returns (uint256) {
           // Автоматическая проверка антипереполнения
           return a - b; // Выбросит revert если b > a
       }
   }
   ```

2. **Unchecked блоки:**
   ```solidity
   contract UncheckedMath {
       function add(uint256 a, uint256 b) external pure returns (uint256) {
           unchecked {
               return a + b; // Нет проверки переполнения
           }
       }
       
       function subtract(uint256 a, uint256 b) external pure returns (uint256) {
           unchecked {
               return a - b; // Нет проверки антипереполнения
           }
       }
   }
   ```

### **2. Применение для оптимизации газа**

1. **Счетчики циклов:**
   ```solidity
   contract LoopOptimization {
       // Неоптимизированная версия
       function standardLoop(uint256[] memory array) external pure returns (uint256) {
           uint256 sum;
           for (uint256 i = 0; i < array.length; i++) {
               sum += array[i];
           }
           return sum;
       }
       
       // Оптимизированная версия
       function optimizedLoop(uint256[] memory array) external pure returns (uint256) {
           uint256 sum;
           for (uint256 i = 0; i < array.length;) {
               sum += array[i];
               unchecked { i++; }
           }
           return sum;
       }
   }
   ```

2. **Математические операции:**
   ```solidity
   contract MathOptimization {
       // Оптимизация вычисления процентов
       function calculatePercentage(
           uint256 amount,
           uint256 bps
       ) external pure returns (uint256) {
           // bps - базисные пункты (1 bps = 0.01%)
           unchecked {
               // Безопасно, так как bps <= 10000
               return (amount * bps) / 10000;
           }
       }
       
       // Оптимизация уменьшения баланса
       function decreaseBalance(
           uint256 balance,
           uint256 amount
       ) external pure returns (uint256) {
           require(balance >= amount, "Insufficient balance");
           unchecked {
               // Безопасно после проверки
               return balance - amount;
           }
       }
   }
   ```

### **3. Безопасное использование**

1. **Проверки безопасности:**
   ```solidity
   contract SafeUnchecked {
       function safeOperation(uint256 a, uint256 b) external pure returns (uint256) {
           // Проверки перед unchecked блоком
           require(b != 0, "Division by zero");
           require(a >= b, "Underflow protection");
           
           unchecked {
               // Теперь безопасно
               return a - b;
           }
       }
       
       function safeMul(uint256 a, uint256 b) external pure returns (uint256) {
           // Проверка переполнения
           if (a != 0) {
               require(b <= type(uint256).max / a, "Overflow");
           }
           
           unchecked {
               return a * b;
           }
       }
   }
   ```

2. **Документирование:**
   ```solidity
   contract DocumentedUnchecked {
       /// @notice Вычисляет сумму элементов массива
       /// @dev Использует unchecked для оптимизации газа в цикле
       /// @param array Массив для суммирования
       function optimizedSum(
           uint256[] memory array
       ) external pure returns (uint256) {
           uint256 sum;
           uint256 length = array.length;
           
           for (uint256 i = 0; i < length;) {
               sum += array[i];
               unchecked { i++; }
           }
           
           return sum;
       }
   }
   ```

### **4. Сравнение газовых затрат**

1. **Бенчмарк:**
   ```solidity
   contract GasComparison {
       // ~28 gas
       function checkedIncrement(uint256 i) external pure returns (uint256) {
           return i + 1;
       }
       
       // ~5 gas
       function uncheckedIncrement(uint256 i) external pure returns (uint256) {
           unchecked { return i + 1; }
       }
       
       // ~3000 gas
       function standardLoop() external pure returns (uint256) {
           uint256 sum;
           for (uint256 i = 0; i < 100; i++) {
               sum += 1;
           }
           return sum;
       }
       
       // ~2000 gas
       function uncheckedLoop() external pure returns (uint256) {
           uint256 sum;
           for (uint256 i = 0; i < 100;) {
               sum += 1;
               unchecked { i++; }
           }
           return sum;
       }
   }
   ```

### **5. Лучшие практики**

1. **Паттерны использования:**
   ```solidity
   contract UncheckedPatterns {
       // Паттерн: уменьшение баланса
       function transfer(
           mapping(address => uint256) storage balances,
           address from,
           address to,
           uint256 amount
       ) internal {
           uint256 fromBalance = balances[from];
           require(fromBalance >= amount, "Insufficient balance");
           
           unchecked {
               balances[from] = fromBalance - amount;
               balances[to] += amount;
           }
       }
       
       // Паттерн: вычисление разницы
       function timeDelta(
           uint256 end,
           uint256 start
       ) internal pure returns (uint256) {
           require(end >= start, "Invalid time range");
           
           unchecked {
               return end - start;
           }
       }
   }
   ```

---

## Связанные темы
- [[6. Список вопросов]]
- [[Fixed point math in Solidity]]
- [[Gas optimisation tips]]
- [[Alice имеет 7.65 токена(в человеческой интерпретации). Какой баланс храниться на контракте: для стандартного токена OpenZeppelin или для USDC?]]

---

## Источники
- [Solidity Documentation - Unchecked Math](https://docs.soliditylang.org/en/latest/control-structures.html#checked-or-unchecked-arithmetic)
- [OpenZeppelin Math Libraries](https://github.com/OpenZeppelin/openzeppelin-contracts/tree/master/contracts/utils/math)
- [Solidity Gas Optimization Guide](https://github.com/iskdrews/awesome-solidity-gas-optimization) 