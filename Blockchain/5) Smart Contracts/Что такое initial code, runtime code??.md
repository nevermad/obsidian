
## Короткий ответ

`Initial code` и `runtime code` — это две фазы кода смарт-контракта в Ethereum. `Initial code` выполняется при развертывании контракта для инициализации, а `runtime code` становится основным кодом контракта после его развертывания. Эти фазы разделены на уровне байт-кода EVM.

---

## Подробный разбор

### **Что такое `initial code`?**
1. **Определение:**
   - `Initial code` — это код, который выполняется при развертывании контракта.
   - Он содержит логику конструктора (`constructor`) и другие инструкции для инициализации контракта.

2. **Пример:**
   ```solidity
   contract Example {
       uint public value;

       constructor(uint initialValue) {
           value = initialValue;
       }
   }
   ```

   - В этом примере:
     - `Initial code` содержит инструкции для выполнения конструктора и установки значения переменной `value`.

3. **Технические детали:**
   - На уровне EVM `initial code` выполняется один раз при развертывании контракта.
   - После выполнения `initial code` генерируется `runtime code`.

4. **Особенности:**
   - `Initial code` может содержать сложную логику инициализации.
   - После выполнения конструктора `initial code` больше не используется.

5. **Подводные камни:**
   - Ошибки в `initial code` могут привести к неудачному развертыванию контракта.
   - Высокие затраты газа на выполнение сложного `initial code`.

---

### **Что такое `runtime code`?**
1. **Определение:**
   - `Runtime code` — это основной код контракта, который выполняется после его развертывания.
   - Он содержит реализацию всех функций контракта.

2. **Пример:**
   ```solidity
   contract Example {
       uint public value;

       function setValue(uint _value) public {
           value = _value;
       }

       function getValue() public view returns (uint) {
           return value;
       }
   }
   ```

   - В этом примере:
     - `Runtime code` содержит реализацию функций `setValue` и `getValue`.

3. **Технические детали:**
   - На уровне EVM `runtime code` сохраняется в блокчейне после выполнения `initial code`.
   - Выполняется при каждом вызове функций контракта.

4. **Особенности:**
   - `Runtime code` определяет поведение контракта после его развертывания.
   - Не содержит логики конструктора.

5. **Подводные камни:**
   - Неправильная реализация `runtime code` может привести к уязвимостям контракта.

---

### **Как это работает на уровне EVM?**
1. **Deployment Process:**
   - При развертывании контракта EVM выполняет `initial code`.
   - После выполнения `initial code` генерируется `runtime code`, который сохраняется в блокчейне.

2. **Gas Costs:**
   - Выполнение `initial code` требует газа.
   - Чем сложнее логика `initial code`, тем выше затраты газа.

3. **Пример байт-кода:**
   - `Initial code` содержит инструкции для выполнения конструктора.
   - `Runtime code` содержит инструкции для выполнения функций контракта.

---

### **Пример комбинированного использования**
```solidity
contract Bank {
    address public owner;
    uint public balance;

    constructor(address _owner, uint _balance) {
        owner = _owner;
        balance = _balance;
    }

    function deposit(uint amount) public {
        balance += amount;
    }

    function withdraw(uint amount) public {
        require(balance >= amount, "Insufficient balance");
        balance -= amount;
        payable(msg.sender).transfer(amount);
    }
}
```

- В этом примере:
  - `Initial code` инициализирует владельца (`owner`) и начальный баланс (`balance`).
  - `Runtime code` содержит реализацию функций `deposit` и `withdraw`.

---

### **Разница между `initial code` и `runtime code`**
| Характеристика      | `Initial Code`                     | `Runtime Code`                    |
|---------------------|------------------------------------|------------------------------------|
| **Выполнение**      | При развертывании контракта        | После развертывания контракта      |
| **Содержимое**      | Логика конструктора               | Реализация функций                |
| **Газовые затраты** | Высокие (зависит от сложности)     | Зависит от вызываемых функций      |
| **Использование**    | Инициализация контракта           | Основной код контракта            |

---

### **Пример отслеживания значений через `initial code`**
```javascript
const Web3 = require('web3');
const web3 = new Web3('https://mainnet.infura.io/v3/YOUR_PROJECT_ID');

const abi = [/* ABI контракта */];
const bytecode = '0x...'; // Байт-код контракта
const deployer = '0xYourAddress';

const contract = new web3.eth.Contract(abi);

const deployTx = contract.deploy({
    data: bytecode,
    arguments: [42] // Аргументы для конструктора
});

deployTx.send({
    from: deployer,
    gas: 3000000
}).then((instance) => {
    console.log("Contract deployed at:", instance.options.address);
});
```

- В этом примере:
  - Контракт разворачивается с аргументом `42` для конструктора.
  - `Initial code` выполняется для инициализации контракта.

---

## Связанные темы
- [Вернуться к списку вопросов](5.%20Список%20вопросов.md)
- [[Как работает constructor в контракте?]]
- [[Как работают модификаторы изменения состояния pure, view на уровне Solidity? Какие нюансы на уровне байткода EVM?]]

---

## Источники
- [Solidity Documentation - Contract Deployment](https://docs.soliditylang.org/en/latest/contracts.html#creating-contracts)
- [Understanding Ethereum Contract Deployment](https://ethereum.stackexchange.com/questions/7601/what-is-the-difference-between-bytecode-and-runtime-bytecode)
---
