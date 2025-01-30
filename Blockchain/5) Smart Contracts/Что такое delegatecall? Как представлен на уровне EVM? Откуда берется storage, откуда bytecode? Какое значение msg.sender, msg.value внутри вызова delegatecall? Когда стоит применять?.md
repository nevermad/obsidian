
## Короткий ответ

`Delegatecall` — это низкоуровневый вызов в Solidity, который выполняет код целевого контракта в контексте вызывающего контракта. На уровне EVM он представлен инструкцией `DELEGATECALL`. Storage и bytecode берутся из вызывающего контракта, а `msg.sender` и `msg.value` сохраняются из исходного вызова. Применяется для использования библиотек или делегирования логики.

---

## Подробный разбор

### **Что такое `delegatecall`?**
1. **Определение:**
   - `Delegatecall` — это низкоуровневый вызов, который выполняет код целевого контракта в контексте вызывающего контракта.
   - Storage, `msg.sender` и `msg.value` сохраняются из вызывающего контракта.

2. **Пример:**
   ```solidity
   contract Library {
       uint public value;

       function setValue(uint _value) public {
           value = _value;
       }
   }

   contract User {
       uint public value;

       function useLibrary(address library, uint _value) public {
           library.delegatecall(abi.encodeWithSignature("setValue(uint256)", _value));
       }
   }
   ```

   - В этом примере:
     - Код функции `setValue` из контракта `Library` выполняется в контексте контракта `User`.
     - Переменная `value` в контракте `User` изменяется.

3. **Технические детали:**
   - На уровне EVM `delegatecall` представлен инструкцией `DELEGATECALL`.
   - Storage и контекст берутся из вызывающего контракта.

4. **Особенности:**
   - `Delegatecall` позволяет повторно использовать код без копирования данных.
   - Используется для библиотек или делегирования логики.

5. **Подводные камни:**
   - Неправильное использование может привести к уязвимостям (например, изменение неожиданных переменных в storage).

---

### **Как это работает на уровне EVM?**
1. **DELEGATECALL Instruction:**
   - На уровне EVM `delegatecall` выполняется через инструкцию `DELEGATECALL`.
   - Код целевого контракта выполняется в контексте вызывающего контракта.

2. **Storage:**
   - Storage берется из вызывающего контракта.
   - Изменения применяются к storage вызывающего контракта.

3. **Bytecode:**
   - Bytecode берется из целевого контракта.

4. **Gas Costs:**
   - Затраты газа зависят от выполнения кода целевого контракта.

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

### **Когда стоит применять `delegatecall`?**
1. **Сценарии использования:**
   - Для использования библиотек, которые изменяют storage вызывающего контракта.
   - Для делегирования логики между контрактами.

2. **Пример:**
   ```solidity
   contract Logic {
       uint public value;

       function updateValue(uint _value) public {
           value = _value;
       }
   }

   contract Proxy {
       address public logic;

       constructor(address _logic) {
           logic = _logic;
       }

       fallback() external payable {
           address(logic).delegatecall(msg.data);
       }
   }
   ```

   - В этом примере:
     - Контракт `Proxy` делегирует все вызовы контракту `Logic`.

---

## Связанные темы
- [Вернуться к списку вопросов](5.%20Список%20вопросов.md)
- [[Чем опасен delegatecall?]]
- [[Что происходит после выполнения selfdestruct?]]

---

## Источники
- [Solidity Documentation - Delegatecall](https://docs.soliditylang.org/en/latest/introduction-to-smart-contracts.html#delegatecall-callcode-and-libraries)
- [Understanding Delegatecall in Solidity](https://ethereum.stackexchange.com/questions/3667/difference-between-call-callcode-and-delegatecall)
---