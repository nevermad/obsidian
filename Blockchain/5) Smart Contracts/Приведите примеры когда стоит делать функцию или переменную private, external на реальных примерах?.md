
## Короткий ответ

Модификаторы `private` и `external` в Solidity используются для управления доступом к функциям и переменным. `private` ограничивает доступ только внутри контракта, а `external` позволяет вызывать функции только извне. На уровне EVM эти модификаторы влияют на способ хранения данных и вызова функций, что может привести к различным затратам газа.

---

## Подробный разбор

### **Когда использовать `private`?**

#### **Определение:**
- Переменные и функции с модификатором `private` доступны только внутри контракта, где они объявлены.
- Никакой внешний контракт или аккаунт не может получить к ним доступ через ABI.

#### **Пример использования:**
```solidity
contract Bank {
    uint private totalDeposits;

    function deposit(uint amount) public {
        totalDeposits += amount;
    }

    function getTotalDeposits() private view returns (uint) {
        return totalDeposits;
    }
}
```

#### **Технические детали на уровне EVM:**
- **Хранение данных:**
  - Переменные с модификатором `private` хранятся в `storage`, но доступ к ним возможен только через внутренние вызовы.
  - На уровне EVM используется опкод `SLOAD` для чтения данных из `storage`.
- **Отсутствие внешнего интерфейса:**
  - Нет геттеров или обработчиков для внешних вызовов.

#### **Особенности:**
- Используется для защиты конфиденциальных данных.
- Меньше затрат газа по сравнению с `public`.

#### **Подводные камни:**
- Даже если переменная `private`, данные все равно хранятся в блокчейне и могут быть прочитаны напрямую из `storage`.
- Не обеспечивает полной безопасности, а только ограничивает доступ через ABI.

---

### **Когда использовать `external`?**

#### **Определение:**
- Функции с модификатором `external` доступны только для внешних вызовов.
- Переменные не могут быть объявлены как `external`.

#### **Пример использования:**
```solidity
contract Token {
    uint public totalSupply;

    function mint(uint amount) external {
        totalSupply += amount;
    }
}
```

#### **Технические детали на уровне EVM:**
- **Использование `calldata`:**
  - Аргументы функции хранятся в `calldata`, что делает внешние вызовы более эффективными.
  - На уровне EVM используется опкод `CALLDATALOAD` для чтения данных.
- **Ограничение на внутренние вызовы:**
  - Внутри контракта вызов `external` функции невозможен напрямую. Требуется использование `this.functionName()`.

#### **Особенности:**
- Экономит газ за счет использования `calldata`.
- Подходит для функций, которые не должны вызываться внутри контракта.

#### **Подводные камни:**
- Невозможно вызвать `external` функцию внутри контракта без использования `this.functionName()`.

---

### **Реальные примеры**

#### **Пример 1: Защита конфиденциальных данных (`private`)**
```solidity
contract SecureBank {
    uint private secretBalance;

    function deposit(uint amount) public {
        secretBalance += amount;
    }

    function withdraw(uint amount) public {
        require(secretBalance >= amount, "Insufficient balance");
        secretBalance -= amount;
        payable(msg.sender).transfer(amount);
    }

    function getSecretBalance() private view returns (uint) {
        return secretBalance;
    }
}
```
- **Анализ:**
  - `secretBalance` является `private`, что предотвращает прямой доступ к данным через ABI.
  - Функция `getSecretBalance` также `private`, чтобы защитить логику доступа к балансу.

#### **Пример 2: Оптимизация газа при внешних вызовах (`external`)**
```solidity
contract TokenMinter {
    uint public totalSupply;

    function mint(uint amount) external {
        totalSupply += amount;
    }

    function burn(uint amount) external {
        require(totalSupply >= amount, "Insufficient supply");
        totalSupply -= amount;
    }
}
```
- **Анализ:**
  - Функции `mint` и `burn` объявлены как `external`, так как они предназначены для вызова извне.
  - Использование `calldata` снижает затраты газа при передаче параметров.

---

### **Сравнение `private` и `external`**

| Характеристика      | `private`                          | `external`                        |
|---------------------|-------------------------------------|------------------------------------|
| **Доступ**          | Только внутри контракта            | Только извне                      |
| **Переменные**      | Поддерживаются                    | Не поддерживаются                 |
| **Газовые затраты** | Низкие                             | Очень низкие (благодаря `calldata`) |
| **Использование**    | Защита конфиденциальных данных     | Оптимизация внешних вызовов       |

---

### **Пример комбинированного использования**

```solidity
contract Example {
    uint private internalValue;
    uint public externalValue;

    function setInternalValue(uint value) private {
        internalValue = value;
    }

    function setExternalValue(uint value) external {
        externalValue = value;
    }

    function getInternalValue() private view returns (uint) {
        return internalValue;
    }

    function getExternalValue() public view returns (uint) {
        return externalValue;
    }
}
```
- **Анализ:**
  - `internalValue` и `setInternalValue` используются только внутри контракта.
  - `externalValue` и `setExternalValue` доступны для внешних вызовов.

---

### **Заключение**

Модификаторы `private` и `external` в Solidity играют ключевую роль в управлении доступом к данным и функциям. На уровне EVM они влияют на способ хранения данных и вызова функций, что может привести к различным затратам газа. Понимание этих механизмов критически важно для оптимизации смарт-контрактов.

---

## Связанные темы
- [Вернуться к списку вопросов](5.%20Список%20вопросов.md)
- [[Как работают модификаторы изменения состояния pure, view на уровне Solidity? Какие нюансы на уровне байткода EVM?]]
- [[Что такое упаковка структур? Приведите примеры.]]

---

## Источники
- [Solidity Documentation - Visibility and Getters](https://docs.soliditylang.org/en/latest/contracts.html#visibility-and-getters)
- [Understanding Function Visibility in Solidity](https://ethereum.stackexchange.com/questions/91874/what-is-the-difference-between-public-private-internal-and-external-functions)
- [The EVM Handbook](https://noxx3xxon.notion.site/noxx3xxon/The-EVM-Handbook-bb38e175cc404111a391907c4975426d)
- [EVM opcodes & instructions set](https://www.evm.codes/)