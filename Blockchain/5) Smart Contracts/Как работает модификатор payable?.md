
## Короткий ответ

Модификатор `payable` в Solidity позволяет функциям или адресам принимать Ether. Без этого модификатора функция не может получать Ether, и попытка отправить Ether вызовет ошибку. На уровне EVM `payable` разрешает выполнение операции `CALL` с ненулевым значением `msg.value`.

---

## Подробный разбор

### **Как работает модификатор `payable`?**
1. **Определение:**
   - Модификатор `payable` указывает, что функция или адрес может принимать Ether.
   - Без `payable` попытка отправить Ether вызовет ошибку.

2. **Пример для функции:**
   ```solidity
   contract Example {
       function deposit() public payable {
           // Функция может принимать Ether
       }
   }
   ```

   - В этом примере:
     - Функция `deposit` помечена как `payable`, поэтому она может принимать Ether.

3. **Пример для адреса:**
   ```solidity
   contract Example {
       address payable public owner;

       constructor() {
           owner = payable(msg.sender);
       }

       function sendEther() public payable {
           owner.transfer(msg.value); // Отправка Ether владельцу
       }
   }
   ```

   - В этом примере:
     - Адрес `owner` помечен как `payable`, поэтому ему можно отправлять Ether.

4. **Технические детали:**
   - На уровне EVM `payable` разрешает выполнение операции `CALL` с ненулевым значением `msg.value`.
   - Если функция не помечена как `payable`, то при попытке отправить Ether вызов завершится ошибкой.

5. **Особенности:**
   - Модификатор `payable` используется только для функций или адресов.
   - Не все функции должны быть `payable`, если они не предназначены для приема Ether.

6. **Подводные камни:**
   - Неправильное использование `payable` может привести к уязвимостям (например, неконтролируемый прием Ether).
   - Убедитесь, что контракт имеет механизм вывода Ether, чтобы избежать блокировки средств.

---

### **Как это работает на уровне EVM?**
1. **CALL Instruction:**
   - На уровне EVM отправка Ether выполняется через инструкцию `CALL`.
   - Если функция не помечена как `payable`, то при попытке выполнить `CALL` с ненулевым значением `msg.value` вызов завершится ошибкой.

2. **Gas Costs:**
   - Вызов `payable` функции требует газа, так как происходит изменение состояния контракта.
   - Отправка Ether также требует газа.

3. **Пример байт-кода:**
   - Для функции `deposit` байт-код содержит инструкции для обработки входящего Ether.

---

### **Пример комбинированного использования**
```solidity
contract Bank {
    address payable public owner;
    uint public balance;

    constructor() {
        owner = payable(msg.sender);
    }

    function deposit() public payable {
        balance += msg.value; // Добавление отправленного Ether к балансу
    }

    function withdraw(uint amount) public {
        require(balance >= amount, "Insufficient balance");
        balance -= amount;
        owner.transfer(amount); // Отправка Ether владельцу
    }
}
```

- В этом примере:
  - Функция `deposit` помечена как `payable`, поэтому она может принимать Ether.
  - Функция `withdraw` отправляет Ether владельцу.

---

### **Что такое `msg.value`?**
1. **Определение:**
   - `msg.value` — это глобальная переменная, которая содержит количество Ether, отправленное с транзакцией.
   - Доступна только внутри функций, помеченных как `payable`.

2. **Пример:**
   ```solidity
   contract Example {
       uint public receivedAmount;

       function deposit() public payable {
           receivedAmount = msg.value; // Сохранение отправленного Ether
       }
   }
   ```

   - В этом примере:
     - Переменная `receivedAmount` сохраняет значение `msg.value`.

3. **Технические детали:**
   - На уровне EVM `msg.value` передается как часть транзакции.
   - Если функция не помечена как `payable`, то `msg.value` будет равен нулю.

4. **Особенности:**
   - `msg.value` доступна только внутри `payable` функций.
   - Значение `msg.value` измеряется в Wei.

5. **Подводные камни:**
   - Неправильная обработка `msg.value` может привести к уязвимостям (например, переполнение баланса).

---

### **Разница между `payable` и `non-payable` адресами**
1. **Payable Addresses:**
   - Адреса, помеченные как `payable`, могут принимать Ether.
   - Пример:
     ```solidity
     address payable owner = payable(0xYourAddress);
     ```

2. **Non-Payable Addresses:**
   - Адреса без модификатора `payable` не могут принимать Ether.
   - Пример:
     ```solidity
     address owner = 0xYourAddress;
     ```

3. **Особенности:**
   - Преобразование обычного адреса в `payable` выполняется с помощью `payable(address)`.

---

### **Если контракт не имеет `payable` функций, можно ли на него отправить Ether?**
1. **Ответ:**
   - Да, но только через специальные механизмы:
     - Саморазрушение (`selfdestruct`) другого контракта.
     - Mining rewards (устаревший механизм).

2. **Пример:**
   ```solidity
   contract NonPayable {
       // Нет payable функций
   }
   ```

   - В этом примере:
     - Контракт не может принимать Ether через обычные транзакции.
     - Однако Ether может быть отправлен через `selfdestruct`.

3. **Особенности:**
   - Отправка Ether через `selfdestruct` не вызывает выполнение кода контракта.
   - Это может привести к блокировке средств, если контракт не имеет механизма вывода Ether.

---

## Связанные темы
- [Вернуться к списку вопросов](5.%20Список%20вопросов.md)
- [[Что такое msg.value?]]
- [[Разница payable и non-payable addresses?]]

---

## Источники
- [Solidity Documentation - Payable](https://docs.soliditylang.org/en/latest/contracts.html#receive-ether-function)
- [Understanding Payable Functions in Solidity](https://ethereum.stackexchange.com/questions/91874/what-is-the-difference-between-public-private-internal-and-external-functions)
---