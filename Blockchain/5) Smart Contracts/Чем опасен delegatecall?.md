
## Короткий ответ

`Delegatecall` опасен, потому что он выполняет код целевого контракта в контексте вызывающего контракта, что может привести к непредсказуемым изменениям в storage. Это особенно рискованно, если структура storage вызывающего и целевого контрактов не совпадает.

---

## Подробный разбор

### **Чем опасен `delegatecall`?**
1. **Определение:**
   - `Delegatecall` выполняет код целевого контракта в контексте вызывающего контракта.
   - Изменения применяются к storage вызывающего контракта, что может привести к непредсказуемым последствиям.

2. **Пример проблемы:**
   ```solidity
   contract Logic {
       uint public value;

       function updateValue(uint _value) public {
           value = _value;
       }
   }

   contract Proxy {
       address public logic;
       uint public balance;

       constructor(address _logic) {
           logic = _logic;
       }

       fallback() external payable {
           address(logic).delegatecall(msg.data);
       }
   }
   ```

   - В этом примере:
     - Если контракт `Logic` изменяет переменную `value`, это повлияет на переменную `balance` в контракте `Proxy`.
     - Это происходит из-за того, что storage слотов совпадают по индексам, но их назначение различается.

3. **Технические детали:**
   - На уровне EVM `delegatecall` использует storage вызывающего контракта.
   - Если структура storage вызывающего и целевого контрактов не совпадает, это может привести к ошибкам.

4. **Особенности:**
   - Проблемы возникают, когда контракты имеют разные структуры storage.
   - Неправильное использование `delegatecall` может привести к уязвимостям безопасности.

5. **Подводные камни:**
   - Сложность отладки, так как ошибки могут быть скрытыми.
   - Риск потери средств или данных.

---

### **Как избежать проблем с `delegatecall`?**
1. **Рекомендации:**
   - Убедитесь, что структура storage вызывающего и целевого контрактов совпадает.
   - Используйте `delegatecall` только для доверенных контрактов.

2. **Пример безопасного использования:**
   ```solidity
   contract Logic {
       uint public value;

       function updateValue(uint _value) public {
           value = _value;
       }
   }

   contract Proxy {
       address public logic;
       uint public value;

       constructor(address _logic) {
           logic = _logic;
       }

       fallback() external payable {
           address(logic).delegatecall(msg.data);
       }
   }
   ```

   - В этом примере:
     - Структура storage контрактов `Logic` и `Proxy` совпадает, что делает использование `delegatecall` безопасным.

3. **Особенности:**
   - Тщательно проверяйте код целевого контракта перед использованием `delegatecall`.
   - Избегайте использования `delegatecall` для неизвестных контрактов.

---

### **Пример атаки через `delegatecall`**
```solidity
contract Malicious {
    uint public value;

    function exploit(address proxy) public {
        proxy.delegatecall(abi.encodeWithSignature("updateValue(uint256)", 0));
    }
}
```

- В этом примере:
  - Контракт `Malicious` вызывает `delegatecall` на контракт `Proxy`.
  - Это может привести к изменению переменной `value` в контракте `Proxy`.

---

## Связанные темы
- [Вернуться к списку вопросов](5.%20Список%20вопросов.md)
- [[Что такое delegatecall? Как представлен на уровне EVM? Откуда берется storage, откуда bytecode? Какое значение msg.sender, msg.value внутри вызова delegatecall? Когда стоит применять?]]
- [[Что происходит после выполнения selfdestruct?]]

---

## Источники
- [Solidity Documentation - Delegatecall](https://docs.soliditylang.org/en/latest/introduction-to-smart-contracts.html#delegatecall-callcode-and-libraries)
- [Understanding Security Risks of Delegatecall](https://ethereum.stackexchange.com/questions/3667/difference-between-call-callcode-and-delegatecall)
---
