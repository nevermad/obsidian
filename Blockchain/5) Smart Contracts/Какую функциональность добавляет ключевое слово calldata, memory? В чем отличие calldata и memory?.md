
## Короткий ответ

Ключевые слова `calldata` и `memory` в Solidity определяют, где хранятся данные при вызове функций. На уровне EVM `calldata` представляет собой неизменяемую область памяти, которая передается в контракт через транзакцию или вызов. `memory`, напротив, является изменяемой временной областью, используемой для вычислений внутри контракта. Основное отличие заключается в том, что `calldata` экономит газ, так как данные хранятся вне контракта, а `memory` требует выделения памяти.

---

## Подробный разбор

### **Что такое calldata?**

#### **Определение:**
- **На уровне Solidity:**
  - `calldata` — это специальное хранилище, которое содержит аргументы, переданные в функцию.
  - Доступно только для чтения и не может быть изменено.
  - Используется для внешних (`external`) функций.

- **На уровне EVM:**
  - `calldata` представляет собой массив байтов, который передается в контракт через транзакцию или вызов.
  - Данные хранятся вне контракта и доступны через опкод `CALLDATA*` (например, `CALLDATALOAD`, `CALLDATASIZE`, `CALLDATACOPY`).
  - Пример:
    ```solidity
    function processArray(uint[] calldata data) external pure returns (uint) {
        return data.length;
    }
    ```

#### **Технические детали:**
- **Опкоды:**
  - `CALLDATALOAD`: Загружает данные из `calldata`.
  - `CALLDATASIZE`: Возвращает размер `calldata`.
  - `CALLDATACOPY`: Копирует данные из `calldata` в память.

- **Газовые затраты:**
  - Чтение данных из `calldata` дешевле, чем использование `memory`, так как данные уже находятся в блокчейне.

---

### **Что такое memory?**

#### **Определение:**
- **На уровне Solidity:**
  - `memory` — это временное хранилище, используемое для операций внутри функции.
  - Может быть изменено во время выполнения функции.
  - Данные удаляются после завершения функции.

- **На уровне EVM:**
  - `memory` представляет собой изменяемую область памяти, которая используется для временного хранения данных.
  - Доступ осуществляется через опкоды `MLOAD`, `MSTORE`, `MSTORE8`.
  - Пример:
    ```solidity
    function createArray() public pure returns (uint[] memory) {
        uint[] memory arr = new uint[](3);
        arr[0] = 1;
        arr[1] = 2;
        arr[2] = 3;
        return arr;
    }
    ```

#### **Технические детали:**
- **Опкоды:**
  - `MLOAD`: Загружает данные из памяти.
  - `MSTORE`: Сохраняет данные в памяти.
  - `MSTORE8`: Сохраняет один байт в памяти.

- **Газовые затраты:**
  - Выделение памяти требует больше газа, особенно для больших данных.

---

### **Отличия calldata и memory**

| Характеристика       | `calldata`                          | `memory`                          |
|----------------------|-------------------------------------|-----------------------------------|
| **Модифицируемость** | Только для чтения                  | Может быть изменена              |
| **Газовые затраты**  | Меньше                             | Больше                           |
| **Использование**    | Внешние функции                    | Внутренние и публичные функции   |
| **Хранение данных**  | Вне контракта                      | Временное хранилище в контракте  |

---

### **Когда использовать?**

#### **calldata:**
- Для внешних вызовов, особенно с большими данными.
- Когда данные не нужно изменять.
- Пример использования:
  ```solidity
  function transfer(address[] calldata recipients, uint[] calldata amounts) external {
      for (uint i = 0; i < recipients.length; i++) {
          payable(recipients[i]).transfer(amounts[i]);
      }
  }
  ```

#### **memory:**
- Для временных вычислений внутри функции.
- Когда данные должны быть изменяемыми.
- Пример использования:
  ```solidity
  function calculateSum(uint[] memory values) internal pure returns (uint) {
      uint sum = 0;
      for (uint i = 0; i < values.length; i++) {
          sum += values[i];
      }
      return sum;
  }
  ```

---

### **Заключение**

Ключевые слова `calldata` и `memory` играют важную роль в управлении данными в смарт-контрактах. На уровне EVM они используют разные механизмы для работы с данными: `calldata` работает с данными, передаваемыми через транзакции, а `memory` предоставляет временное хранилище для вычислений. Понимание их различий критически важно для оптимизации газовых затрат и эффективной разработки смарт-контрактов.

---

## Связанные темы
- [Вернуться к списку вопросов](5.%20Список%20вопросов.md)
- [[Как работают модификаторы изменения состояния pure, view на уровне Solidity? Какие нюансы на уровне байткода EVM?]]
- [[Где хранятся переменные объявленные в параметрах функций смарт-контракта?]]
- [[Какие типы данных есть в Solidity?]]

---

## Источники
- [The EVM Handbook](https://noxx3xxon.notion.site/noxx3xxon/The-EVM-Handbook-bb38e175cc404111a391907c4975426d)
- [EVM opcodes & instructions set](https://www.evm.codes/)
- [EVM Deep Dives: The Path to Shadowy Super Coder](https://noxx.substack.com/p/evm-deep-dives-the-path-to-shadowy)
- [Deconstructing a Solidity Contract](https://blog.openzeppelin.com/deconstructing-a-solidity-smart-contract-part-i-introduction-832efd2d7737)
- [EVM puzzles](https://github.com/fvictorio/evm-puzzles)
- [Официальная документация по layout storage](https://docs.soliditylang.org/en/stable/internals/layout_in_storage.html)
- [Понимание хранения данных в Ethereum Smart Contracts](https://programtheblockchain.com/posts/2018/03/09/understanding-ethereum-smart-contract-storage/)
- [Подробное объяснение типов памяти Ethereum (memory, storage)](https://www.fatalerrors.org/a/19131jg.html)
