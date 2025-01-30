
## Короткий ответ

`Receive` функция — это специальная функция в Solidity, которая вызывается, если контракт получает Ether без данных. Она должна быть помечена как `external` и `payable`. На уровне EVM она представлена как часть контракта и выполняется при отправке Ether без данных.

---

## Подробный разбор

### **Что такое `receive` функция?**
1. **Определение:**
   - `Receive` функция вызывается, если контракт получает Ether без данных.
   - Она должна быть помечена как `external` и `payable`.

2. **Пример:**
   ```solidity
   contract Example {
       receive() external payable {
           // Логика receive функции
       }
   }
   ```

3. **Технические детали:**
   - На уровне EVM `receive` функция вызывается, если контракт получает Ether без данных.
   - Если контракт имеет `receive` функцию, она вызывается вместо `fallback`.

4. **Особенности:**
   - Должна быть максимально простой, чтобы минимизировать затраты газа.
   - Может быть использована для обработки входящих платежей.

5. **Подводные камни:**
   - Сложная логика в `receive` может привести к высоким затратам газа.
   - Убедитесь, что контракт имеет механизм вывода Ether, чтобы избежать блокировки средств.

---

### **Когда вызывается `receive` функция?**
1. **Вызов при отправке Ether без данных:**
   - Если контракт получает Ether без данных, вызывается `receive`.
   - Пример:
     ```solidity
     contract Example {
         receive() external payable {
             // Вызывается при отправке Ether без данных
         }
     }
     ```

2. **Отличие от `fallback`:**
   - Если контракт имеет `receive`, то при отправке Ether без данных вызывается именно `receive`.
   - Если контракт не имеет `receive`, то вызывается `fallback`.

---

### **Как это работает на уровне EVM?**
1. **CALL Instruction:**
   - На уровне EVM `receive` вызывается, если контракт получает Ether без данных.
   - Если контракт имеет `receive`, она вызывается вместо `fallback`.

2. **Gas Costs:**
   - Затраты газа зависят от логики внутри `receive`.

---

### **Пример комбинированного использования**
```solidity
contract Bank {
    uint public balance;

    receive() external payable {
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
  - `receive` функция добавляет отправленный Ether к балансу контракта.

---

## Связанные темы
- [Вернуться к списку вопросов](5.%20Список%20вопросов.md)
- [[Что такое fallback функция? Когда вызывается? Как представлена на уровне байткода EVM?]]
- [[Может ли произойти коллизия селекторов функции? Как решить эту проблему?]]

---

## Источники
- [Solidity Documentation - Receive Function](https://docs.soliditylang.org/en/latest/contracts.html#receive-ether-function)
- [Understanding Fallback and Receive Functions](https://ethereum.stackexchange.com/questions/81994/what-is-the-difference-between-fallback-and-receive-functions-in-solidity)
---