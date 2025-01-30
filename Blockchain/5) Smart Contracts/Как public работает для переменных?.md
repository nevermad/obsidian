
## Короткий ответ

Ключевое слово `public` для переменных в Solidity автоматически создает геттер (getter) функцию, которая позволяет внешним контрактам и аккаунтам читать значение переменной. На уровне EVM это реализуется через специальную функцию, которая возвращает значение переменной из `storage`.

---

## Подробный разбор

### **Как работает `public` для переменных?**
1. **Определение:**
   - Переменные, объявленные как `public`, доступны как внутри контракта, так и извне.
   - Для каждой `public` переменной Solidity автоматически создает геттер функцию.

2. **Пример:**
   ```solidity
   contract Example {
       uint public value = 42;
   }
   ```

   - В этом примере:
     - Solidity автоматически создает функцию `value()`:
       ```solidity
       function value() external view returns (uint) {
           return value;
       }
       ```

3. **Технические детали:**
   - На уровне EVM геттер функция выполняет чтение значения переменной из `storage`.
   - Вызов геттера не требует газа, если он выполняется вне транзакции (например, через `call`).

4. **Особенности:**
   - Геттер функция имеет модификатор `view`, так как она только читает данные.
   - Имя геттера совпадает с именем переменной.

5. **Подводные камни:**
   - Некорректное использование `public` может привести к утечке конфиденциальных данных.
   - Если переменная является сложным типом (например, массив или структура), геттер может быть дорогостоящим.

---

### **Как это работает на уровне EVM?**
1. **Storage Slots:**
   - На уровне EVM каждая переменная хранится в определенном слоте `storage`.
   - Геттер функция считывает значение из соответствующего слота.

2. **Gas Costs:**
   - Чтение данных из `storage` требует газа.
   - Вызов геттера не требует газа, если он выполняется вне транзакции (например, через `call`).

3. **Пример байт-кода:**
   - Для переменной `value` геттер функция выполняет инструкцию `SLOAD`, чтобы прочитать значение из `storage`.

---

### **Пример комбинированного использования**
```solidity
contract Bank {
    uint public balance;

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
  - `balance` — это `public` переменная.
  - Solidity автоматически создает геттер функцию `balance()` для чтения значения переменной.

---

### **Геттеры для сложных типов данных**
1. **Массивы:**
   - Для массивов геттер возвращает элемент по индексу:
     ```solidity
     contract Example {
         uint[] public numbers;

         function addNumber(uint number) public {
             numbers.push(number);
         }
     }
     ```

     - Геттер для массива:
       ```solidity
       function numbers(uint index) external view returns (uint) {
           return numbers[index];
       }
       ```

2. **Структуры:**
   - Для структур геттер возвращает все поля:
     ```solidity
     contract Example {
         struct User {
             uint id;
             string name;
         }

         User public user;

         constructor(uint id, string memory name) {
             user = User(id, name);
         }
     }
     ```

     - Геттер для структуры:
       ```solidity
       function user() external view returns (uint, string memory) {
           return (user.id, user.name);
       }
       ```

---

### **Пример отслеживания значений через геттеры**
```javascript
const Web3 = require('web3');
const web3 = new Web3('https://mainnet.infura.io/v3/YOUR_PROJECT_ID');

const abi = [/* ABI контракта */];
const contractAddress = '0xYourContractAddress';
const contract = new web3.eth.Contract(abi, contractAddress);

async function getBalance() {
    const balance = await contract.methods.balance().call();
    console.log("Balance:", balance);
}

getBalance();
```

- В этом примере:
  - Внешнее приложение вызывает геттер `balance()` для получения значения переменной `balance`.

---

## Связанные темы
- [Вернуться к списку вопросов](5.%20Список%20вопросов.md)
- [[Как работают модификаторы изменения состояния pure, view на уровне Solidity? Какие нюансы на уровне байткода EVM?]]
- [[Что такое interface в Solidity? Как представлен на уровне EVM? Какие особенности и ограничения?]]

---

## Источники
- [Solidity Documentation - Visibility and Getters](https://docs.soliditylang.org/en/latest/contracts.html#visibility-and-getters)
- [Understanding Public Variables in Solidity](https://ethereum.stackexchange.com/questions/91874/what-is-the-difference-between-public-private-internal-and-external-functions)
---