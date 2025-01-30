
## Короткий ответ

`Raw call` — это низкоуровневый вызов в Solidity, который позволяет взаимодействовать с другими контрактами или адресами. На уровне EVM он представлен инструкцией `CALL`. Его стоит применять, когда требуется гибкость, например, для вызова функций с динамическими параметрами или отправки Ether. Внутри `delegatecall` значения `msg.sender` и `msg.value` сохраняются из исходного вызова.

---

## Подробный разбор

### **Что такое `raw call`?**
1. **Определение:**
   - `Raw call` — это низкоуровневый способ взаимодействия с другими контрактами или адресами.
   - Он позволяет отправлять произвольные данные и Ether, а также задавать количество газа.

2. **Пример:**
   ```solidity
   contract Caller {
       function rawCall(address target, bytes memory data) public {
           (bool success, ) = target.call(data);
           require(success, "Call failed");
       }
   }
   ```

   - В этом примере:
     - Выполняется низкоуровневый вызов контракта по адресу `target` с данными `data`.

3. **Технические детали:**
   - На уровне EVM `raw call` представлен инструкцией `CALL`.
   - Позволяет отправлять Ether и данные одновременно.

4. **Особенности:**
   - `Raw call` не проверяет существование целевого контракта.
   - Может использоваться для вызова неизвестных функций.

5. **Подводные камни:**
   - Неправильное использование может привести к уязвимостям (например, повторному входу).
   - Необходимо тщательно обрабатывать результат вызова.

---

### **Когда стоит применять `raw call`?**
1. **Сценарии использования:**
   - Когда требуется гибкость, например, для вызова функций с динамическими параметрами.
   - Для отправки Ether вместе с данными.
   - Когда сигнатура функции неизвестна заранее.

2. **Пример:**
   ```solidity
   contract Example {
       function sendEtherAndData(address target, bytes memory data) public payable {
           (bool success, ) = target.call{value: msg.value}(data);
           require(success, "Call failed");
       }
   }
   ```

   - В этом примере:
     - Функция отправляет Ether и данные на адрес `target`.

---

### **Какое значение `msg.sender` и `msg.value` внутри вызова `delegatecall`?**
1. **Ответ:**
   - Внутри `delegatecall` значения `msg.sender` и `msg.value` сохраняются из исходного вызова.
   - Это связано с тем, что `delegatecall` выполняет код целевого контракта в контексте вызывающего контракта.

2. **Пример:**
   ```solidity
   contract A {
       uint public value;

       function setValue(uint _value) public {
           value = _value;
       }
   }

   contract B {
       uint public value;

       function delegateToA(address a, uint _value) public {
           a.delegatecall(abi.encodeWithSignature("setValue(uint256)", _value));
       }
   }
   ```

   - В этом примере:
     - `msg.sender` внутри `setValue` будет адресом, который вызвал `delegateToA`.
     - `msg.value` также сохранится из исходного вызова.

---

### **Как это работает на уровне EVM?**
1. **CALL Instruction:**
   - На уровне EVM `raw call` выполняется через инструкцию `CALL`.
   - Если вызывается `delegatecall`, используется инструкция `DELEGATECALL`.

2. **Gas Costs:**
   - Задание параметра `gas` влияет на общие затраты газа.
   - Неиспользованный газ возвращается отправителю.

---

## Связанные темы
- [Вернуться к списку вопросов](5.%20Список%20вопросов.md)
- [[Какую информацию необходимо передать в raw call чтобы вызвать определенную функцию другого контракта? Как кодировать эти данные? Какой layout у этих данных?]]
- [[Что такое delegatecall? Как представлен на уровне EVM? Откуда берется storage, откуда bytecode? Какое значение msg.sender, msg.value внутри вызова delegatecall? Когда стоит применять?]]

---

## Источники
- [Solidity Documentation - Low-Level Calls](https://docs.soliditylang.org/en/latest/control-structures.html#external-function-calls)
- [Understanding Delegatecall in Solidity](https://ethereum.stackexchange.com/questions/3667/difference-between-call-callcode-and-delegatecall)
---
