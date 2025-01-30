
## Короткий ответ

`Fallback` функция — это специальная функция в Solidity, которая вызывается, если вызванная функция не найдена или если контракт получает Ether без данных. На уровне EVM она представлена как часть контракта и выполняется при определенных условиях.

---

## Подробный разбор

### **Что такое `fallback` функция?**
1. **Определение:**
   - `Fallback` функция вызывается, если:
     - Нет совпадений с selector функции.
     - Контракт получает Ether без данных.
   - Она должна быть помечена как `external`.

2. **Пример:**
   ```solidity
   contract Example {
       fallback() external {
           // Логика fallback функции
       }
   }
   ```

3. **Технические детали:**
   - На уровне EVM `fallback` функция вызывается, если:
     - Нет совпадений с selector функции.
     - Контракт получает Ether без данных.

4. **Особенности:**
   - Может быть объединена с `receive` функцией для обработки входящих платежей.
   - Должна быть максимально простой, чтобы минимизировать затраты газа.

5. **Подводные камни:**
   - Сложная логика в `fallback` может привести к высоким затратам газа.
   - Убедитесь, что контракт имеет механизм вывода Ether, чтобы избежать блокировки средств.

---

### **Когда вызывается `fallback` функция?**
1. **Вызов при отсутствии совпадений:**
   - Если вызванная функция не найдена, вызывается `fallback`.
   - Пример:
     ```solidity
     contract Example {
         fallback() external {
             // Вызывается, если функция не найдена
         }
     }
     ```

2. **Вызов при отправке Ether без данных:**
   - Если контракт получает Ether без данных, вызывается `fallback`.
   - Пример:
     ```solidity
     contract Example {
         fallback() external payable {
             // Вызывается при отправке Ether без данных
         }
     }
     ```

---

### **Как это работает на уровне EVM?**
1. **CALL Instruction:**
   - На уровне EVM `fallback` вызывается, если нет совпадений с selector функции.
   - Если контракт получает Ether без данных, вызывается `fallback`.

2. **Gas Costs:**
   - Затраты газа зависят от логики внутри `fallback`.

---

### **Пример комбинированного использования**
```solidity
contract Bank {
    uint public balance;

    fallback() external payable {
        balance += msg.value; // Добавление отправленного Ether к балансу
    }

    function withdraw(uint amount) public {
        require(balance >= amount, "Insufficient balance");
        balance -= amount;
        payable(msg.sender).transfer(amount); // Отправка Ether обратно
    }
}
```

- В этом примере:
  - `fallback` функция добавляет отправленный Ether к балансу контракта.

---

## Связанные темы
- [Вернуться к списку вопросов](5.%20Список%20вопросов.md)
- [[Что такое receive функция? Когда вызывается? Как представлена на уровне байткода EVM?]]
- [[Может ли произойти коллизия селекторов функции? Как решить эту проблему?]]

---

## Источники
- [Solidity Documentation - Fallback Function](https://docs.soliditylang.org/en/latest/contracts.html#fallback-function)
- [Understanding Fallback and Receive Functions](https://ethereum.stackexchange.com/questions/81994/what-is-the-difference-between-fallback-and-receive-functions-in-solidity)
---