## Обзор
Оптимизация газа — важная часть разработки смарт-контрактов. Это помогает снизить затраты на выполнение транзакций и сделать контракты более эффективными. В этом документе собраны практические советы по оптимизации газа в Solidity.

---

## Основные советы

### 1. **Используйте `uint256` вместо `uint8`**
- Solidity работает с 256-битными числами, поэтому использование `uint8` может привести к дополнительным затратам газа из-за конвертации.
- Пример:
  ```solidity
  // Плохо
  uint8 public count;

  // Хорошо
  uint256 public count;
  ```

### 2. **Избегайте лишних операций с хранилищем**
- Операции с хранилищем (storage) дорогие. Минимизируйте их использование.
- Пример:
  ```solidity
  // Плохо
  uint256 public data;

  function setData(uint256 _data) public {
      data = _data;
  }

  // Хорошо
  function setData(uint256 _data) public {
      // Используйте локальные переменные, если возможно
      uint256 localData = _data;
      // Логика с localData
  }
  ```

### 3. **Кэшируйте переменные**
- Кэширование переменных, которые используются несколько раз, может снизить затраты газа.
- Пример:
  ```solidity
  // Плохо
  function calculate(uint256 a, uint256 b) public pure returns (uint256) {
      return a + b + a * b + a / b;
  }

  // Хорошо
  function calculate(uint256 a, uint256 b) public pure returns (uint256) {
      uint256 sum = a + b;
      uint256 product = a * b;
      uint256 division = a / b;
      return sum + product + division;
  }
  ```

### 4. **Используйте `external` вместо `public` для функций**
- Функции с модификатором `external` дешевле, чем `public`, так как они не копируют аргументы в память.
- Пример:
  ```solidity
  // Плохо
  function doSomething(uint256 a) public {
      // Логика
  }

  // Хорошо
  function doSomething(uint256 a) external {
      // Логика
  }
  ```

### 5. **Используйте `calldata` вместо `memory` для массивов**
- `calldata` дешевле, чем `memory`, так как данные не копируются.
- Пример:
  ```solidity
  // Плохо
  function processArray(uint256[] memory arr) public {
      // Логика
  }

  // Хорошо
  function processArray(uint256[] calldata arr) external {
      // Логика
  }
  ```

### 6. **Избегайте лишних проверок**
- Убедитесь, что проверки (например, `require`) действительно необходимы.
- Пример:
  ```solidity
  // Плохо
  function transfer(address to, uint256 amount) public {
      require(to != address(0), "Invalid address");
      require(amount > 0, "Amount must be greater than 0");
      // Логика
  }

  // Хорошо
  function transfer(address to, uint256 amount) public {
      require(to != address(0) && amount > 0, "Invalid input");
      // Логика
  }
  ```

### 7. **Используйте битовые операции**
- Битовые операции могут быть более эффективными, чем арифметические.
- Пример:
  ```solidity
  // Плохо
  uint256 public value = 10 * 2;

  // Хорошо
  uint256 public value = 10 << 1; // Сдвиг влево на 1 бит (умножение на 2)
  ```

### 8. **Оптимизация циклов**
- Минимизируйте операции внутри циклов, особенно если они связаны с хранилищем.
- Пример:
  ```solidity
  // Плохо
  for (uint256 i = 0; i < array.length; i++) {
      storageArray[i] = array[i];
  }

  // Хорошо
  uint256 length = array.length;
  for (uint256 i = 0; i < length; i++) {
      storageArray[i] = array[i];
  }
  ```

### 9. **Используйте `unchecked` для безопасных операций**
- В Solidity 0.8.0 и выше можно использовать `unchecked` для отключения проверок на переполнение, если вы уверены в безопасности операции.
- Пример:
  ```solidity
  // Плохо
  function increment(uint256 a) public pure returns (uint256) {
      return a + 1;
  }

  // Хорошо
  function increment(uint256 a) public pure returns (uint256) {
      unchecked {
          return a + 1;
      }
  }
  ```

### 10. **Используйте библиотеки для повторяющихся операций**
- Библиотеки могут помочь уменьшить размер контракта и оптимизировать газ.
- Пример:
  ```solidity
  library Math {
      function add(uint256 a, uint256 b) internal pure returns (uint256) {
          return a + b;
      }
  }

  contract MyContract {
      using Math for uint256;

      function calculate(uint256 a, uint256 b) public pure returns (uint256) {
          return a.add(b);
      }
  }
  ```

---

## Дополнительные советы

### 1. **Используйте `immutable` и `constant`**
- Переменные, помеченные как `immutable` или `constant`, не требуют записи в хранилище, что экономит газ.
- Пример:
  ```solidity
  // Хорошо
  uint256 public constant FIXED_VALUE = 100;
  address public immutable owner;

  constructor(address _owner) {
      owner = _owner;
  }
  ```

### 2. **Избегайте лишних событий**
- События (events) требуют газа. Используйте их только при необходимости.
- Пример:
  ```solidity
  // Плохо
  event Log(uint256 value);

  function doSomething(uint256 a) public {
      emit Log(a);
      // Логика
  }

  // Хорошо
  function doSomething(uint256 a) public {
      // Логика без лишних событий
  }
  ```

### 3. **Оптимизация упаковки переменных**
- Solidity упаковывает переменные в слоты по 32 байта. Используйте это для экономии газа.
- Пример:
  ```solidity
  // Плохо
  uint256 a;
  uint256 b;
  uint256 c;

  // Хорошо
  uint128 a;
  uint128 b;
  uint256 c;
  ```

---

## Заключение
- Оптимизация газа — это баланс между читаемостью кода и эффективностью.
- Используйте приведённые советы для снижения затрат газа, но не забывайте о безопасности и читаемости кода.

---

## Ссылки
- [Репозиторий Solidity Gas Optimization Tips](https://github.com/devanshbatham/Solidity-Gas-Optimization-Tips)
- [Документация Solidity](https://docs.soliditylang.org/en/latest/)