
## Короткий ответ

В событии (`event`) может быть любое количество параметров, но только 3 параметра могут быть помечены как `indexed`. Индексированные параметры добавляются в темы лога, что позволяет фильтровать события. Неиндексированные параметры хранятся в данных лога и содержат больше информации, но не поддерживают фильтрацию.

---

## Подробный разбор

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

### **Как это работает на уровне EVM?**
1. **Log Entries:**
   - На уровне EVM события хранятся в виде логов.
   - Логи содержат:
     - Адрес контракта.
     - Темы (indexed параметры).
     - Данные (non-indexed параметры).

2. **Gas Costs:**
   - Запись событий дешевле, чем запись в `storage`.
   - Индексированные параметры увеличивают затраты газа.

---

### **Пример отслеживания событий через Web3.js**
```javascript
const Web3 = require('web3');
const web3 = new Web3('https://mainnet.infura.io/v3/YOUR_PROJECT_ID');

const abi = [/* ABI контракта */];
const contractAddress = '0xYourContractAddress';
const contract = new web3.eth.Contract(abi, contractAddress);

contract.events.Deposit({
    filter: { user: '0xYourAddress' },
    fromBlock: 0,
    toBlock: 'latest'
}, (error, event) => {
    if (!error) {
        console.log("Deposit detected:", event.returnValues);
    }
});
```

- В этом примере:
  - Приложение подписывается на событие `Deposit`.
  - Фильтрация выполняется по индексированному параметру `user`.

---

## Связанные темы
- [Вернуться к списку вопросов](5.%20Список%20вопросов.md)
- [[Каким образом оперативно отслеживать важные изменения в работе вашего смарт-контракта? Например: у вас есть контракт выпуска NFT и вы хотели бы знать когда и какая NFT была выпущена.]]
- [[Какую функциональность несет event, emmit?]]

---

## Источники
- [Solidity Documentation - Events](https://docs.soliditylang.org/en/latest/contracts.html#events)
- [Understanding Ethereum Logs and Events](https://ethereum.stackexchange.com/questions/12950/what-are-solidity-events-and-how-they-are-related-to-topics-and-logs)
---