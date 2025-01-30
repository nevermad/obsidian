
## Короткий ответ

Между версиями Solidity 0.4, 0.5, 0.6, 0.7 и 0.8 произошли значительные изменения, включая улучшения безопасности, оптимизацию газа и новые функциональные возможности. Ключевые отличия включают: строгую типизацию (`0.5`), улучшенную обработку ошибок (`0.6`), поддержку ABI-кодера v2 (`0.7`) и встроенную проверку переполнения (`0.8`).

---

## Подробный разбор

### **Solidity 0.4**
- **Основные особенности:**
  - Первая стабильная версия Solidity.
  - Поддержка базовых функций смарт-контрактов.
  - Отсутствие строгой типизации для некоторых операций.

- **Пример:**
  ```solidity
  function add(uint a, uint b) returns (uint) {
      return a + b;
  }
  ```

### **Solidity 0.5**
- **Ключевые изменения:**
  - Введение строгой типизации:
    - `address` теперь имеет два типа: `address` и `address payable`.
    - Требуется явное преобразование между `uint` и `int`.
  - Удаление глобальных переменных, таких как `msg.gas`.

- **Пример:**
  ```solidity
  function transfer(address payable recipient, uint amount) public {
      recipient.transfer(amount);
  }
  ```

### **Solidity 0.6**
- **Ключевые изменения:**
  - Новый модификатор `virtual` для переопределения функций.
  - Улучшенная обработка ошибок с помощью `revert` и `require`.
  - Добавлены интерфейсы для контрактов.

- **Пример:**
  ```solidity
  interface IERC20 {
      function transfer(address to, uint amount) external;
  }
  ```

### **Solidity 0.7**
- **Ключевые изменения:**
  - Внедрение ABI-кодера v2:
    - Позволяет работать с динамическими массивами и сложными типами данных.
  - Удаление устаревших функций, таких как `callcode`.

- **Пример:**
  ```solidity
  function encodeData() public pure returns (bytes memory) {
      return abi.encode("example", uint(123));
  }
  ```

### **Solidity 0.8**
- **Ключевые изменения:**
  - Встроенная проверка переполнения и потери значимости:
    - Больше не требуется использовать библиотеку SafeMath.
  - Улучшения производительности и оптимизация газа.
  - Новые функции для работы с ошибками, такие как `error` и `revert`.

- **Пример:**
  ```solidity
  error InsufficientBalance(uint balance, uint required);

  function withdraw(uint amount) public {
      if (amount > address(this).balance) {
          revert InsufficientBalance({
              balance: address(this).balance,
              required: amount
          });
      }
      payable(msg.sender).transfer(amount);
  }
  ```

---

## Связанные темы
- [Вернуться к списку вопросов](5.%20Список%20вопросов.md)
- [[Что такое pragma? Как указать версию  >, <, = ?]]
- [[Какую функциональность добавляет ключевое слово calldata, memory? В чем отличие calldata и memory?]]
- [[Как работают модификаторы изменения состояния pure, view на уровне Solidity? Какие нюансы на уровне байткода EVM?]]

---

## Источники
- [Solidity Release Notes](https://github.com/ethereum/solidity/releases)
- [Solidity Documentation - Versions](https://docs.soliditylang.org/en/latest/installing-solidity.html#versioning)
---
