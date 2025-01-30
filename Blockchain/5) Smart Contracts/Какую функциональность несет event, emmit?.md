
## Короткий ответ

`event` в Solidity используется для создания событий, которые могут быть записаны в блокчейн и отслежены внешними приложениями. Ключевое слово `emit` используется для вызова события и записи данных в лог. События позволяют эффективно отслеживать изменения состояния контракта без использования `storage`.

---

## Подробный разбор

### **Что такое `event`?**
1. **Определение:**
   - `event` — это ключевое слово в Solidity, которое позволяет объявить событие.
   - События используются для записи данных в блокчейн, которые могут быть отслежены внешними приложениями.

2. **Пример:**
   ```solidity
   contract Example {
       event Transfer(address indexed from, address indexed to, uint amount);

       function transfer(address to, uint amount) public {
           emit Transfer(msg.sender, to, amount);
       }
   }
   ```

3. **Технические детали:**
   - На уровне EVM события хранятся в виде логов (log entries).
   - Логи содержат:
     - Адрес контракта.
     - Темы (indexed параметры).
     - Данные (non-indexed параметры).

4. **Особенности:**
   - События не занимают место в `storage`, что делает их экономичными с точки зрения газа.
   - Они предназначены только для внешнего использования и не могут быть прочитаны внутри контракта.

5. **Подводные камни:**
   - Неправильное использование индексированных параметров может увеличить затраты газа.
   - Размер данных события ограничен (максимум 32 кб).

---

### **Что такое `emit`?**
1. **Определение:**
   - `emit` — это ключевое слово, которое используется для вызова события.
   - Оно указывает на то, что данные должны быть записаны в лог.

2. **Пример:**
   ```solidity
   contract Example {
       event LogMessage(string message);

       function log(string memory message) public {
           emit LogMessage(message); // Вызов события
       }
   }
   ```

3. **Технические детали:**
   - На уровне байт-кода `emit` добавляет инструкцию для записи данных в лог.
   - Данные события становятся доступны для внешних приложений через ABI.

4. **Особенности:**
   - `emit` является обязательным для вызова событий (начиная с Solidity 0.4.21).
   - Без `emit` компилятор выдаст ошибку.

5. **Подводные камни:**
   - Забыть использовать `emit` при вызове события — распространенная ошибка у новичков.

---

### **Как работает `event` на уровне EVM?**
1. **Log Entries:**
   - На уровне EVM события хранятся в виде структур данных, называемых "log entries".
   - Каждая запись содержит:
     - Адрес контракта.
     - Темы (indexed параметры).
     - Данные (non-indexed параметры).

2. **Gas Costs:**
   - Запись событий дешевле, чем запись в `storage`.
   - Индексированные параметры увеличивают затраты газа.

---

### **Пример комбинированного использования**
```solidity
contract Bank {
    event Deposit(address indexed user, uint amount);
    event Withdraw(address indexed user, uint amount);

    function deposit() public payable {
        emit Deposit(msg.sender, msg.value); // Вызов события Deposit
    }

    function withdraw(uint amount) public {
        require(amount <= address(this).balance, "Insufficient balance");
        payable(msg.sender).transfer(amount);
        emit Withdraw(msg.sender, amount); // Вызов события Withdraw
    }
}
```

- В этом примере:
  - Событие `Deposit` вызывается при пополнении счета.
  - Событие `Withdraw` вызывается при выводе средств.

---

### **Сколько параметров может быть в `event`?**
1. **Ответ:**
   - В событии может быть любое количество параметров.
   - Однако только 3 параметра могут быть помечены как `indexed`.

2. **Пример:**
   ```solidity
   event Transaction(
       address indexed from,
       address indexed to,
       uint indexed amount,
       string message
   );

   function transfer(address to, uint amount, string memory message) public {
       emit Transaction(msg.sender, to, amount, message);
   }
   ```

   - В этом примере:
     - `from`, `to` и `amount` — индексированные параметры.
     - `message` — неиндексированный параметр.

---

### **Как работают индексированные параметры?**
1. **Определение:**
   - Параметры, помеченные как `indexed`, добавляются в темы лога.
   - Максимум 3 параметра могут быть индексированы.

2. **Пример:**
   ```solidity
   event LogData(address indexed user, uint amount);

   function log(uint amount) public {
       emit LogData(msg.sender, amount);
   }
   ```

   - В этом примере:
     - `user` — индексированный параметр (добавляется в темы).
     - `amount` — неиндексированный параметр (добавляется в данные).

3. **Особенности:**
   - Индексированные параметры позволяют фильтровать события.
   - Неиндексированные параметры содержат больше информации, но не поддерживают фильтрацию.

---

## Связанные темы
- [Вернуться к списку вопросов](5.%20Список%20вопросов.md)
- [[Каким образом представлено логирование? Особенности и ограничения.]]
- [[Как оперативно отслеживать важные изменения в работе вашего смарт-контракта? Например: у вас есть контракт выпуска NFT и вы хотели бы знать когда и какая NFT была выпущена.]]

---

## Источники
- [Solidity Documentation - Events](https://docs.soliditylang.org/en/latest/contracts.html#events)
- [Understanding Ethereum Logs and Events](https://ethereum.stackexchange.com/questions/12950/what-are-solidity-events-and-how-they-are-related-to-topics-and-logs)
---
