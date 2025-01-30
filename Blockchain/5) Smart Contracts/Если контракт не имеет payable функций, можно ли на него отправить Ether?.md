
## Короткий ответ

Если контракт не имеет `payable` функций, на него все равно можно отправить Ether через специальные механизмы, такие как `selfdestruct` или mining rewards (устаревший механизм). Однако это может привести к блокировке средств, если контракт не имеет механизма вывода Ether.

---

## Подробный разбор

### **Можно ли отправить Ether на контракт без `payable` функций?**
1. **Ответ:**
   - Да, но только через специальные механизмы:
     - Саморазрушение (`selfdestruct`) другого контракта.
     - Mining rewards (устаревший механизм).

2. **Пример с `selfdestruct`:**
   ```solidity
   contract Sender {
       function destroyAndSend(address payable recipient) public {
           selfdestruct(recipient);
       }
   }

   contract NonPayable {
       // Нет payable функций
   }
   ```

   - В этом примере:
     - Контракт `Sender` отправляет весь свой баланс на адрес контракта `NonPayable` через `selfdestruct`.
     - Контракт `NonPayable` получает Ether, даже если у него нет `payable` функций.

3. **Технические детали:**
   - На уровне EVM отправка Ether через `selfdestruct` не вызывает выполнение кода контракта.
   - Это может привести к блокировке средств, если контракт не имеет механизма вывода Ether.

4. **Особенности:**
   - Отправка Ether через `selfdestruct` не требует взаимодействия с функциями контракта.
   - Это может быть использовано для атаки "форсированного" отправления Ether.

5. **Подводные камни:**
   - Если контракт не имеет механизма вывода Ether, средства могут быть заблокированы навсегда.
   - Убедитесь, что контракт имеет функцию вывода Ether, даже если он не принимает Ether напрямую.

---

### **Пример блокировки средств**
```solidity
contract NonPayable {
    // Нет payable функций и механизма вывода Ether
}
```

- В этом примере:
  - Контракт может получить Ether через `selfdestruct`, но не имеет способа вывести его.
  - Это приводит к блокировке средств.

---

### **Как избежать блокировки средств?**
1. **Рекомендации:**
   - Добавьте функцию вывода Ether, даже если контракт не принимает Ether напрямую.
   - Пример:
     ```solidity
     contract SafeContract {
         address payable owner;

         constructor() {
             owner = payable(msg.sender);
         }

         function withdraw() public {
             require(msg.sender == owner, "Not the owner");
             owner.transfer(address(this).balance);
         }
     }
     ```

2. **Особенности:**
   - Функция `withdraw` позволяет владельцу вывести заблокированные средства.

---

## Связанные темы
- [Вернуться к списку вопросов](5.%20Список%20вопросов.md)
- [[Что такое msg.value?]]
- [[Разница payable и non-payable addresses?]]

---

## Источники
- [Solidity Documentation - Receive Ether Function](https://docs.soliditylang.org/en/latest/contracts.html#receive-ether-function)
- [Understanding Forced Ether Sending in Solidity](https://ethereum.stackexchange.com/questions/68407/what-happens-if-you-send-ether-to-a-contract-without-a-payable-fallback-or-recei)
---