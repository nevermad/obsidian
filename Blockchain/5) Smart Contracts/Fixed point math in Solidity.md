## Обзор
Solidity не поддерживает дробные числа напрямую. Для работы с дробными числами используется **арифметика с фиксированной точкой** (fixed-point arithmetic). Это позволяет выполнять точные вычисления с дробными числами, используя целые числа с фиксированным масштабированием.

---

## Основные концепции

### 1. **Фиксированная точка**
- Фиксированная точка представляет дробные числа как целые числа с фиксированным количеством знаков после запятой.
- Например, число `1.23` может быть представлено как `123` с масштабированием `100`.

### 2. **Масштабирование**
- Масштабирование определяет, сколько знаков после запятой поддерживается.
- Например, масштабирование `1e18` означает 18 знаков после запятой.

---

## Примеры

### 1. Базовые операции
```solidity
// Масштабирование
uint256 public constant SCALE = 1e18;

// Умножение с фиксированной точкой
function multiply(uint256 x, uint256 y) public pure returns (uint256) {
    return (x * y) / SCALE;
}

// Деление с фиксированной точкой
function divide(uint256 x, uint256 y) public pure returns (uint256) {
    return (x * SCALE) / y;
}
```
- Умножение и деление выполняются с учётом масштабирования.

### 2. Сложение и вычитание
```solidity
// Сложение с фиксированной точкой
function add(uint256 x, uint256 y) public pure returns (uint256) {
    return x + y;
}

// Вычитание с фиксированной точкой
function subtract(uint256 x, uint256 y) public pure returns (uint256) {
    return x - y;
}
```
- Сложение и вычитание выполняются напрямую, так как числа уже масштабированы.

### 3. Пример использования
```solidity
contract FixedPointMath {
    uint256 public constant SCALE = 1e18;

    function multiply(uint256 x, uint256 y) public pure returns (uint256) {
        return (x * y) / SCALE;
    }

    function divide(uint256 x, uint256 y) public pure returns (uint256) {
        return (x * SCALE) / y;
    }

    function add(uint256 x, uint256 y) public pure returns (uint256) {
        return x + y;
    }

    function subtract(uint256 x, uint256 y) public pure returns (uint256) {
        return x - y;
    }
}
```
- Контракт реализует базовые операции с фиксированной точкой.

---

## Важные моменты

### 1. **Переполнение**
- При умножении и делении важно учитывать возможность переполнения.
- Используйте библиотеки, такие как `SafeMath`, для безопасных вычислений.

### 2. **Точность**
- Чем больше масштабирование, тем выше точность вычислений.
- Однако увеличение масштабирования увеличивает затраты на газ.

### 3. **Библиотеки**
- Используйте готовые библиотеки, такие как `ABDKMath64x64` или `DSMath`, для работы с фиксированной точкой.

---

## Пример с библиотекой ABDKMath64x64
```solidity
import "abdk-libraries-solidity/ABDKMath64x64.sol";

contract FixedPointExample {
    using ABDKMath64x64 for int128;

    function multiply(int128 x, int128 y) public pure returns (int128) {
        return x.mul(y);
    }

    function divide(int128 x, int128 y) public pure returns (int128) {
        return x.div(y);
    }

    function add(int128 x, int128 y) public pure returns (int128) {
        return x.add(y);
    }

    function subtract(int128 x, int128 y) public pure returns (int128) {
        return x.sub(y);
    }
}
```
- Библиотека `ABDKMath64x64` предоставляет удобные функции для работы с фиксированной точкой.

---

## Ссылки
- [Статья на Hackernoon](https://hackernoon.com/fixed-point-math-in-solidity-616f4508c6e8)
- [Библиотека ABDKMath64x64](https://github.com/abdk-consulting/abdk-libraries-solidity)